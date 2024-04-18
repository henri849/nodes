import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import Jetson.GPIO as GPIO
import os
import time
import Unit

class Motor(Node):
    def __init__(self, enable_pin, A_pin, B_pin, input_pin):
        
        super().__init__('Motor')# ROS2 node initialization
        
        #pins
        self.enable = enable_pin  #turns the motor on or off
        self.A = A_pin #Serves to set different angular velocities
        self.B = B_pin #Serves to set different angular velocities
        self.inp = input_pin # gives pulses every delta_pulse degrees

        #GPIO - sets up all input-output functionallity
        self.GPIO_Setup()

        #Rotation tracking
        self.angle = Unit.Angle(0,"degrees") # current motor angle
        self.TargetAngle = Unit.Angle(0,"degrees") # angle the motor targets
        self.rates = {0:0,1:-100,2:100,3:-4000,4:4000} # different rates in rotations/minute
        self.last_gear = 0 # last speed setting
        self.gear =  0# current speed setting
        self.pulse_delta = 360/16 # how often the motors get a pulse
        self.last_pulse = time.time() # time at last motor pulse
        self.current_pulse = time.time() # time we are querying for estimated rotation of when rotation stopped
        GPIO.add_event_detect(self.inp, GPIO.RISING, callback = self.pulse) # event detector for motor pulse

        #ROS subscribtion to controller node
        # self.controller = self.create_subscription(Float32, 'controller', self.Go_To, 5)
        #self.Set_Target_Angle(Unit.Angle(180,"degrees"))
        self.Motor_On()
        self.Go_To= True
        
        # while True:
        #     inp = int(input())
        #     if inp ==55:
        #         self.Close()
        #     else:
        #         # self.Set_Target_Angle(Unit.Angle(inp,"degrees"))
        #         # if self.angle >= self.TargetAngle:
        #         #     self.Set_Gear(1)
        #         # if self.angle <= self.TargetAngle:
        #         #     self.Set_Gear(2)
        #         self.Set_Gear(4)
        #         self.Motor_On()
                # self.pulse(0)
        self.controller = self.create_subscription(Float32, 'controller', self.Cont_Angle, 5)

    def Set_Target_Angle(self,angle):
        self.TargetAngle = angle

    def Cont_Angle(self,msg):
        # print("radio")
        self.get_logger().info('radio: "%s"' % str(msg.data))
        if msg.data == 190:
            self.Close()
        self.Set_Target_Angle(Unit.Angle(msg.data*2,"degrees"))
        if self.angle >= self.TargetAngle:
            self.Set_Gear(1)
        if self.angle <= self.TargetAngle:
            self.Set_Gear(2)
        self.Motor_On()

    def GPIO_Setup(self):
        #board mode
        GPIO.setmode(GPIO.BOARD)
        self.get_logger().debug("Board On")
        #Input output initialization
        GPIO.setup(self.enable,GPIO.OUT)
        GPIO.setup(self.A,GPIO.OUT)
        GPIO.setup(self.B,GPIO.OUT)
        GPIO.setup(self.inp,GPIO.IN)
        self.get_logger().debug("Enabled")

    def pulse(self, channel):
        print(self.Cont_Angle.get_as("degrees"))
        if self.rates[self.gear]>0: #if we are rotating CCW
            self.angle += Unit.Angle(self.pulse_delta,"degrees")

        #if self.rates[self.gear] == 0: #if we are no longer supposed to be rotating we revert to last velocity
            #if self.rates[self.last_gear]>0:
                #self.angle += Unit.Angle(self.pulse_delta,"degrees")
            #if self.rates[self.gear]<0:
                #self.angle -= Unit.Angle(self.pulse_delta,"degrees")

        if self.rates[self.gear]<0:#if we are rotating CW
            self.angle -= Unit.Angle(self.pulse_delta,"degrees")

        if self.Go_To: # Simple control loop to get to target angle as long as self.Go_To is TRUE
            # print(self.angle.get_as("degrees"), abs(self.angle.get_as("degrees")-self.TargetAngle.get_as("degrees")),self.pulse_delta/2)
            if abs(self.angle.get_as("degrees")-self.TargetAngle.get_as("degrees"))<self.pulse_delta/2:
                self.Motor_Off()
            else:
                if self.angle >= self.TargetAngle:
                    self.Set_Gear(1)
                if self.angle <= self.TargetAngle:
                    self.Set_Gear(2)  
                self.Motor_On()

        self.current_pulse = 0
        self.last_pulse = time.time()# save last pulse time

    def Motor_Off(self):
        self.last_gear = self.gear 
        self.gear = 0 # set gear to zero
        GPIO.output(self.enable,GPIO.LOW) #turn off motor
        self.get_logger().debug("Motor Off")
        self.current_pulse = time.time() # save time
    
    def Motor_On(self):
        GPIO.output(self.enable,GPIO.HIGH) #turn motor on
        self.get_logger().debug("Motor On")
        self.current_pulse = 0 # refresh current pulse, this will rarely have an impact

    def Close(self):
        GPIO.output(self.enable,GPIO.LOW) # turn motor off
        GPIO.cleanup() # exit GPIO
        self.get_logger().info("Exited")
        os._exit(0)

    def Set_Gear(self,_gear):
        if _gear == 0: # If motor is off
            self.get_logger().warn("Can't set motor speed gear to 0")

        self.last_gear = self.gear
        self.gear = _gear
        GPIO.output(self.A,(_gear-1)%2)# set the gear 
        GPIO.output(self.B,((_gear-1)>>1)%2)
    
    def Get_Rotation(self):
        if self.current_pulse == 0 and self.gear != 0: # if the motor wasn't stopped
            ang_v = Unit.Angular_Velocity(self.rates[self.gear],"rotations/minute") # how fast we are going
            delta_t =  Unit.Duration(time.time() - self.last_pulse,"seconds")# how long it's been
        else:
            ang_v = Unit.Angular_Velocity(self.rates[self.last_gear],"rotations/minute") # how fast we were going
            delta_t =  Unit.Duration(self.current_pulse - self.last_pulse,"seconds") # how long it had been

        if ang_v.get_as("degrees/second")> 0: # if we were rotating CCW
            delta_a = Unit.Angle(min(ang_v.get_as("degrees/second") * delta_t.get_as("seconds"),self.pulse_delta-0.01),"degrees") # add a maximum of 99.9
        else:
            delta_a = Unit.Angle(max(ang_v.get_as("degrees/second") * delta_t.get_as("seconds"),-self.pulse_delta+0.01),"degrees")# remove a maximum of 99.9
        return self.angle + delta_a

    
if __name__ == "__main__":
    rclpy.init()
    print("Motor Object constructed")
    m1 = Motor(enable_pin = 19, A_pin = 15, B_pin = 13, input_pin = 11)
    print("Motor Object initalized")
    rclpy.spin(m1)
    # m1.Go_To(Unit.Angle(360, "degrees"))
    # m1.Go()
    # print("Spun")
    m1.destroy_node()
    rclpy.shutdown()
