'''
Script for turret testing.
You can manually move with turret
USe WASD and enter to shoot, q - quit

Created by: Tomas Hromada
  tomashromada1@gmail.com
Github: https://github.com/tomash1234/

See: https://www.youtube.com/watch?v=S3CwzkT6cK4
'''

import keyboard
import time
import autoshot

rotate = 90
pitch = 90
ANGLE_DIFF_PITCH = 0.5
ANGLE_DIFF_ROTATE = 1


while True:  # making a loop
    try:  
        if keyboard.is_pressed('q'):  
            print('Quit!')
            break
        if keyboard.is_pressed('a'):
            rotate = max(0, rotate - ANGLE_DIFF_ROTATE)
            autoshot.rotate(rotate)
        if keyboard.is_pressed('w'):
            pitch = min(180, pitch + ANGLE_DIFF_PITCH)
            autoshot.pitch(int(pitch))
        if keyboard.is_pressed('d'):
            rotate = min(180, rotate + ANGLE_DIFF_ROTATE)
            autoshot.rotate(rotate)
        if keyboard.is_pressed('s'):
            pitch = max(0, pitch - ANGLE_DIFF_PITCH)
            autoshot.pitch(int(pitch))
        if keyboard.is_pressed('enter'):
            autoshot.shotandreloade()
            
    except:
        break
    time.sleep(0.05)

camera.end()
