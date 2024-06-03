import rclpy
import pygame
from rclpy.node import Node
from std_msgs.msg import Float32

class RemoteController(Node):
    def __init__(self):
        super().__init__('RemoteController')
        self.publisher_ = self.create_publisher(Float32, 'controller', 5)

        self.controller = self.create_subscription(
            Float32,
            'radio',
            self.radio_callBack,
            5)
    def radio_callBack(self, msg):
        self.get_logger().info('Motor: "%s"' % str(msg.data))
        self.publisher_.publish(msg)
        print(msg)
def main():
    rclpy.init()
    print("remote control constructed")
    rc = RemoteController()
    print("remote control initalized")
    rclpy.spin(rc)
    rc.destroy_node()
    rclpy.shutdown()
    print("remote control shutdown")


if __name__ == "__main__":
    main()

        
    