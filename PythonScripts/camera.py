'''
Scripts for detecting and moving leser
towards target

Created by: Tomas Hromada
  tomashromada1@gmail.com
Github: https://github.com/tomash1234/

See: https://www.youtube.com/watch?v=S3CwzkT6cK4
'''

import numpy as np
import cv2
import control
import time

class Target:

    def __init__(self):
        self.target = None
        self.candidate = (0, 0)
        self.confidence = 0
        self.is_found = False
        self.radius = 0
        self.aim_point = (0, 0)

    def new_loc(self, pos, radius):
        if (self.candidate[0] - pos[0])**2 + (self.candidate[1] - pos[1])**2 > 50:
            self.confidence = 0
            self.candidate = pos
        else:
            self.confidence += 1
            if self.confidence > 3:
                self.radius = radius
                self.is_found = True
                self.target = self.candidate

    def set_aim_point(self, pos):
        self.aim_point = pos

    def get_target(self):
        return self.target

    def move(self):
        self.is_found = False
        self.confidence = 0
    
    def get_laser(self):
        return self.aim_point

    def get_radius(self):
        return self.radius

class Gun:

    def __init__(self):
        self.rotate = 90
        self.pitch = 100
        self.confidence = 0
        self.loaded = True
        

    def move(self, target, recorder):
        if not target.is_found or target.confidence < 5:
            return
        target_pos = target.get_target()
        laser_pos = target.get_laser()
        x_len = (target_pos[0] -  laser_pos[0])**2
        if  x_len > 45:
            mult = 1
            if x_len > 70:
                mult = 2
            if target_pos[0] > laser_pos[0]:
                self.rotate -= 1 * mult
            else:
                self.rotate += 1 * mult
        
            control.rotate(self.rotate)
            target.move()
            
        if (target_pos[1] -  laser_pos[1])**2 > 100:
            if target_pos[1] > laser_pos[1]:
                self.pitch -= 1
            else:
                self.pitch += 1
        
            control.pitch(self.pitch)
            target.move()
            self.confidence = 0
        elif self.loaded:
            self.confidence += 1
            if self.confidence == 5:
                #aarecorder.start()
                pass
            if self.confidence > 10:
                self.loaded = False
                control.shotandreloade()
                

class Recorder:

    def __init__(self):
        self.recording = False
        self.startTime = 0
        self.buffer = []

    def start(self):
        self.recording = True
        self.startTime = time.time()
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = cv2.VideoWriter('shot_long.avi',fourcc, 15.0, (640,480))

    def frame_iter(self, frame):
        if not self.recording:
            return
        self.out.write(frame)

        if time.time() - self.startTime > 60:
            self.stop()
            
    def stop(self):
        self.out.release()
        

def detect_target(frame, target):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,60,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
    if circles is None:
        return frame
    
    for i in circles[0,:]:
        target.new_loc((i[0], i[1]), i[2])
        break

    
    return frame
    

def detect_dot(frame, target):
    ret,th1 = cv2.threshold(frame,220,255,cv2.THRESH_BINARY)
    th1 = cv2.cvtColor(th1, cv2.COLOR_BGR2GRAY)
    ret,th1 = cv2.threshold(th1,70,255,cv2.THRESH_BINARY)
    th1 = np.uint8(th1)
    contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxContour = 0
    maxContourData= None
    for contour in contours:
        contourSize = cv2.contourArea(contour)
        if contourSize > maxContour and contourSize < frame.shape[0]*frame.shape[1]/400:
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            maxContour = contourSize
            maxContourData = contour
            

    if maxContourData is None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray
    M = cv2.moments(maxContourData)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
	
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    frame = cv2.circle(frame, (cX, cY), 10, (0, 0, 255), (3))
    target.set_aim_point((cX, cY))

    # draw target
    target_pos = target.get_target()
    print('Laser detected at', cX, cY)
    
    if target_pos is not None:
        radius = target.get_radius()
        cv2.circle(frame,(target_pos[0], target_pos[1]), radius,(0,255,0),2)
        cv2.circle(frame,(target_pos[0], target_pos[1]),2,(0,0,255),3)
        print('Target detected at', (target_pos[0], target_pos[1]))

    return frame

cap = cv2.VideoCapture(0)

target = Target()
gun = Gun()
recorder = None
# recorder = Recorder()
# recorder.start()

while(True):
    ret, frame = cap.read()


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting framea
    detect_target(frame, target)
    mframe = detect_dot(frame, target)
    cv2.imshow('frame2', mframe)
    # recorder.frame_iter(mframe)
    gun.move(target, recorder)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

