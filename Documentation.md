# 2023-2024 Kehillah Sailbot Documentation

## Compass:
- **Constructor**: `Compass` takes 1 *PySerial* object ex:
```python 
compass = Compass(serial.Serial(port="/dev/ttyUSB0", baudrate=19200))
```
- **Publisher**: Publishes 1 `Float32` object with compass angle in degrees under the `"compass"` topic
- **Calibration**: Motor must be calibrated, calibration software can be found [here](https://www.wit-motion.com/searchq.html) and [here](https://drive.google.com/drive/u/0/folders/1I6sBC-8Q3_vtY-GrFDZbWJZJFk7UnNfO) and documentation [here](https://drive.google.com/drive/folders/1V7vE1aCca5QXJfwsxnFihDbj0dZtanuF) and [here](https://m.media-amazon.com/images/I/B164cgpgHQS.pdf).
- **ROS2 Debug/Info/Warnings**: It sends out a debug with the angle whenever it parses compass data

## Motor:
- **Constructor**: `Motor` takes `name: str`, `enable_pin: int`, `A_pin: int`, `B_pin: int`, `input_pin: int` ex: 
```python
winch = Motor(name = "Winch", enable_pin = 19, A_pin = 15, B_pin = 13, input_pin = 11)
```
- **Subscriber**: Subscribes to `"controller"` topic which broadcasts 1 `Float32` angle in degrees, motor then goes torwards that angle
- **Shutdown** is configured to shutdown motor and node when it receives exactly `100678576.0`
- **Calibration** TBD with the electrical team
- **ROS2 Debug/Info/Warnings**:
    - DEBUG: `"{self.name} Enable Off"`
    - DEBUG: `"{self.name} Enable On"`
    - INFO: `"{self.name} Board On"`
    - INFO: `"{self.name} Pins Enabled"`
    - INFO: `"{self.name} GPIO Exited"`
    - <y> WARN </y>: `"{self.name} received invalid target angle"`
    - <y> WARN </y>: `"{self.name} received pulse when gear=0! defaulting to last gear setting"`
    > [!NOTE]
    > DEBUGs don't show up in the console by default


<style>
r { color: Red }
o { color: Orange }
y { color: Yellow }
g { color: Green }
</style>