## 2023-2024 Kehillah Sailbot Documentation

## Compass:
- **Constructor**: `Compass` takes 1 *PySerial* object ie: `Compass(serial.Serial(port="/dev/ttyUSB0", baudrate=19200))`
- **Publisher**: Publishes 1 `Float32` object with compass angle in degrees under the `"compass"` topic
- **Calibration**: Motor must be calibrated, calibration software can be found [here](https://www.wit-motion.com/searchq.html) and [here](https://drive.google.com/drive/u/0/folders/1I6sBC-8Q3_vtY-GrFDZbWJZJFk7UnNfO) and documentation [here](https://drive.google.com/drive/folders/1V7vE1aCca5QXJfwsxnFihDbj0dZtanuF) and [here](https://m.media-amazon.com/images/I/B164cgpgHQS.pdf).
- **ROS2 Debug/Info/Warnings**: It sends out a debug with the angle whenever it parses compass data

## Compass:
