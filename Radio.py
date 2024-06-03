import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import time

class Radio(Node):
    def __init__(self, ser):
        super().__init__('radio')#Creating new node with name "radio"
        self.publisher_ = self.create_publisher(Float32MultiArray, 'controller', 5) #we'll proadcast what we get from the radio to other nodes through this topic called "controller"
        self.ser = ser # serial object, this is how we read from our radio module 
        self.publisher()# function that perpetually reads radio and broadcasts what it receives to other nodes
    
    def publisher(self):
        print("publisher on")
        inst = Float32MultiArray() # instructions are to be stored in here to be sent
        while True:
            # if self.ser.in_waiting >0: # if the radio has received anything it will go into the radio's buffer, this checks if the buffer is not empty
            parse = self.parse(self.ser.readline())# readline waits for a newline character "\n" then returns everythign before it including the \n 
            if parse != [1,2,3]:
                inst.data = parse
                self.get_logger().info('radio: ' + str(inst.data))
                self.publisher_.publish(inst)

    def parse(self,msg):
        try:
            msg = msg.split(b',')   
            return list(map(lambda a: float(round(float(a))),msg))#*200
        except:
            self.get_logger().warning("radio received bad input"+ str(msg))
            #msg= [msg[0][msg[0].find(".")+1:],msg[1]]
            #msg = list(map(lambda a : float(round(float(a)))))
            return [1,2,3]
if __name__ == "__main__":
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=57600)#sudo chmod 666 /dev/ttyACM0
    rclpy.init()
    print("radio constructed")
    radio = Radio(ser)
    print("radio initalized")
    rclpy.spin(radio)
    # radio.publisher()
    radio.destroy_node()
    rclpy.shutdown()
    print("radio shutdown")

