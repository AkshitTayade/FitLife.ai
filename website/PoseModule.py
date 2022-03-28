# Beginner Playlist count
# Squats = 12
# Lunges = 14
# Jumping jacks 10
# crunhes = 8
# pushup = 12
# arm raise = 15

import mediapipe as mp
import cv2
import numpy as np
import datetime
import json
from tblib import Frame
import time

class poseDetector():

    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.posture = self.mp_pose.Pose(min_detection_confidence=0.5)

        # overall time
        self.j = 0
        self.i = 1

        # for squats
        self.dir = 0
        self.count = 0

        # for jumping jack
        self.dir_jj = 0
        self.count_jj = 0

        # for crunches
        self.count_ac = 0
        self.dir_ac = 0

        # for knee pushup
        self.dir_kp = 0
        self.count_kp = 0

        # for side arm raise
        self.dir_sar = 0
        self.count_sar = 0

        # for backward lunges
        self.l_dir_bl = 0
        self.l_count_bl = 0
        self.r_dir_bl = 0
        self.r_count_bl = 0

        # for cobra stretch
        self.mins = 0
        self.sec = 0
        self.period = '00:00'

        self.file = open('website/exercise_timing.json', 'r+')

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
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.line(frame, (x3, y3), (x2, y2), (255, 255, 255), 2)
            
            cv2.circle(frame, (x1, y1), 5, (0, 255, 0), cv2.FILLED)
            #cv2.circle(frame, (x1, y1), 15, (0, 255, 0), 2)
            cv2.circle(frame, (x2, y2), 5, (0, 255, 0), cv2.FILLED)
            #cv2.circle(frame, (x2, y2), 15, (0, 255, 0), 2)
            cv2.circle(frame, (x3, y3), 5, (0, 255, 0), cv2.FILLED)
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

        if self.i == 1:
            if self.count <= 0.5:
                self.earlier = datetime.datetime.now()
                #earlier_lt.append(earlier)
                print("Start = ",self.earlier)
                self.i += 1
        
        if self.i == 2:
            if int(self.count) == 12:
               
                now = datetime.datetime.now()
                    
                diff = now - self.earlier

                print("Diff = ", diff.total_seconds())

                data = json.load(self.file)
                data.update({"Total_seconds": diff.total_seconds(), 
                            "Timestamp": time.strftime('%H:%M:%S', time.gmtime(int(diff.total_seconds()))),
                            "Total_Reps": 12})
                self.file.seek(0)
                json.dump(data, self.file)
                self.file.close()

                self.i += 1

        if self.count >= 12:
            cv2.putText(frame, "Completed", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        else:
            cv2.putText(frame, f"Count = {int(self.count)}/12", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            
        return(frame)

    def Jumping_Jack(self, frame):

        positions = self.findPosition(frame)

        # left-ankle & right-ankle
        x_left_1, y_left_1 = positions[27][1:]
        x_right_2, y_right_2 = positions[28][1:]

        euclidian_dist_bottom = int(((x_left_1 - x_right_2)**2 + (y_left_1 - y_right_2)**2)**0.5)
        #print(euclidian_dist_bottom)

        # left-wrist & right-wrist
        x_left_3, y_left_3 = positions[15][1:]
        x_right_4, y_right_4 = positions[16][1:]

        euclidian_dist_upper = int(((x_left_3 - x_right_4)**2 + (y_left_3 - y_right_4)**2)**0.5)
        #print(euclidian_dist_upper)

        per = np.interp(euclidian_dist_bottom, (40, 175), (0, 100))
        #print(euclidian_dist_bottom, per)
        
        if per == 100:
            if self.dir_jj == 0:
                self.count_jj += 0.5
                self.dir_jj == 1

        if per == 0:
            if self.dir_jj == 1:
                self.count_jj += 0.5
                self.dir_jj == 0

        if self.i == 1:
            if self.count_jj <= 0.5:
                self.earlier = datetime.datetime.now()
                #earlier_lt.append(earlier)
                print("Start = ",self.earlier)
                self.i += 1
        
        if self.i == 2:
            if int(self.count_jj/4) == 10:
               
                now = datetime.datetime.now()
                    
                diff = now - self.earlier

                print("Diff = ", diff.total_seconds())

                data = json.load(self.file)
                data.update({"Total_seconds": diff.total_seconds(), 
                            "Timestamp": time.strftime('%H:%M:%S', time.gmtime(int(diff.total_seconds()))),
                            "Total_Reps": 10})
                self.file.seek(0)
                json.dump(data, self.file)
                self.file.close()

                self.i += 1
                
        if int(self.count_jj/4) >= 10:
            cv2.putText(frame, f"Completed", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        else:
            cv2.putText(frame, f"Count = {int(self.count_jj/4)}/10", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        cv2.line(frame, (x_left_1, y_left_1), (x_right_2, y_right_2), (0, 255, 0), 3)
        cv2.line(frame, (x_left_3, y_left_3), (x_right_4, y_right_4), (0, 255, 0), 3)
        cv2.circle(frame, (x_left_1, y_left_1), 5, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x_right_2, y_right_2), 5, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x_left_3, y_left_3), 5, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x_right_4, y_right_4), 5, (0, 255, 0), cv2.FILLED)

        return(frame)

    def Adbominal_crunches(self, frame):
        
        positions = self.findPosition(frame)
        #print(positions)
        #print()

        left_knee_angle = self.findAngle(frame, 23, 25, 27, True)
        hip_angle = self.findAngle(frame, 11, 23, 25, True)

        #print("Knee Angle - ",left_knee_angle)
        #knee angle should be between 80-90 degree

        #print("Hips Angle - ", hip_angle)
        # hips angle should be between 110-145
        
        if (left_knee_angle<=85):
            x3, y3 = positions[25][1:]
            
            cv2.circle(frame, (x3, y3), 5, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (x3, y3), 15, (0, 255, 0), 2)

            if (hip_angle < 130):
                x2, y2 = positions[23][1:]
                
                cv2.circle(frame, (x2, y2), 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 15, (0, 255, 0), 2)
    
                #print("Perfect posture")

        if (left_knee_angle>90):
            
            #print("Keep your legs close to your thighs")

            x3, y3 = positions[25][1:]
            cv2.circle(frame, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x3, y3), 15, (0, 0, 255), 2)

        if (hip_angle >= 130):
        
            #print("Try to lift up your body")
        
            x2, y2 = positions[23][1:]
            cv2.circle(frame, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (0, 0, 255), 2)
        
        per = np.interp(hip_angle, (120, 140), (0, 100))
        
        if left_knee_angle < 100:
            if per == 100:
                if self.dir_ac == 0:
                    self.count_ac += 0.5
                    self.dir_ac = 1

            if per == 0:
                if self.dir_ac == 1:
                    self.count_ac += 0.5
                    self.dir_ac = 0

        if self.i == 1:
            if self.count_ac <= 0.5:
                self.earlier = datetime.datetime.now()
                #earlier_lt.append(earlier)
                print("Start = ",self.earlier)
                self.i += 1
        
        if self.i == 2:
            if int(self.count_ac) == 8:
               
                now = datetime.datetime.now()
                    
                diff = now - self.earlier

                print("Diff = ", diff.total_seconds())

                data = json.load(self.file)
                data.update({"Total_seconds": diff.total_seconds(), 
                            "Timestamp": time.strftime('%H:%M:%S', time.gmtime(int(diff.total_seconds()))),
                            "Total_Reps": 8})
                self.file.seek(0)
                json.dump(data, self.file)
                self.file.close()

                self.i += 1

        if int(self.count_ac) <=8:
            cv2.putText(frame, f"Count = {int(self.count_ac)}/8", (900, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "Completed", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        
        return(frame)

    def Knee_pushup(self, frame):
        
        positions = self.findPosition(frame)

        knee = self.findAngle(frame, 24, 26, 28, True)
        elbow = self.findAngle(frame, 11, 13, 15, True)

        #print(f"knee = {knee}")
        #print(f"elbow = {elbow}")

        if (knee < 100) and (knee > 70):
            x3, y3 = positions[26][1:]
        
            cv2.circle(frame, (x3, y3), 5, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (x3, y3), 15, (0, 255, 0), 2)

            if elbow < 120:
                x2, y2 = positions[13][1:]
            
                cv2.circle(frame, (x2, y2), 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 15, (0, 255, 0), 2)

                    #print("Perfect posture")

        if knee > 100:
            x3, y3 = positions[26][1:]
        
            cv2.circle(frame, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x3, y3), 15, (0, 0, 255), 2)

            #print("Keep your knee close to your butt")

        if elbow >= 100:
            x2, y2 = positions[13][1:]
            
            cv2.circle(frame, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (0, 0, 255), 2)

            #print("Bend down")

        per = np.interp(elbow, (90, 160), (0, 100))
    
        if (knee < 100) and (knee > 70):
            if per == 100:
                if self.dir_kp == 0:
                    self.count_kp += 0.5
                    self.dir_kp = 1

            if per == 0:
                if self.dir_kp == 1:
                    self.count_kp += 0.5
                    self.dir_kp = 0
        
        if self.i == 1:
            if self.count_kp <= 0.5:
                self.earlier = datetime.datetime.now()
                #earlier_lt.append(earlier)
                print("Start = ",self.earlier)
                self.i += 1
        
        if self.i == 2:
            if int(self.count_kp) == 12:
               
                now = datetime.datetime.now()
                    
                diff = now - self.earlier

                print("Diff = ", diff.total_seconds())

                data = json.load(self.file)
                data.update({"Total_seconds": diff.total_seconds(), 
                            "Timestamp": time.strftime('%H:%M:%S', time.gmtime(int(diff.total_seconds()))),
                            "Total_Reps": 12})
                self.file.seek(0)
                json.dump(data, self.file)
                self.file.close()

                self.i += 1

        if int(self.count_kp) <= 12:
            cv2.putText(frame, f"Count = {int(self.count_kp)}/12", (500, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        else:
            cv2.putText(frame, f"Completed", (500, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        
        return(frame)

    def Side_arm_raises(self, frame):
    
        positions = self.findPosition(frame)

        left_shoulder = self.findAngle(frame, 13, 11, 23, True)
        right_shoulder = self.findAngle(frame, 14, 12, 24, True)

        # left-shoulder & right-shoudler
        x_left_1, y_left_1 = positions[11][1:]
        x_right_2, y_right_2 = positions[12][1:]

        euclidian_dist_shoudler = int(((x_left_1 - x_right_2)**2 + (y_left_1 - y_right_2)**2)**0.5)
        #print(euclidian_dist_shoudler)

        # left-ankle & right-ankle
        x_left_3, y_left_3 = positions[27][1:]
        x_right_4, y_right_4 = positions[28][1:]

        euclidian_dist_bottom = int(((x_left_3 - x_right_4)**2 + (y_left_3 - y_right_4)**2)**0.5)
        #print(euclidian_dist_bottom)

        #print(f"Left = {left_shoulder}, Right = {right_shoulder}")

        if left_shoulder > 100:
            x, y = positions[11][1:]

            x1, y1 = positions[15][1:]
        
            cv2.arrowedLine(frame, (x1, y1), (x1, y1+80), (0, 0, 255), 2)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)
            
            #print("Try to keep your hand parallel to the ground")

        if right_shoulder > 100:
            x, y = positions[12][1:]

            x1, y1 = positions[16][1:]
        
            cv2.arrowedLine(frame, (x1, y1), (x1, y1+80), (0, 0, 255), 2)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)
            
            #print("Try to keep your hand parallel to the ground")
        
        if euclidian_dist_bottom < euclidian_dist_shoudler:

            cv2.arrowedLine(frame, (x_left_3, y_left_3), (x_left_3+60, y_left_3), (0, 0, 255), 2)
            cv2.arrowedLine(frame, (x_right_4, y_right_4), (x_right_4-60, y_right_4), (0, 0, 255), 2)
            #cv2.line(frame, (x_left_3, y_left_3), (x_right_4, y_right_4), (0, 0, 255), 2)

            #print("Increase the distance between your ankles")


        left_per = np.interp(left_shoulder, (20, 90), (0, 100))
        right_per = np.interp(right_shoulder, (20, 90), (0, 100))

        #print(f"Left = {left_per}, Right = {right_per}")

        if euclidian_dist_bottom >= euclidian_dist_shoudler:
            #then perform counting
            
            if (left_per == 0) and (right_per == 0):
                if self.dir_sar == 0:
                    self.count_sar += 0.5
                    self.dir_sar = 1
            
            if (left_per == 100) and (right_per == 100):
                if self.dir_sar == 1:
                    self.count_sar += 0.5
                    self.dir_sar = 0

            cv2.line(frame, (x_left_3, y_left_3), (x_right_4, y_right_4), (0, 255, 0), 2)

        if self.i == 1:
            if self.count_sar <= 0.5:
                self.earlier = datetime.datetime.now()
                #earlier_lt.append(earlier)
                print("Start = ",self.earlier)
                self.i += 1
        
        if self.i == 2:
            if int(self.count_sar) == 15:
               
                now = datetime.datetime.now()
                    
                diff = now - self.earlier

                print("Diff = ", diff.total_seconds())

                data = json.load(self.file)
                data.update({"Total_seconds": diff.total_seconds(), 
                            "Timestamp": time.strftime('%H:%M:%S', time.gmtime(int(diff.total_seconds()))),
                            "Total_Reps": 15})
                self.file.seek(0)
                json.dump(data, self.file)
                self.file.close()

                self.i += 1

        if int(self.count_sar) >= 15:
            cv2.putText(frame, f"Completed", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f"Count = {int(self.count_sar)}/15", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
        return(frame)

    def Backward_Lunges(self, frame):
        
        positions = self.findPosition(frame)

        # left-knee
        left_knee = self.findAngle(frame, 23, 25, 27, True)
        # right-knee
        right_knee = self.findAngle(frame, 24, 26, 28, True)

        #print(f"Left = {left_knee}, Right = {right_knee}")
        
        if left_knee < 75:
            x, y = positions[25][1:]
            
            #cv2.putText(frame, f"You are leaning way too back, Keep your Left Knee at 90 degree", (200, 700), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
            print("You are leaning way too back, Keep your Left Knee at 90 degree")
            
            cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)

        if right_knee < 75:
            x, y = positions[26][1:]
            
            #cv2.putText(frame, f"You are leaning way too back, Keep your Right Knee at 90 degree", (200, 700), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
            print("You are leaning way too back, Keep your Right Knee at 90 degree by streching your leg")
            
            cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)

        left_per = int(np.interp(left_knee, (90, 170), (0, 100)))
        right_per = int(np.interp(left_knee, (90, 170), (0, 100)))

        #print(f"Left = {left_per}, Right = {right_per}")
        #cv2.putText(frame, f"Left = {left_per}, Right = {right_per}", (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        if left_per == 100:
            if self.l_dir_bl == 0:
                self.l_count_bl += 0.5
                self.l_dir_bl = 1

        if left_per == 0:
            if self.l_dir_bl == 1:
                self.l_count_bl += 0.5
                self.l_dir_bl = 0

        if right_per == 100:
            if self.r_dir_bl == 0:
                self.r_count_bl += 0.5
                self.r_dir_bl = 1

        if right_per == 0:
            if self.r_dir_bl == 1:
                self.r_count_bl += 0.5
                self.r_dir_bl = 0

        if self.i==1:
            if self.l_count_bl <= 0.5:
                earlier = datetime.datetime.now()
                #earlier_lt.append(earlier)
                print(earlier)
                self.i = self.i + 1
        
        if self.i==2:
            if int(int(int(self.l_count_bl/2) + int(self.r_count_bl/2))/2) == 14:
                now = datetime.datetime.now()
                #print(now)
                
                diff = now - earlier

                #print(diff.total_seconds())

                data = json.load(self.file)
                data.update({"Total_seconds": diff.total_seconds(), 
                            "Timestamp": time.strftime('%H:%M:%S', time.gmtime(int(diff.total_seconds()))),
                            "Total_Reps": 14})
                self.file.seek(0)
                json.dump(data, self.file)
                self.file.close()

                self.i = self.i + 1
        

        if int(int(int(self.l_count_bl/2) + int(self.r_count_bl/2))/2) <= 14:
            cv2.putText(frame, f"Total Reps = {int(int(int(self.l_count_bl/2) + int(self.r_count_bl/2))/2)}/14", (900, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(frame, f"Left = {int(self.l_count_bl/2)}", (900, 140), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(frame, f"Right = {int(self.r_count_bl/2)}", (900, 180), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f"Completed", (900, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
       
        return(frame)

    def Cobra_Stretch(self, frame):
        
        positions = self.findPosition(frame)

        elbow = self.findAngle(frame, 11, 13, 15, True)
        leg = self.findAngle(frame, 23, 25, 27, True)
        head_angle = self.findAngle(frame, 0, 11, 23, True)
        #print(head_angle)

        if elbow <= 150:
            x, y = positions[13][1:]
        
            cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)

        #print(f"elbow = {elbow}, back = {spinal}")

        elbow_per = np.interp(elbow, (60, 150), (0, 100))

        if elbow_per == 100:
            if head_angle > 150:
                if leg > 150:
                    if self.period != "10:00":
                        if self.sec > 59:
                            self.sec = 0
                            self.mins = self.mins+1

                        if self.mins > 59:
                            self.mins = 0
                    
                    self.period = "{:02d}:{:02d}".format(self.mins,self.sec)
                    self.sec = self.sec + 1
                    
                    if self.period == "10:00":
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame,"Completed",(500,200), font, 1,(0,255,0),2,cv2.LINE_AA)
                        #print("Completed")
                
                    self.time_left = 10 - self.mins

                    if len(str(self.time_left)) == 2:
                        time_left_str = self.time_left
                    
                    else:
                        time_left_str = "0" + str(self.time_left)

                    if self.i == 1:
                        if self.time_left == 1:
                            data = json.load(self.file)
                            data.update({"Total_seconds": 20, 
                                        "Timestamp": "00:00:10",
                                        "Total_Reps": "20 sec"})
                            self.file.seek(0)
                            json.dump(data, self.file)
                            self.file.close()

                            self.i += 1

                    font = cv2.FONT_HERSHEY_SIMPLEX

                    #print(period)
                    cv2.circle(frame, (30,680), 100, (255, 0, 0), 3)
                    cv2.putText(frame,str(time_left_str),(10,680), font, 2,(0,0,255),3,cv2.LINE_AA)
                
                else:
                    x, y = positions[25][1:]
        
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
                    cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)

                    #print("Keep your legs straight")

            else:
                x, y = positions[0][1:]
        
                cv2.circle(frame, (x, y), 5, (0, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x, y), 15, (0, 0, 255), 2)

                #print("Look Straight, instead looking down")

        return(frame)


       