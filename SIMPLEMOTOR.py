import Jetson.GPIO as GPIO
import time

# Pin Definitions
input_pin = 23  # BCM pin 18, BOARD pin 12
# enable = 13
# A = 15
# B = 19
def main():
    prev_value = None

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
    # GPIO.setup(enable,GPIO.OUT)
    # GPIO.setup(A,GPIO.OUT)
    # GPIO.setup(B,GPIO.OUT)
    GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin

    # GPIO.output(enable,GPIO.LOW)
    # GPIO.output(A,GPIO.LOW)
    # GPIO.output(B,GPIO.LOW)

    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            value = GPIO.input(input_pin)
            print(value)
            # if value != prev_value:
            #     if value == GPIO.HIGH:
            #         value_str = "HIGH"
            #     else:
            #         value_str = "LOW"
            #     print("Value read from pin {} : {}".format(input_pin,
            #                                                value_str))
            #     prev_value = value
            time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("done")

if __name__ == '__main__':
    main()
# import Jetson.GPIO as GPIO
# import time
# idx = 0

# # Pin Definitons:
# inp_pin = 24  # Board pin 18
# def pulse(chan):
#     global idx

#     print("pulse",idx)
#     idx+=1


# def main():
#     # Pin Setup:
#     GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
#     GPIO.setup(inp_pin, GPIO.IN)  # button pin set as input
#     GPIO.add_event_detect(inp_pin, GPIO.RISING, callback = pulse) # event detector for motor pulse
#     time.sleep(10)
#     # print("Starting demo now! Press CTRL+C to exit")
#     # try:
#     #     while True:
#     #         print("Waiting for button event")
#     #         GPIO.wait_for_edge(inp_pin, GPIO.FALLING)

#     #         # event received when button pressed
#     #         print("Button Pressed!")
#     # finally:
#     #     GPIO.cleanup()  # cleanup all GPIOs

# if __name__ == '__main__':
#     main()