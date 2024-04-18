import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Float32MultiArray
#sudo /home/kst/mambaforge/envs/2023Sailbot/bin/python /home/kst/Desktop/Coding/VideoServer.py
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import threading
import cv2, time
import datetime
from imutils.video import VideoStream
import numpy as np
# angle = 0
app = Flask('hello')
socketio = SocketIO(app,cors_allowed_origins="*")
camera = cv2.VideoCapture(0)  # CAP_DSHOW because of https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
camera.set(cv2.CAP_PROP_BUFFERSIZE, 0)

# camera = VideoStream(usePiCamera=False).start() # For Webcam


def crop_img(img, scale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

def gen_frames():  
    while True:
        #print(time.time())#python -m http.server 5000
        #ctime = time.time()
        success, frame = camera.read()
        # (B, G, R) = cv2.split(frame)
        # zeros = np.zeros(frame.shape[:2], dtype="uint8")
        # frame = cv2.merge([zeros, G, R])
        # # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR)
        # frame = crop_img(frame,0.10)
        if not success:
            print("no video")
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)#, [cv2.IMWRITE_JPEG_QUALITY, 30]
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #print(time.time()-ctime)
            # time.sleep(1)
@app.route('/video_feed')
def video_feed():
    print("here")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/compass')
# def compass():
#     # print(angle)
#     return  Response(str(angle))
    # return str(angle)
    # return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    return render_template('index.html')
#     return """
# <head>
#     <title>Boat Telemetry</title>
# </head>
# <body>
# <div class="container">
#     <center>
#         <div class="row">
#             <div class="col-lg-8  offset-lg-2">
#                 <h3 class="mt-5">Live Streaming</h3>
#                 <img id="video" src="/video_feed" width="80%">
#             </div>
#             <h3 id="compass" >Compass: </h3>
#             <h3 id="gps" >Gps: </h3>
#             <div class="map2"></div>    
#             <iframe id="map" src="https://www.google.com/maps/embed?pb=!1m10!1m8!1m3!1d329.5377637070215!2d-122.10497283935547!3d37.42497634887695!3m2!1i1024!2i768!4f13.1!5e1!3m2!1sen!2sus!4v1712513404953!5m2!1sen!2sus" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
#         </div>
#     </center>
# </div>
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/3.0.4/socket.io.js" integrity="sha512-aMGMvNYu8Ue4G+fHa359jcPb1u+ytAF+P2SCb+PxrjCdO3n3ZTxJ30zuH39rimUggmTwmh2u7wvQsDTHESnmfQ==" crossorigin="anonymous"></script>
#     <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
#     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
#     <script>
#         var socket;
#         $(document).ready(function() {
#             socket = io();
#             socket.on('compass', function(msg) {
#                 console.log(msg)
#                 document.getElementById('compass').innerHTML = 'Angle: ' + msg.data;
#             });
#             socket.on('gps', function(msg) {
#                 console.log(msg)
#                 document.getElementById('gps').innerHTML = 'Gps: ' + msg.data;
#                 x = msg.data.split(",")[1].substring(2)
#                 y = msg.data.split(",")[2].substring(1,msg.data.split(",")[2].length - 2)
#                 document.getElementById('map').src = "https://www.google.com/maps/embed?pb=!1m10!1m8!1m3!1d329.5377637070215!2d"+x+"!3d"+y+"!3m2!1i1024!2i768!4f13.1!5e1!3m2!1sen!2sus!4v1712513404953!5m2!1sen!2sus"
#                 var map = L.map('map2', {
#                     center: [51.505, -0.09],
#                     zoom: 13
#                 });
#             });
#             socket.on('disconnect', function() {
#                 console.log("Socket disconnected.");
#                 socket.socket.reconnect();
#             });
#         });
#     </script>
# </body>        
#      """
        # //var socket = io.connect('http://' + document.domain + ':' + location.port);
        # var socket = io();
        # socket.on('compass', function(msg) {
        #     console.log(msg)
        #     document.getElementById('compass').innerHTML = 'Angle: ' + msg.data;
        # });
# app.run(host='0.0.0.0', port=5000)
class Website(Node):

    def __init__(self):
        super().__init__('Website')
        self.subscription = self.create_subscription(
            Float32,
            'compass',
            self.compass_callback,
            1)
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'gps',
            self.gps_callback,
            1)
        self.subscription  # prevent unused variable warning

    @socketio.on('compass')
    def compass_callback(self, msg):
        self.get_logger().debug('I heard: "%s"' % str(msg.data))
        socketio.emit('compass', {'data': str(msg.data)})
        # socketio.sleep(1)
        # return str(msg.data)

    @socketio.on('gps')
    def gps_callback(self, msg):
        self.get_logger().debug('I heard: "%s"' % str(msg.data))
        socketio.emit('gps', {'data': str(msg.data)})
        # socketio.sleep(1)
        # return str(msg.data)
        


def main(args=None):
    rclpy.init(args=args)
    print("hello")
    minimal_subscriber = Website()
    print("created Node")
    rclpy.spin(minimal_subscriber)
    print("Ran node")
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    print("Shutting down")
    rclpy.shutdown()


if __name__ == '__main__':
    thr = threading.Thread(target=main, args={"debug": True}).start()
    socketio.run(app)#, args=['0.0.0.0', 5000,]
    
    

# if __name__ == '__main__':
#     threading.Thread(target = app.run, args=['0.0.0.0', 5000,]).start()
#     main()
    

