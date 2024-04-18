#sudo /home/kst/mambaforge/envs/2023Sailbot/bin/python /home/kst/Desktop/Coding/nmea.py
#use sudo pkill screen if no data is being returned after using the screen command
import pynmea2
import io
import serial
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class Gps(Node):
    def __init__(self, ser):
        super().__init__('gps') 
        self.publisher_ = self.create_publisher(Float32MultiArray, 'gps', 5)
        self.ser = ser
        self.time_ping = time.time()
        self.active = True
        self.publisher()
    
    def publisher(self):
        msg = Float32MultiArray()
        while True:
            line = self.ser.readline().decode("utf-8")
            try:
                data = pynmea2.parse(line)
                # print(data)
                msg.data = [data.longitude, data.latitude]
                self.publisher_.publish(msg)
                self.get_logger().info('gps' + str(msg.data))
            except Exception as e:
                pass
                # self.get_logger().warn(str(e))
            # except Exception as e:
                # print(e)

def main():
    ser =  serial.Serial('/dev/ttyUSB1', 38400, timeout=5.0)
    # ser =  serial.Serial('/dev/ttyTHS1', 38400, timeout=5.0)#sudo chmod 666 /dev/ttyTHS1
    rclpy.init()
    gps = Gps(ser)
    rclpy.spin(gps)
    gps.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()