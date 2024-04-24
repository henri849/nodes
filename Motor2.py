#ROS2 imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
#GPIO imports
import Jetson.GPIO as GPIO
#Unit system
import Unit


class Motor(Node):
    def __init__(self, name: str, enable_pin: int, A_pin: int, B_pin: int, input_pin: int):
        super().__init__(name)# ROS2 node initialization
        #Saving pins
        self.name = name
        self.enable = enable_pin  #turns the motor on or off
        self.A = A_pin #Serves to set different angular velocities
        self.B = B_pin #Serves to set different angular velocities
        self.inp = input_pin # gives pulses every delta_pulse degrees

        #GPIO - sets up all input-output functionallity
        self.GPIO_Setup()

        #Internal variables for controlling
        self.angle = Unit.Angle(0,"degrees") # current motor angle
        self.TargetAngle = Unit.Angle(0,"degrees") # angle the motor targets
        self.rates = {0:0,1:-100,2:100,3:-4000,4:4000} # different rates in rotations/minute
        self.last_gear = 0 # last speed setting
        self.gear =  0# current speed setting
        self.pulse_delta = Unit.Angle(360/16,"degrees") # how often the motors get a pulse, 16ppr

        #Rotation detection
        GPIO.add_event_detect(self.inp, GPIO.RISING, callback = self.pulse) # event detector for motor pulse

        self.Close()

    def pulse(self, channel):
        if self.rates[self.gear]>0: #if we are rotating CCW
            self.angle += Unit.Angle(self.pulse_delta,"degrees")
        if self.rates[self.gear]<0:#if we are rotating CW
            self.angle -= Unit.Angle(self.pulse_delta,"degrees")

        if self.rates[self.gear] == 0:# if our momentum carried us over when we stopped the motor
            self.get_logger().warn(f"{self.name} received pulse when gear=0! defaulting to last year setting")
            if self.rates[self.last_gear]>0: #if we are rotating CCW
                self.angle += Unit.Angle(self.pulse_delta,"degrees")
            if self.rates[self.last_gear]<0:#if we are rotating CW
                self.angle -= Unit.Angle(self.pulse_delta,"degrees")
    
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
    
    def Motor_Off(self):
        self.last_gear = self.gear 
        self.gear = 0 # set gear to zero
        GPIO.output(self.enable,GPIO.LOW) #turn off motor
        self.get_logger().debug("Motor Off")
    
    def Motor_On(self):
        GPIO.output(self.enable,GPIO.HIGH) #turn motor on
        self.get_logger().debug("Motor On")

    def Set_Gear(self,_gear: int):
        if _gear == 0: # Turns Motor Off
            self.Motor_Off()
        else:
            if self.gear == 0:# If Motor is Off and we're turning it on
                self.Motor_On()
            
            # Fun bitwise gearsetting, basically 1 gets mapped to A off B off, 2 A on B off, 3 A off B on, 4 A on B on
            GPIO.output(self.A,(_gear-1)%2)
            GPIO.output(self.B,((_gear-1)>>1)%2) 

            self.last_gear = self.gear #saves last gear
            self.gear = _gear #sets new gear

if __name__ == "__main__":
    rclpy.init()# Starts ROS2
    m1 = Motor(name = "Winch", enable_pin = 19, A_pin = 15, B_pin = 13, input_pin = 11)#Creates Winch object
    rclpy.spin(m1)# Launches Winch
    m1.destroy_node()# Destroys Winch once it's done running
    rclpy.shutdown()# Turns ROS2 Off
