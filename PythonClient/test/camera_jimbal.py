import socket 
import struct # 패킷 b 로 시작하는건 실제 네트워크 스트림에 사용하는 데이터가 파이썬에 맞지 않음. C에서 api 가져와야함.
from math import pi
#import setup_path
import airsim

import pprint
import os
import time
import math
import tempfile
    
client = airsim.VehicleClient()
client.confirmConnection()

localIP = "172.31.32.1" 
localPort = 8500
bufferSize = 1024

# 데이터그램 소켓을 생성 
# 
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

count = 0

temp_cmd_pitch = 0.0
temp_cmd_roll = 0.0
temp_cmd_yaw = 0.0

while(True): 
    data, bytesAddressPair = UDPServerSocket.recvfrom(bufferSize) 
    #length = int.from_bytes(bytesAddressPair, "little")
    #data = UDPServerSocket.recv(length)

    address = bytesAddressPair[0] 
    port = bytesAddressPair[1] 
    clientMsg = "IP Address:{}".format(address) 
    clientIP = "port:{}".format(port) 
    data_print = "data :{}".format(data) 
    
    #print(clientMsg) 
    #print(clientIP) 
    #print("received {} bytes {}".format(len(data), list(map(hex,data)))) 
    
    pitch_angle = data[:4]
    roll_angle = data[4:8]
    yaw_angle = data[8:12]
    zoom = data[12:13]

    #radian_to_degree = 57.3
    roll_angle_f = float(str((struct.unpack('f', pitch_angle))[0])) * 0.018 * 180/pi  # 0.018 resolution
    pitch_angle_f = float(str((struct.unpack('f', roll_angle))[0])) * 0.018 * 180/pi
    yaw_angle_f= float(str((struct.unpack('f', yaw_angle))[0])) * 0.018 * 180/pi

    if((pitch_angle_f>3.0) or (pitch_angle_f<-3.0)):
        if(temp_cmd_pitch>60):
            temp_cmd_pitch = 60
            #temp_cmd_pitch = temp_cmd_pitch + pitch_angle_f
        elif(temp_cmd_pitch<-60):
            temp_cmd_pitch = -60
            #temp_cmd_pitch = temp_cmd_pitch + pitch_angle_f
        else:
            temp_cmd_pitch = temp_cmd_pitch + pitch_angle_f*0.001

    if((roll_angle_f>2.0) or (roll_angle_f<-2.0)):
        if(temp_cmd_roll>40):
            temp_cmd_roll = 40
            #temp_cmd_roll = temp_cmd_roll + roll_angle_f
        elif(temp_cmd_roll<-40):
            temp_cmd_roll = -40
            #temp_cmd_roll = temp_cmd_roll + roll_angle_f
        else:
            temp_cmd_roll = temp_cmd_roll + roll_angle_f*0.001

    if((yaw_angle_f>2.0) or (yaw_angle_f<-2.0)):
        if(temp_cmd_yaw>359):
            temp_cmd_yaw = 359
            #temp_cmd_roll = temp_cmd_roll + roll_angle_f
        elif(temp_cmd_yaw<-359):
            temp_cmd_yaw = -359
            #temp_cmd_roll = temp_cmd_roll + roll_angle_f
        else:
            temp_cmd_yaw = temp_cmd_yaw + yaw_angle_f*0.001


    if ((count % 100) == 0):
        print(pitch_angle_f)
        print(temp_cmd_pitch)
        print(yaw_angle_f)
        print('-----------')
        count = count+1
    else:
        count = count+1

    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(math.radians(temp_cmd_pitch), math.radians(temp_cmd_roll), math.radians(temp_cmd_yaw))) #radians

    client.simSetCameraPose("0", camera_pose)

    #airsim.wait_key('Press any key to set camera-0 gimbal to 15-degree pitch')

    
    #print(type(yaw_angle_f))
    #yaw_angel_f = float(str(yaw_angle[0]))
    #print(type(yaw_angel_f))
    #print(yaw_angel_f)

    # Sending a reply to client 
    #UDPServerSocket.sendto(bytesToSend, address)
    