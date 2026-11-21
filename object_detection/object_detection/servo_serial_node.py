
import rclpy
import serial

from rclpy.node import Node
from std_msgs.msg import String


class ServoSerialNode(Node):

    def __init__(self):
        super().__init__('servo_serial_node')

        self.ser = serial.Serial(
            '/dev/ttyACM0',
            115200,
            timeout=1
        )

        self.subscription = self.create_subscription(
            String,
            '/servo_command',
            self.command_callback,
            10
        )

        self.get_logger().info("Arduino servo connection established")

    def command_callback(self, msg):

        command = msg.data.strip()

        allowed_commands = [
            'MOVE_LEFT',
            'MOVE_RIGHT',
            'GO_FORWARD',
            'STOP'
        ]

        if command in allowed_commands:
            self.ser.write((command + '\n').encode())

            self.get_logger().info(
                f"Servo command sent: {command}"
            )

    def destroy_node(self):
        if self.ser.is_open:
            self.ser.close()

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = ServoSerialNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

