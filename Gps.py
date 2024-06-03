
#sudo /home/kst/mambaforge/envs/2023Sailbot/bin/python /home/kst/Desktop/Coding/nmea.py
#use sudo pkill screen if no data is being returned after using the screen command
import pynmea2
import io
import serial
import time
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class Gps(Node):
    timer = time.time()
    def __init__(self, ser):
        super().__init__('gps') 
        self.publisher_ = self.create_publisher(Float32MultiArray, 'gps', 5)
        self.ser = ser
        self.time_ping = time.time()
        self.active = True
        self.publisher()
    import pynmea2
import io
import serial
import time
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class Gps(Node):
    def __init__(self, ser):
        super().__init__('gps') 
        self.publisher_ = self.create_publisher(Float32MultiArray, 'gps', 5)
        self.ser = ser
        self.prev_longitude = None
        self.prev_latitude = None
        self.prev_time = None
        self.active = True
        self.publisher()
    
    def publisher(self):
        while True:
            line = self.ser.readline().decode("utf-8")
            try:
                data = pynmea2.parse(line)
                current_longitude = data.longitude
                current_latitude = data.latitude

                if self.prev_longitude is not None and self.prev_latitude is not None:
                    distance = self.calculate_distance(self.prev_latitude, self.prev_longitude, current_latitude, current_longitude)
                    current_time = time.time()
                    time_elapsed = current_time - self.prev_time
                    velocity = distance / time_elapsed  # Velocity in meters per second
                    #self.publish_velocity(velocity)
"""
                self.prev_longitude = current_longitude
                self.prev_latitude = current_latitude
                self.longitude_velocity =
                self.prev_time = time.time()
                #once the longitude and latitude changes we want to check how much time has pase dot calculate the velocity
                if current_longitude != self.prev_longitude and current_latitude != self.current_latitude:
                    self.longitude_speed = ((time.time()-self.prev_time)/(current_longitude-self.prev_longitude))
                    self.latitude_speed = ((time.time()-self.prev_time)/(current_latitude-self.prev_latitude))
"""

            except Exception as e:
                pass
                # Handle exceptions

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Haversine formula to calculate distance between two points on a sphere
        R = 6371.0  # Radius of the Earth in kilometers
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c * 1000  # Convert distance to meters
        return distance
"""
    def publish_velocity(self, velocity):
        msg = Float32MultiArray()
        msg.data = [velocity]
        self.publisher_.publish(msg)
        self.get_logger().info('Velocity: {:.2f} m/s'.format(velocity))
"""
def main():
    ser =  serial.Serial('/dev/ttyUSB0', 38400, timeout=5.0)
    rclpy.init()
    gps = Gps(ser)
    rclpy.spin(gps)
    gps.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

    def publisher(self):
        msg = Float32MultiArray()
        while True:
            line = self.ser.readline().decode("utf-8")
            try:
                data = pynmea2.parse(line)
                # print(data)
                msg.data = [data.longitude, data.latitude]
                current_longitude = data.longitude
                current_latitude = data.latitude
                while current_longitude is not None and current_latitude is not None:
                    current_time = time.time()
                
                prev_time = current_time
                current_time = time.time()
                prev_distance = calculate_distance(self.prev_latitude, current_latitude, self.prev_longitude, current_longitude) 
                speed = ((calculate_distance(self.prev_latitude, current_latitude, self.prev_longitude, current_longitude)-prev_distance)/(current_time-prev_time))  

                #once the longitude and latitude changes we want to check how much time has pase dot calculate the velocity
                self.publisher_.publish(msg)
                self.get_logger().info('gps' + str(msg.data))
            except Exception as e:
                pass
                # self.get_logger().warn(str(e))
            # except Exception as e:
                # print(e)

def main():
    ser =  serial.Serial('/dev/ttyUSB0', 38400, timeout=5.0)
    # ser =  serial.Serial('/dev/ttyTHS1', 38400, timeout=5.0)#sudo chmod 666 /dev/ttyTHS1
    rclpy.init()
    gps = Gps(ser)
    rclpy.spin(gps)
    gps.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()