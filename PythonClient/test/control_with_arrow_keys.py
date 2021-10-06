import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import tkinter as tk


# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

state = client.getMultirotorState()
s = pprint.pformat(state)
print("state: %s" % s)

#airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
#client.moveToPositionAsync(-10, 10, -10, 5).join()
#airsim.wait_key('Press any key to takeoff')   
#-- Key event function

x = 0
y = 0
z = 0
altitude = 0

while(True):
    up = 0
    def key(event):
        if event.char == event.keysym: #-- standard keys
            if event.keysym == 't':   
                print("Taking off...")
                client.armDisarm(True)
                client.takeoffAsync().join()
            elif event.keysym == 'a':
                altitude += 1
                client.moveToPositionAsync(x, y, z, (altitude)).join()
                #altitude = altitude + 1 
            elif event.keysym == 'z':
                altitude -= 1
                client.moveToPositionAsync(x, y, z, (altitude)).join()
                print("key z %d, %d, %d, %d" % (x,y,z,altitude))

        else: #-- non standard keys
            if event.keysym == 'Up':
                x += 1
                client.moveToPositionAsync(x, y, z, (altitude)).join()
            elif event.keysym == 'Down':
                x -= 1
                client.moveToPositionAsync(x, y, z, (altitude)).join()
            elif event.keysym == 'Left':
                y += 1                
                client.moveToPositionAsync(x, y, z, (altitude)).join()
            elif event.keysym == 'Right':
                y -= 1         
                client.moveToPositionAsync(x, y, z, (altitude)).join()
    #---- MAIN FUNCTION
    
    #- Read the keyboard with tkinter

    root = tk.Tk()
    root.bind_all('<Key>', key)
    root.mainloop()
