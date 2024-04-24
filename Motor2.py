#ROS2 imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
#GPIO imports
import Jetson.GPIO as GPIO
#System imports
import os 
import time
#Unit system
import Unit


class Motor(Node):
    def __init__(self, name: str, enable_pin: int, A_pin: int, B_pin: int, input_pin: int):
        super().__init__(name)# ROS2 node initialization
        

if __name__ == "__main__":
    m1 = Motor("Winch", enable_pin = 19, A_pin = 15, B_pin = 13, input_pin = 11)