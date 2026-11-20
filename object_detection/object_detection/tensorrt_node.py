
import cv2
import numpy as np
import rclpy
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from object_detection.decision_engine import decide

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


ENGINE_PATH = "/home/jc-bose-lab/ros2_ws/models/yolo11s_fp16.engine"

CONF_THRESHOLD = 0.25
NMS_THRESHOLD = 0.45

CLASS_NAMES = [
    "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon",
    "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet",
    "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator",
    "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
]


class TensorRTDetector(Node):

    def __init__(self):
        super().__init__('tensorrt_detector')

        self.bridge = CvBridge()

        # Load TensorRT engine
        self.logger = trt.Logger(trt.Logger.WARNING)
        trt.init_libnvinfer_plugins(self.logger, "")

        with open(ENGINE_PATH, 'rb') as f:
            self.runtime = trt.Runtime(self.logger)
            self.engine = self.runtime.deserialize_cuda_engine(f.read())

        if self.engine is None:
            raise RuntimeError("Failed to load TensorRT engine")

        self.trt_context = self.engine.create_execution_context()

        # Find input and output bindings
        self.input_index = None
        self.output_index = None

        for i in range(self.engine.num_bindings):
            if self.engine.binding_is_input(i):
                self.input_index = i
            else:
                self.output_index = i

        if self.input_index is None or self.output_index is None:
            raise RuntimeError("Expected one input and one output binding")

        input_shape = tuple(self.engine.get_binding_shape(self.input_index))

        if -1 in input_shape:
            raise RuntimeError(
                "Dynamic input shape detected; engine needs shape configuration"
            )

        self.input_height = input_shape[2]
        self.input_width = input_shape[3]

        output_shape = tuple(self.engine.get_binding_shape(self.output_index))

        self.get_logger().info("Input shape: {}".format(input_shape))
        self.get_logger().info("Output shape: {}".format(output_shape))

        # Allocate CUDA memory
        self.bindings = [0] * self.engine.num_bindings

        self.input_host = cuda.pagelocked_empty(
            trt.volume(input_shape),
            dtype=trt.nptype(self.engine.get_binding_dtype(self.input_index))
        )

        self.output_host = cuda.pagelocked_empty(
            trt.volume(output_shape),
            dtype=trt.nptype(self.engine.get_binding_dtype(self.output_index))
        )

        self.input_device = cuda.mem_alloc(self.input_host.nbytes)
        self.output_device = cuda.mem_alloc(self.output_host.nbytes)

        self.bindings[self.input_index] = int(self.input_device)
        self.bindings[self.output_index] = int(self.output_device)

        # ROS 2 subscriber and publisher
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/camera/detections',
            10
        )

        self.get_logger().info("YOLO11 TensorRT detector started")

    def preprocess(self, image):

        h, w = image.shape[:2]

        scale = min(
            self.input_width / w,
            self.input_height / h
        )

        new_w = int(round(w * scale))
        new_h = int(round(h * scale))

        resized = cv2.resize(image, (new_w, new_h))

        pad_x = (self.input_width - new_w) / 2
        pad_y = (self.input_height - new_h) / 2

        left = int(round(pad_x - 0.1))
        right = int(round(pad_x + 0.1))
        top = int(round(pad_y - 0.1))
        bottom = int(round(pad_y + 0.1))

        padded = cv2.copyMakeBorder(
            resized,
            top, bottom, left, right,
            cv2.BORDER_CONSTANT,
            value=(114, 114, 114)
        )

        rgb = cv2.cvtColor(padded, cv2.COLOR_BGR2RGB)

        blob = rgb.astype(np.float32) / 255.0
        blob = np.transpose(blob, (2, 0, 1))
        blob = np.expand_dims(blob, axis=0)

        return blob, scale, pad_x, pad_y

    def inference(self, image):

        blob, scale, pad_x, pad_y = self.preprocess(image)

        np.copyto(
            self.input_host,
            blob.ravel().astype(self.input_host.dtype)
        )

        cuda.memcpy_htod(self.input_device, self.input_host)

        success = self.trt_context.execute_v2(self.bindings)

        if not success:
            raise RuntimeError("TensorRT inference failed")

        cuda.memcpy_dtoh(self.output_host, self.output_device)

        predictions = self.output_host.reshape(
            tuple(self.trt_context.get_binding_shape(self.output_index))
        )

        predictions = np.squeeze(predictions)

        if predictions.ndim != 2:
            raise RuntimeError("Unexpected YOLO output dimensions")

        # YOLO11 output is normally (84, 8400).
        if predictions.shape[0] < predictions.shape[1]:
            predictions = predictions.T

        if predictions.shape[1] == 85:
            class_scores = predictions[:, 5:] * predictions[:, 4:5]
        else:
            class_scores = predictions[:, 4:]

        class_ids = np.argmax(class_scores, axis=1)
        scores = np.max(class_scores, axis=1)

        boxes = []
        confidences = []
        classes = []

        for i in range(len(scores)):

            if scores[i] < CONF_THRESHOLD:
                continue

            cx, cy, bw, bh = predictions[i, :4]

            x = (cx - bw / 2 - pad_x) / scale
            y = (cy - bh / 2 - pad_y) / scale
            width = bw / scale
            height = bh / scale

            boxes.append([
                int(x), int(y), int(width), int(height)
            ])

            confidences.append(float(scores[i]))
            classes.append(int(class_ids[i]))

        # Class-wise Non-Maximum Suppression
        
