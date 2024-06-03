#ROS2 imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
#GPIO imports
import Jetson.GPIO as GPIO
#Unit system
import Unit
import time

class Motor(Node):
    def __init__(self, name: str, enable_pin: int, A_pin: int, B_pin: int, input_pin: int, radio_idx: int):
        super().__init__(name)# ROS2 node initialization
        #Saving pins
        self.name = name
        self.enable = enable_pin  #turns the motor on or off
        self.A = A_pin #Serves to set different angular velocities
        self.B = B_pin #Serves to set different angular velocities
        self.inp = input_pin # gives pulses every delta_pulse degrees
        self.Go_To = False
        self.idx = radio_idx
        self.ppr = 2
        if radio_idx == 0:
            self.ppr = 1*2
        if radio_idx == 1:
            self.ppr = 16*2
        #GPIO - sets up all input-output functionallity
        self.GPIO_Setup()

        #Internal variables for controlling
        self.angle = Unit.Angle(0,"degrees") # current motor angle
        self.TargetAngle = Unit.Angle(0,"degrees") # angle the motor targets

        #self.rates = {0:0,1:-800,2:800,3:-400,4:400} # different rates in rotations/minute

        if radio_idx == 0:
            self.rates = {0:0,1:-400,2:400,3:-400,4:400} # different rates in rotations/minute
            self.offset= 0
        if radio_idx == 1:
            self.rates = {0:0,1:-350,2:350,3:200,4:400} # different rates in rotations/minute
            self.offset = 0

        self.last_gear = 0 # last speed setting
        self.gear = 0# current speed setting
        self.pulse_delta = Unit.Angle(36/self.ppr,"degrees") # how often the motors get a pulse, 16ppr
        # self.Motor_On()
        # self.Set_Gear(1)# 1 is in, 2 is out
        # time.sleep(10)
        #msg = Float32MultiArray()
        #msg.data = [-360.0*4,-36.0]#- is in + is out
        #self.Set_Target_Angle(msg)
        #time.sleep(1*4)
        #self.Motor_Off()
        #self.Close()
        self.controller = self.create_subscription(Float32MultiArray,'controller', self.Set_Target_Angle, 5)
        #self.Close()

    def Set_Target_Angle(self, angle):
        #This should be a switch type statement but I think our python is too old for that
        if type(angle) == Float32MultiArray: # if it's a ROS2 message
            if angle.data[self.idx] == 100678576.0: # Some random number that's probably never going to occure turns the motor off
                self.Close()
            self.TargetAngle = Unit.Angle(angle.data[self.idx], "degrees")
        elif type(angle) == float or type(angle) == int: # if you receive the angle as a float or integer
            self.TargetAngle = Unit.Angle(angle, "degrees")
        elif type(angle) == Unit.Angle: # if it's already an Angle object
            self.TargetAngle = angle
        else:
            self.get_logger().warn(f"{self.name} received invalid target angle")
        self.get_logger().info(f"{self.name} received new target angle  {self.TargetAngle.get_as('degrees')}")
        self.Adjust_Motor()
        self.Go_To = True

    def pulse(self, channel):
        #print("pulse received")
        self.Pulse_Update_Rotation() # Updates self.angle to reflect receiving one pulse
        self.get_logger().info(f"{self.name} received pulse, "+str(self.angle.get_as("degrees")))

        if self.Go_To: # if we have some desired angle this boolean gets turned on
            self.Adjust_Motor()
    
    def Adjust_Motor(self):
        #To avoid waisting power if we're within half a pulse of the target angle we turn the motor off (the +5 is to avoid rounding errors)
        # This way in the worse case we're only half a pulse off, a pulse is 22.5 degrees but since it's geared down 10:1 half a pulse is only ~1.125 degrees
        # print(self.angle.get_as("degrees"),abs(self.angle.get_as("degrees")-self.TargetAngle.get_as("degrees")),self.pulse_delta.get_as("degrees")/2+5)
        if abs(self.angle.get_as("degrees")-self.TargetAngle.get_as("degrees"))<self.pulse_delta.get_as("degrees")/2+0.5:
            self.Set_Gear(0)
            self.Go_To = False
        else:
            if self.angle >= self.TargetAngle:#cw rotation
                self.Set_Gear(1)
            if self.angle <= self.TargetAngle:#ccw rotation
                self.Set_Gear(2)  
    
    def Pulse_Update_Rotation(self):
        if self.rates[self.gear]>0: #if we are rotating CCW
            self.angle += self.pulse_delta
        if self.rates[self.gear]<0:#if we are rotating CW
            self.angle -= self.pulse_delta

        if self.rates[self.gear] == 0:# if our momentum carried us over when we stopped the motor
            self.get_logger().warn(f"{self.name} received pulse when gear=0! defaulting to last gear setting")
            if self.rates[self.last_gear]>0: #if we are rotating CCW
                self.angle += self.pulse_delta
            if self.rates[self.last_gear]<0:#if we are rotating CW
                self.angle -= self.pulse_delta

    def GPIO_Setup(self):
        #board mode
        GPIO.setmode(GPIO.BOARD)
        self.get_logger().info(f"{self.name} Board On")
        #Input output initialization
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.A,GPIO.OUT)
        GPIO.setup(self.B,GPIO.OUT)
        GPIO.setup(self.inp,GPIO.IN)
        self.get_logger().info(f"{self.name} Pins Enabled")
        
        #Rotation detection
        GPIO.add_event_detect(self.inp, GPIO.BOTH, callback = self.pulse) # event detector for motor pulse
        self.get_logger().info(f"{self.name} Event Detector Enabled")

    def Close(self):
        GPIO.output(self.enable,GPIO.LOW) # turn motor off
        GPIO.cleanup() # exit GPIO
        self.get_logger().info(f"{self.name} GPIO Exited")
        exit()
    
    def Motor_Off(self):
        self.last_gear = self.gear 
        self.gear = 0 # set gear to zero
        GPIO.output(self.enable,GPIO.LOW) #turn off motor
        self.get_logger().debug(f"{self.name} Enable Off")
    
    def Motor_On(self):
        GPIO.output(self.enable,GPIO.HIGH) #turn motor on
        self.get_logger().debug(f"{self.name} Enable On")

    def Set_Gear(self,_gear: int):
        if _gear == 0: # Turns Motor Off
            self.Motor_Off()
        else:
            self.last_gear = self.gear #saves last gear
            self.gear = _gear #sets new gear

            if self.last_gear == 0:# If Motor is Off and we're turning it on
                self.Motor_On()
            # Fun bitwise gearsetting, basically _gear=1 gets mapped to A off B off, 2 A on B off, 3 A off B on, 4 A on B on
            GPIO.output(self.A,(_gear-1+self.offset)%2)
            GPIO.output(self.B,((_gear-1+self.offset)>>1)%2) 


if __name__ == "__main__":
    rclpy.init()# Starts ROS2
    #m1 = Motor(name = "Winch", enable_pin = 19, A_pin = 15, B_pin = 13, input_pin = 23, radio_idx=0)#Creates Winch object
    m1 = Motor(name = "Rudder", enable_pin = 16, A_pin = 18, B_pin = 22, input_pin = 24, radio_idx=1)#Creates Winch object
    rclpy.spin(m1)# Launches Winch
    m1.destroy_node()# Destroys Winch once it's done running
    rclpy.shutdown()# Turns ROS2 Off
