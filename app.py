#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import time

import firenet


# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    #from camera import Camera
    from camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


load_fire = False


@app.route('/test')
def test():
    return "test!!!"


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video')
def video_with_path():
    path = request.args.get('path')
    if not path:
        path = 0

    return render_template('video_with_path.html', path=path)


def gen_firenet(path):
    print("before load")
    firenet.load()
    print("after load")

    """Video streaming generator function."""
    for frame in firenet.get_frame(path): 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed_with_path')
def video_feed_with_path():
    path = request.args.get('path')
    return Response(gen_firenet(path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9500, debug=True, threaded=True)

