import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Char
# import radio
# import compass
import time
class RC(Node):

    def __init__(self):
        super().__init__('RC')
        # self.compass = self.create_subscription(
        #     Float32,
        #     'compass',
        #     self.compass_callback,
        #     5)
        # self.radio = self.create_subscription(
        #     Float32,
        #     'radio',
        #     self.radio_callback,
        #     5)
        self.publisher_ = self.create_publisher(Float32, 'controller', 5)
        msg2 = Float32()
        msg2.data = 100678576.0
        self.publisher_.publish(msg2)
        exit()


    def compass_callback(self, msg):
        self.get_logger().debug('compass: "%s"' % str(msg.data))
    def radio_callback(self, msg):
        msg2 = Float32()
        if msg.data > 100:
            msg2.data = float(-(360-msg.data*9/5))
        else:
            msg2.data = float(msg.data*9/5)
        self.get_logger().info('Motor: "%s"' % str(msg2.data))
        self.publisher_.publish(msg2)

if __name__  == "__main__":
    rclpy.init()
    rc_node = RC()
    print("RC Node created")
    rclpy.spin(rc_node)

    rc_node.destroy_node()
    print("Shutting down RC")
    rclpy.shutdown()
