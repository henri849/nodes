import Jetson.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
print("Cleanup 1 done")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.cleanup()
print("Cleanup 2 done")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(19,GPIO.IN)
GPIO.setup(18,GPIO.IN)
GPIO.setup(15,GPIO.IN)
GPIO.setup(13,GPIO.IN)

GPIO.cleanup()
print("Cleanup 3 done")

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
print("Cleanup 1 done")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.cleanup()
print("Cleanup 2 done")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)
GPIO.setup(22,GPIO.IN)

GPIO.cleanup()
print("Cleanup 3 done")
