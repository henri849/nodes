import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Float32
import math
class Compass(Node):
    def __init__(self, ser):
        super().__init__('compass')
        self.publisher_ = self.create_publisher(Float32, 'compass', 5)
        self.ser = ser
        self.publisher()

    def publisher(self):
       sentence = []
       msg = Float32()
       while True:
            inp = int.from_bytes(self.ser.read(),"little")
            if inp == 0x55:
                if len(sentence)==10 and sentence[0] == 0x54:
                     parse = self.parse(sentence)
                     msg.data = parse
                     self.publisher_.publish(msg)
                     self.get_logger().debug('compass' + str(msg.data))
                sentence = []
            else:
                sentence.append(inp)


    def parse(self, data):
        mag_f = []
        for i in range(1, 7, 2):
            value = data[i+1]<<8 | data[i]
            if value >= 65536/2:
                value = -(65536-value)
            mag_f.append(value)
        return math.atan2(mag_f[1],mag_f[0])*180/math.pi
    
def main():
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=19200)
    rclpy.init()
    compass = Compass(ser)
    rclpy.spin(compass)
    compass.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()