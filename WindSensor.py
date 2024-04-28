import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import board
import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn
import time
class WindSensor(Node):
    def __init__(self, chan):
        super().__init__('WindSensor')
        self.publisher_ = self.create_publisher(Float32, 'Wind', 5)
        self.chan = chan
        self.publisher()

    def publisher(self):
        msg = Float32()
        while True:
            parse = self.parse(self.chan.value)
            msg.data = parse
            self.publisher_.publish(msg)
            self.get_logger().debug(f"ADC channel 3 = {parse}, raw value:{self.chan.value}")
            time.sleep(0.1)

    def parse(self, data):
        return 360/(2**16)*data
    
def main():
    i2c = board.I2C()
    # Initialize ADS7830
    adc = ADC.ADS7830(i2c)
    chan = AnalogIn(adc, 3)

    rclpy.init()
    anemometer = WindSensor(chan)
    rclpy.spin(anemometer)
    anemometer.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()