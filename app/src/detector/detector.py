import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils


class AmbulanceDetection():
    def __init__(self, args):

        self.model = args.model
        self.cameraId = int(args.cameraId)
        self.frameWidth = args.frameWidth
        self.frameHeigth = args.frameHeight
        self.numThreads = int(args.numThreads)
        self.enableEdgeTPU = bool(args.enableEdgeTPU)
        self.detections = []
            # Visualization parameters
        self.row_size = 20  # pixels
        self.left_margin = 24  # pixels
        self.text_color = (0, 0, 255)  # red
        self.font_size = 1
        self.font_thickness = 1
        self.fps_avg_frame_count = 10
    
    def loadModel(self):
        # Initialize the object detection model
        base_options = core.BaseOptions(
            file_name=self.model, use_coral=self.enableEdgeTPU, num_threads=self.numThreads)
        detection_options = processor.DetectionOptions(
            max_results=3, score_threshold=0.3)
        options = vision.ObjectDetectorOptions(
            base_options=base_options, detection_options=detection_options)
        self.detector = vision.ObjectDetector.create_from_options(options)
    
        
    def __detector__(self):
        return self.detector()
                 
