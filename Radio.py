import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Float32
import math
import time
class Radio(Node):
    def __init__(self, ser):
        super().__init__('radio')
        self.publisher_ = self.create_publisher(Float32, 'radio', 5)
        self.ser = ser
        self.time_ping = time.time()
        self.active = True
        self.publisher()

    def publisher(self):
        msg = Float32()
        while True:
            if self.ser.in_waiting >0:
                inp = self.ser.readline()[:-1] #ord(self.ser.read())
                print(inp,str(inp)[2:-1].split(",")[0])
                msg.data = float(str(inp)[2:-1].split(",")[0])#int.from_bytes(inp, "little") 
                self.publisher_.publish(msg)
                self.get_logger().info('radio: ' + str(msg.data))
                # print(inp, int.from_bytes(inp, "little") )
                # inp = self.ser.read() #ord(self.ser.read()) 
                # print(inp, ord(inp))
                # print(inp, int.from_bytes(inp, "little") )
                # msg.data = ord(inp)
                # if inp == 113:#q
                #     self.ser.write("OK\n".encode("utf-8"))
                #     if not self.active:
                #         self.get_logger().warning("Radio reconnected after {} seconds".format(int(time.time() -self.time_ping)))
                #         self.active = True
                #     self.time_ping = time.time()
                # else:
            # elif time.time() -self.time_ping > 20 and self.active:
            #     self.get_logger().warning("No radio pings received in : {} seconds".format(int(time.time() -self.time_ping)))
            #     self.active = False
                # self.radioReset()

    def radioReset(self):
        self.ser.write(bytes('+++', 'utf-8'))
        time.sleep(1)
        self.ser.write(bytes('ATB\n\r', 'utf-8'))
        time.sleep(1)
        self.ser.write(bytes('ATO\n\r', 'utf-8'))
        self.get_logger().info('radio reset complete')
        self.time_ping = time.time()

    
def main():
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=57600)
    rclpy.init()
    print("radio constructed")
    radio = Radio(ser)
    print("radio initalized")
    rclpy.spin(radio)
    radio.destroy_node()
    rclpy.shutdown()
    print("radio shutdown")


if __name__ == "__main__":
    main()
