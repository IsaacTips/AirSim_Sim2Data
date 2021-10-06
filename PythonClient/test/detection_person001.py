# https://microsoft.github.io/AirSim/object_detection/
import setup_path 
import airsim
import cv2
import numpy as np 
import pprint
import time
import os.path
from datetime import datetime
import json
from json import JSONEncoder
import time
from time import strftime # 시간복잡도 확인

# subclass JSONEncoder
class DetectionEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__



def save_scenery_label(s):
    print("save_scenery_label")
    #경로 C:\Users\sim\Documents\AirSim\scenery_label
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_label\\'
    filenames = datetime.now().strftime("%Y%m%d-%H%M%S")

    with open(filepath+filenames+'.json', 'w', encoding='utf-8') as f:
        f.write(s)




        
    

def save_scenery_orignal(image):
    print("save_scenery_original")
    #경로 C:\Users\sim\Documents\AirSim\scenery_original
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_original\\'
    filenames = datetime.now().strftime("%Y%m%d-%H%M%S")
    cv2.imwrite(filepath + filenames + '.jpg', image)


  
def save_scenery_bbox(image):
    print("save_scenery_bbox")
    #경로 C:\Users\sim\Documents\AirSim\scenery_bbox
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_bbox\\'
    filenames = datetime.now().strftime("%Y%m%d-%H%M%S")
    cv2.imwrite(filepath + filenames + '.jpg', image)






# connect to the AirSim simulator
client = airsim.VehicleClient()
client.confirmConnection()

# set camera name and image type to request images and detections
camera_name = "0"
image_type = airsim.ImageType.Scene

# set detection radius in [cm]
client.simSetDetectionFilterRadius(camera_name, image_type, 200 * 200) 
# add desired object name to detect in wild card/regex format
client.simAddDetectionFilterMeshName(camera_name, image_type, "Person*") 


while True:
    start_time = time.time() # 시작시간

    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        continue
    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
    people = client.simGetDetections(camera_name, image_type)
    if people:
        for person in people:

            
            personJSONData = json.dumps(person, indent=4, cls=DetectionEncoder) # str타입
            print(personJSONData)
            #print("personJSONData타입{}".format(type(personJSONData)))
            #save_scenery_label(personJSONData)

            save_scenery_label(personJSONData)

           
            #print(type(person)) =><class 'airsim.types.DetectionInfo'>
            #s = pprint.pformat(person) #=> 한줄로 된 josn파일 보여줌
            #print(s)


            # cv2.rectangle => bbox
            # cv2.putText=> 식별자 이름
            cv2.rectangle(png,(int(person.box2D.min.x_val),int(person.box2D.min.y_val)),(int(person.box2D.max.x_val),int(person.box2D.max.y_val)),(255,0,0),2)
            cv2.putText(png, person.name, (int(person.box2D.min.x_val),int(person.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12))
            
     

                
    # 한줄 추가
    #png = cv2.resize(png, dsize=(640, 300))
    cv2.imshow("AirSim", png)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        client.simClearDetectionMeshNames(camera_name, image_type)
    elif cv2.waitKey(1) & 0xFF == ord('a'):
        client.simAddDetectionFilterMeshName(camera_name, image_type, "Person*")
    png
    print(time.time() - start_time)  # (끝시간 - 시작 시간) 출력
    
cv2.destroyAllWindows() 


