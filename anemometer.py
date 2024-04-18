import time
import board
import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn

i2c = board.I2C()

# Initialize ADS7830
adc = ADC.ADS7830(i2c)
chan = AnalogIn(adc, 3)

while True:
    print(f"ADC channel 3 = {5/(2**16)*chan.value}, raw value:{chan.value}")
    time.sleep(0.1)

# import time
# import board
# import adafruit_ads7830.ads7830 as ADC
# from adafruit_ads7830.analog_in import AnalogIn

# i2c = board.I2C()

# # Initialize ADS7830
# adc = ADC.ADS7830(i2c)
# analog_inputs = []
# for i in range(8):
#     analog_inputs.append(AnalogIn(adc, i))

# while True:
#     for i in range(len(analog_inputs)):
#         print(f"ADC input {i} = {analog_inputs[i].value}")
#     time.sleep(0.1)