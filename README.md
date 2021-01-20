# Auto-Targeting Nerf Turret

Here is the code used to create this project
 https://www.youtube.com/watch?v=S3CwzkT6cK4

[![Youtube video](https://img.youtube.com/vi/S3CwzkT6cK4/0.jpg)](https://www.youtube.com/watch?v=S3CwzkT6cK4)

Note: This code is not perfect. I did not want to publish it, but I got many requests to share this code.

## Hardware
See video
 * Wemos D1 Wifi
 * 3x Mini servo
 * Laser diod
 * Cheap webcam 
 * Nerf pistol

## Code
 * AutomaticGun/AutomaticGun.ino  - Arudino code
 * PythonScripts/control.py - Communication between computer and turret
 * PythonScripts/camera.py (main) - Detecting target and laser dot, moving turret towards the target - Run this code
 * PythonScripts/manual_control.py - For debugging purpose, Moving turret using WSAD and enter to shoot

## Detection & Targeting
 * The target must be a well visible fairly big circle
 * A circle is detected in the image, if center of circle is stable for few frames, turrets starts moving towards it
 * Laser dot should be small red dot
 * The script tries to get the laser dot into the circle
 * If the dot is inside the circle and close to the center for few frames, the trigger is pulled

## Communication
 * Communication between computer and Wemos d1 is implemented using UDP packets, computer and Wemos must be connect to the same network
 * Every packet contains 3 bytes - [**KEY=44**, **Action code**, **Value**]
 * Rotate (yaw) - [44, 120, [angle in degrees 0-180]]
 * Pitch - [44, 88, [angle in degrees 0-180]]
 * Reset the trigger - [44, 44, 0]
 * Pull the trigger - [44, 44, 64]


## Notes
 * key Q - quit
 * **class Recorder** in camera.py can be used for recording videos
 * Packages - Numpy and Opencv is required for this project