# Class-wise Non-Maximum Suppression using NumPy
        results = []

        for class_id in set(classes):

            indices = [
                i for i, c in enumerate(classes)
                if c == class_id
            ]

            indices.sort(
                key=lambda i: confidences[i],
                reverse=True
            )

            while indices:

                best = indices.pop(0)
                results.append(best)

                remaining = []

                x1, y1, w1, h1 = boxes[best]

                for i in indices:

                    x2, y2, w2, h2 = boxes[i]

                    xx1 = max(x1, x2)
                    yy1 = max(y1, y2)
                    xx2 = min(x1 + w1, x2 + w2)
                    yy2 = min(y1 + h1, y2 + h2)

                    intersection = max(0, xx2 - xx1) * max(0, yy2 - yy1)

                    area1 = w1 * h1
                    area2 = w2 * h2

                    union = area1 + area2 - intersection

                    iou = intersection / union if union > 0 else 0

                    if iou <= NMS_THRESHOLD:
                        remaining.append(i)

                indices = remaining

        return [
            (boxes[i], confidences[i], classes[i])
            for i in results
        ]


    def image_callback(self, msg):

        try:
            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

            detections = self.inference(frame)
            # Convert TensorRT detections for decision engine
            navigation_detections = []

            frame_height, frame_width = frame.shape[:2]

            for box, confidence, class_id in detections:

                x, y, w, h = box

                center_x = x + w // 2

                if center_x < frame_width // 3:
                    position = "LEFT"
                elif center_x < 2 * frame_width // 3:
                    position = "CENTER"
                else:
                    position = "RIGHT"

                navigation_detections.append({
                    "object": (
                    CLASS_NAMES[class_id]
                    if 0 <= class_id < len(CLASS_NAMES)
                    else "unknown"
                    ),
                    "confidence": confidence,
                    "position": position,
                    "bbox": (x, y, x + w, y + h)
                })

            # Get navigation decision
            decision = decide(
                navigation_detections,
                frame_width,
                frame_height
            )

            self.get_logger().info(
                "Action: {} | {}".format(
                    decision["action"],
                    decision["voice"]
                )
            )

            for box, confidence, class_id in detections:

                x, y, w, h = box

                x = max(0, x)
                y = max(0, y)
                x2 = min(frame.shape[1], x + w)
                y2 = min(frame.shape[0], y + h)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                class_name = (
                CLASS_NAMES[class_id]
                if 0 <= class_id < len(CLASS_NAMES)
                else "unknown"
                )

                label = "{}: {:.2f}".format(class_name, confidence)

                cv2.putText(
                    frame,
                    label,
                    (x, max(20, y - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            output_msg = self.bridge.cv2_to_imgmsg(
                frame,
                encoding='bgr8'
            )

            output_msg.header = msg.header
            self.publisher.publish(output_msg)

        except Exception as e:
            self.get_logger().error(str(e))


def main(args=None):

    rclpy.init(args=args)

    node = TensorRTDetector()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
