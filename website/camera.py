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
           
            if self.exercise_name == 'squat':
                frame = posedetector.Squat_Exercise(frame)

            elif self.exercise_name == 'jumping jack':
                frame = posedetector.Jumping_Jack(frame)

            elif self.exercise_name == 'adbominal crunches':
                frame = posedetector.Adbominal_crunches(frame)

            elif self.exercise_name == 'knee pushup':
                frame = posedetector.Knee_pushup(frame)

            elif self.exercise_name == 'side arm raises':
                frame = posedetector.Side_arm_raises(frame)

            elif self.exercise_name == 'backward lunges':
                frame = posedetector.Backward_Lunges(frame)

            elif self.exercise_name == 'cobra stretch':
                frame = posedetector.Cobra_Stretch(frame)

            return (frame)

        except:
            return (frame)
