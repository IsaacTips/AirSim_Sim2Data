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
import msvcrt

# subclass JSONEncoder
class DetectionEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__





     
    
# 원본 이미지 저장
def save_scenery_orignal(image, filenames):
    print("save_scenery_original")
    #경로 C:\Users\sim\Documents\AirSim\scenery_original
    #경로에 폴더 따로 생성해야됨(추후 생성 코드작성할 것임)
    #filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_original\\'
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_orignal\\'
    
    cv2.imwrite(filepath + filenames + '.jpg', image)

#  bbox 좌표 JSON 저장
def save_scenery_label(s, filenames):
    print("save_scenery_label")
    #경로 C:\Users\sim\Documents\AirSim\scenery_label
    #경로에 폴더 따로 생성해야됨(추후 생성 코드작성할 것임)
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_label\\'
    
    with open(filepath+filenames+'.json', 'w', encoding='utf-8') as f:
        f.write(s)



# 원본에 bbox 적용된 이미지 저장  
def save_scenery_bbox(image, filenames):
    print("save_scenery_bbox")
    #경로 C:\Users\sim\Documents\AirSim\scenery_bbox
    #경로에 폴더 따로 생성해야됨(추후 생성 코드작성할 것임)
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_bbox\\'
    
    cv2.imwrite(filepath + filenames + '.jpg', image)


def execute_detection():
    
    
    start_time = time.time() # 시작시간
    filenames = datetime.now().strftime("%Y%m%d-%H%M%S")

    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        print("이미지없음")
      
    else:

        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        people = client.simGetDetections(camera_name, image_type)
        if people:
            for person in people:

            
                personJSONData = json.dumps(person, indent=4, cls=DetectionEncoder) # str타입
               

                save_scenery_label(personJSONData, filenames) # JSON파일 저장
                print("--------------------------json저장:{}".format(time.time() - start_time))
                save_scenery_orignal(png, filenames) #원본이미지 저장
                print("--------------------------원본저장:{}".format(time.time() - start_time)) 
           

                # cv2.rectangle => bbox
                # cv2.putText=> 식별자 이름
                cv2.rectangle(png,(int(person.box2D.min.x_val),int(person.box2D.min.y_val)),(int(person.box2D.max.x_val),int(person.box2D.max.y_val)),(255,0,0),2)
                cv2.putText(png, person.name, (int(person.box2D.min.x_val),int(person.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12))
            save_scenery_bbox(png, filenames) #detection 저장
            
            png = cv2.resize(png, dsize=(540, 300))
            cv2.imshow("AirSim", png)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("원래는 continue")
            elif cv2.waitKey(1) & 0xFF == ord('c'):
                 client.simClearDetectionMeshNames(camera_name, image_type)
            elif cv2.waitKey(1) & 0xFF == ord('a'):
                client.simAddDetectionFilterMeshName(camera_name, image_type, "Person*")
            print(time.time() - start_time)  # (끝시간 - 시작 시간) 출력

        else:
             print("사람 없음")
      
        #cv2.destroyAllWindows() 

def execute_auto_detection():
    while True:
        print("시작")
        
        
        start_time = time.time() # 시작시간
        filenames = datetime.now().strftime("%Y%m%d-%H%M%S")

        rawImage = client.simGetImage(camera_name, image_type)
        if not rawImage:
            continue
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        people = client.simGetDetections(camera_name, image_type)
        if people:
            for person in people:

            
                personJSONData = json.dumps(person, indent=4, cls=DetectionEncoder) # str타입


                save_scenery_label(personJSONData, filenames) # JSON파일 저장
                print("--------------------------json저장:{}".format(time.time() - start_time))
                save_scenery_orignal(png, filenames) #원본이미지 저장
                print("--------------------------원본저장:{}".format(time.time() - start_time)) 

                # cv2.rectangle => bbox
                # cv2.putText=> 식별자 이름
                cv2.rectangle(png,(int(person.box2D.min.x_val),int(person.box2D.min.y_val)),(int(person.box2D.max.x_val),int(person.box2D.max.y_val)),(255,0,0),2)
                cv2.putText(png, person.name, (int(person.box2D.min.x_val),int(person.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12))
             
            save_scenery_bbox(png, filenames) #detection 저장
                
            png = cv2.resize(png, dsize=(640, 300))
            cv2.imshow("AirSim", png)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('c'):
                client.simClearDetectionMeshNames(camera_name, image_type)
            elif cv2.waitKey(1) & 0xFF == ord('a'):
                client.simAddDetectionFilterMeshName(camera_name, image_type, "Person*")
            
            print("종료")
            print(time.time() - start_time)  # (끝시간 - 시작 시간) 출력
            time.sleep(1.5)
        else:
            print("Person 없음")
        
       
        





      


        


if __name__ == '__main__':


    while(True):
    


        print("(1).image 수동 저장  (2)자동 저장(1.5초간격)  (3).종료 ")
        input = msvcrt.getwch()


        # connect to the AirSim simulator
        client = airsim.VehicleClient()
        client.confirmConnection()

        # set camera name and image type to request images and detections
        camera_name = "0"
        image_type = airsim.ImageType.Scene

        # set detection radius in [cm]
        client.simSetDetectionFilterRadius(camera_name, image_type, 500 * 500) 
        # add desired object name to detect in wild card/regex format
        client.simAddDetectionFilterMeshName(camera_name, image_type, "Person*") 


        #state = True # True : 실행,  False 실행중지



        if(input == "1"):
            execute_detection()
        elif(input == "2"):
            print('자동 저장')
            execute_auto_detection()
        elif(input == "3"):
            tmp=''
            print("종료(1), 다시실행(2)")
            tmp = msvcrt.getwch()
            if(tmp == '1'):
                break
            elif(tmp == '2'):
                continue


    