from operator import pos
import mediapipe as mp
import cv2
import numpy as np
import pyttsx3

class poseDetector():

    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.posture = self.mp_pose.Pose(min_detection_confidence=0.5)

        # for squats
        self.dir = 0
        self.count = 0

    # just finding and drawing the landmarks
    def findPose(self, frame, draw=True):
        # convert image to RGB
        imgRGB =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        self.results = self.posture.process(imgRGB)

        imgRGB.flags.writeable = True

        if self.results.pose_landmarks:
            if draw == True:
                self.mp_drawing.draw_landmarks(frame, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return (frame, self.results.pose_landmarks)

    # Creating a iteratable list of all 32 landmarks
    def findPosition(self, frame, draw=True):
        self.lmList = []
        self.lmlist_status = None

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = frame.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

        return self.lmList

    # finding angle between 3 given points
    def findAngle(self, frame, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Get the angle between these three points ( i.e., using numpy )
        a = np.array([x1,y1])
        b = np.array([x2,y2])
        c = np.array([x3,y3])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        # we get the angle in radians, converting into degrees
        angle = round(np.degrees(np.arccos(cosine_angle)))

        if draw:
            #cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            #cv2.line(frame, (x3, y3), (x2, y2), (255, 255, 255), 2)

            #cv2.circle(frame, (x1, y1), 5, (0, 255, 0), cv2.FILLED)
            #cv2.circle(frame, (x1, y1), 15, (0, 255, 0), 2)
            cv2.circle(frame, (x2, y2), 5, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (0, 255, 0), 2)
            #cv2.circle(frame, (x3, y3), 5, (0, 255, 0), cv2.FILLED)
            #cv2.circle(frame, (x3, y3), 15, (0, 255, 0), 2)

            #cv2.putText(frame, f"Hips's Angle = {angle}", (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        return(angle)

    def Squat_Exercise(self, frame):
        
        positions = self.findPosition(frame)

        hips_angle = self.findAngle(frame, 11, 23, 25, True)
        knee_angle = self.findAngle(frame, 23, 25, 27, True)

        if hips_angle >= 100:

            x2, y2 = positions[23][1:]

            image = cv2.arrowedLine(frame, (1200, 300), (1200, 400), (0, 0, 255), 4)

            cv2.circle(frame, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (0, 0, 255), 2)

            if knee_angle >= 100:
                
                x3, y3 = positions[25][1:]

                cv2.circle(frame, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x3, y3), 15, (0, 0, 255), 2)

        else:
            image = cv2.arrowedLine(frame, (1200, 400), (1200, 300), (0, 255, 0), 4)
        
        per = np.interp(hips_angle, (90, 160), (0, 100))

        if per == 100:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1

        if per == 0:
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0

        if self.count <=3:
            cv2.putText(frame, f"Count = {int(self.count)}/3", (900, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "Completed", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        return(frame)

         

       