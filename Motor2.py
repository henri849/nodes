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
        #Saving pins pins
        self.name = name
        self.enable = enable_pin  #turns the motor on or off
        self.A = A_pin #Serves to set different angular velocities
        self.B = B_pin #Serves to set different angular velocities
        self.inp = input_pin # gives pulses every delta_pulse degrees

        self.GPIO_Setup()#GPIO - sets up all input-output functionallity

        self.Close()
    
    def GPIO_Setup(self):
        #board mode
        GPIO.setmode(GPIO.BOARD)
        self.get_logger().info(f"{self.name} On")
        #Input output initialization
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.A,GPIO.OUT)
        GPIO.setup(self.B,GPIO.OUT)
        GPIO.setup(self.inp,GPIO.IN)
        self.get_logger().info(f"{self.name} Enabled")
    
    def Close(self):
        GPIO.output(self.enable,GPIO.LOW) # turn motor off
        GPIO.cleanup() # exit GPIO
        self.get_logger().info(f"{self.name} Exited")
        exit()
        

if __name__ == "__main__":
    rclpy.init()
    m1 = Motor(name = "Winch", enable_pin = 19, A_pin = 15, B_pin = 13, input_pin = 11)
    rclpy.spin(m1)
    m1.destroy_node()
    rclpy.shutdown()
