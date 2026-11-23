
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class TestingNode(Node):

    def __init__(self):
        super().__init__("testing_node")
        self.get_logger().info("Testing node started!")


def main(args=None):
    rclpy.init(args=args)

    node = TestingNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
