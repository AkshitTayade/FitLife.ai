import cv2
from .PoseModule import poseDetector
import numpy as np

posedetector = poseDetector()

class VideoCamera(object):
	
    def __init__(self, exercise_name):
        self.video = cv2.VideoCapture(0)
        self.exercise_name = exercise_name
       
    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        success, frame = self.video.read()

        try:
            frame,_ = posedetector.findPose(frame, False) 
           
            if self.exercise_name == 'squats':
                frame = posedetector.Squat_Exercise(frame)

            return (frame)

        except:
            return (frame)
