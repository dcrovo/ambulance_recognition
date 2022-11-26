#!/home/camera/tflite/bin/python
import argparse
import utils
from detector.detector import AmbulanceDetection
from flask import Response
from flask import Flask
from flask import render_template, send_file
import threading
import argparse
import datetime
import time
import cv2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

def parse():
            
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='detector/efficientdet_lite0.tflite')
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--enableEdgeTPU',
        help='Whether to run the model on EdgeTPU.',
        action='store_true',
        required=False,
        default=False)
    args = parser.parse_args()
    return args


args = parse()
detector = AmbulanceDetection(args)
detector.loadModel()
outputFrame = None
lock = threading.Lock()
app = Flask(__name__)

def run(detector):
	# Variables to calculate FPS
	counter, fps = 0, 0
	start_time = time.time()
	global lock, outputFrame
	# Start capturing video input from the camera
	cap = cv2.VideoCapture(detector.cameraId)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, detector.frameWidth)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, detector.frameHeigth)

	# Continuously capture images from the camera and run inference
	while cap.isOpened():
		success, image = cap.read()
		if not success:
			sys.exit(
			'ERROR: Unable to read from webcam. Please verify your webcam settings.'
		)

		counter += 1
		image = cv2.flip(image, 1)

		# Convert the image from BGR to RGB as required by the TFLite model.
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# Create a TensorImage object from the RGB image.
		input_tensor = vision.TensorImage.create_from_array(rgb_image)

		# Run object detection estimation using the model.
		detection_result = detector.detector.detect(input_tensor)
		detector.detections = detection_result.detections
		# Draw keypoints and edges on input image
		image = utils.visualize(image, detection_result)
		
		# Calculate the FPS
		if counter % detector.fps_avg_frame_count == 0:
			end_time = time.time()
			fps = detector.fps_avg_frame_count / (end_time - start_time)
			start_time = time.time()

		# Show the FPS
		fps_text = 'FPS = {:.1f}'.format(fps)
		text_location = (detector.left_margin, detector.row_size)
		cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
					detector.font_size, detector.text_color, detector.font_thickness)
		with lock:
			outputFrame = image.copy()
			cv2.imwrite('Test.jpg', image)
			


@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

def generate():
	# grab global references to the output frame and lock variables
	global lock, outputFrame
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
				# check if the output frame is available, otherwise skip
				# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
			
			
@app.route("/video_feed")
def video_feed():
	
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
	 

if __name__ == '__main__':
	
	# start a thread that will run the object detector
	t = threading.Thread(target=run, args=(detector,))
	t.daemon = True
	t.start()
	# start the flask app
	app.run(host="0.0.0.0", port=5000, debug=True,
		threaded=True, use_reloader=False)
