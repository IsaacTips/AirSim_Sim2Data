
# https://microsoft.github.io/AirSim/object_detection/
# https://data-make.tistory.com/170 폴더 만들기
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




def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


     
    
# 원본 이미지 저장
def save_scenery_orignal(image, filenames):
    print("save_scenery_original")
    #경로 C:\Users\sim\Documents\AirSim\datasets
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\datasets\\'
    #filepath =os.path.expanduser('~')+'\Documents\\AirSim\\scenery_orignal\\'
    
    createFolder(filepath)
    cv2.imwrite(filepath + filenames + '.jpg', image)

def save_yolo_label(list_cordinate, filenames):
    
    #경로 C:\Users\sim\Documents\AirSim\datasets
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\datasets\\'
    st=''
    for cordinate in list_cordinate:
        yolo_coord = polygon2yolo(cordinate[0],cordinate[1],cordinate[2],cordinate[3]) #욜로 변환

        yolo_coord = list(map(str,yolo_coord))
        st += '0 '+yolo_coord[0]+' '+yolo_coord[1]+' '+yolo_coord[2]+' '+yolo_coord[3]+'\n'
    createFolder(filepath)
    print(st)
        
    with open(filepath+filenames+'.txt', 'w', encoding='utf-8') as f:
       f.writelines(st[:-1])

    print("save_yolo_label")

#4개의 좌표 받아서 욜로 라벨형태로 반환
def polygon2yolo(x1,x2,y1,y2):
    
    yolo_list = []
    
    #cx = int((x1 + x2) / 2)
    #cy = int((y1 + y2) / 2)
    #w = int(y2 - y1)
    #h = int(x2 - x1)

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    w = (x2 - x1)
    h = (y2 - y1)
    

    norm_cx = float(cx / 3840)
    norm_cy = float(cy / 2160)
    norm_w = float(w / 3840)
    norm_h = float(h / 2160)
    
    yolo_list.extend([norm_cx, norm_cy, norm_w, norm_h])
    
    return yolo_list


# 원본에 bbox 적용된 이미지 저장  
def save_scenery_bbox(image, filenames):
    print("save_scenery_bbox")
    #경로 C:\Users\sim\Documents\AirSim\scenery_bbox
    filepath =os.path.expanduser('~')+'\Documents\\AirSim\\datasets_bbox\\'
    createFolder(filepath)
    
    cv2.imwrite(filepath + filenames + '.jpg', image)

def execute_detection():
    
    
    start_time = time.time() # 시작시간
    filenames = datetime.now().strftime("%Y%m%d-%H%M%S") + '_isaac_EF'

    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        print("이미지없음")
      
    else:

        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        people = client.simGetDetections(camera_name, image_type)
        
        list_cordinate = []
        if people:
            save_scenery_orignal(png, filenames) #원본이미지 저장
            for i,person in enumerate(people):

            
                personJSONData = json.dumps(person, indent=4, cls=DetectionEncoder) # str타입
               

         
           

                # cv2.rectangle => bbox
                # cv2.putText=> 식별자 이름
                cv2.rectangle(png,(int(person.box2D.min.x_val),int(person.box2D.min.y_val)),(int(person.box2D.max.x_val),int(person.box2D.max.y_val)),(255,0,0),2)
                cv2.putText(png, person.name, (int(person.box2D.min.x_val),int(person.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12))
 
                
                list_cordinate.append([]) #이중리스트 만들기
                list_cordinate[i].append(person.box2D.min.x_val)
                list_cordinate[i].append(person.box2D.max.x_val)
                list_cordinate[i].append(person.box2D.min.y_val)
                list_cordinate[i].append(person.box2D.max.y_val)


            save_yolo_label(list_cordinate,filenames ) # txt파일 저장
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
        filenames = datetime.now().strftime("%Y%m%d-%H%M%S") + '_isaac_EF'

        rawImage = client.simGetImage(camera_name, image_type)
        if not rawImage:
            continue
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        people = client.simGetDetections(camera_name, image_type)
        list_cordinate = []
        if people:
            save_scenery_orignal(png, filenames) #원본이미지 저장 (시작)

            for i,person in enumerate(people):
                #print(i,person)
                personJSONData = json.dumps(person, indent=4, cls=DetectionEncoder) # str타입

                # cv2.rectangle => bbox
                # cv2.putText=> 식별자 이름

                
                cv2.rectangle(png,(int(person.box2D.min.x_val),int(person.box2D.min.y_val)),(int(person.box2D.max.x_val),int(person.box2D.max.y_val)),(255,0,0),2)
                cv2.putText(png, person.name, (int(person.box2D.min.x_val),int(person.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (36,255,12))
                
                list_cordinate.append([]) #이중리스트 만들기
                list_cordinate[i].append(person.box2D.min.x_val)
                list_cordinate[i].append(person.box2D.max.x_val)
                list_cordinate[i].append(person.box2D.min.y_val)
                list_cordinate[i].append(person.box2D.max.y_val)


            save_yolo_label(list_cordinate,filenames ) # txt파일 저장
           
            save_scenery_bbox(png, filenames) #detection 저장
             
            
            png = cv2.resize(png, dsize=(640, 300))
            cv2.imshow("AirSim", png)
        
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('c'):
                client.simClearDetectionMeshNames(camera_name, image_type)
            elif cv2.waitKey(1) & 0xFF == ord('a'):
                client.simAddDetectionFilterMeshName(camera_name, image_type, "Person*")
            time.sleep(0.001)
            print("종료 :작업시간:{}".format(time.time() - start_time))  # (끝시간 - 시작 시간) 출력
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
        client.simSetDetectionFilterRadius(camera_name, image_type, 800 * 100) 
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


    
