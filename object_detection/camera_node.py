
import cv2
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')

        self.publisher = self.create_publisher(
            Image, '/camera/image_raw', 10
        )

        self.bridge = CvBridge()

        self.camera = cv2.VideoCapture('/dev/video1')

        # Use MJPEG camera format
        self.camera.set(
            cv2.CAP_PROP_FOURCC,
            cv2.VideoWriter_fourcc(*'MJPG')
        )

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.camera.isOpened():
            raise RuntimeError("Cannot open Logitech C270")

        self.timer = self.create_timer(0.05, self.publish_frame)

        self.get_logger().info("Logitech C270 camera started")

    def publish_frame(self):
        ret, frame = self.camera.read()

        if not ret:
            self.get_logger().error("Camera frame capture failed")
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'

        self.publisher.publish(msg)

    def destroy_node(self):
        self.camera.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
