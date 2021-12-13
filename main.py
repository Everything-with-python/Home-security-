import cv2
import imutils
import time 
from datetime import datetime
import requests                                                                                                                                                                                                                                                        
import json
from twilio.rest import Client
import os

cam=cv2.VideoCapture(0)

firstFrame=None
area=800
guy = 0

def sendSMS():
    url = "https://www.fast2sms.com/dev/bulk"
    my_data = { 'sender_id': 'FSTSMS',  
                              'message': "Alert : Someone has entered into our house",                  
                              'language': 'english', 
                              'route': 'p', 
                              'numbers': ************} 
    headers = { 'authorization': '***********',   
                            'Content-Type': "application/x-www-form-urlencoded", 
                            'Cache-Control': "no-cache"}
    response = requests.request("POST", url, data = my_data, headers = headers) 
    returned_msg = json.loads(response.text) 

def sendIMG():
    client = Client()
    sender = "whatsapp:+91***********"
    receiver = "whatsapp:+91***********"
    msg = client.messages.create(body = "Alert : Someone has entered into our house. He is the guy buddy",
                                                                     media_url = "thief.jpg",
                                                                     from_ = sender,
                                                                     to = receiver)
    
while True:
    image=cam.read()[1]
    text="Normal"
    image=imutils.resize(image,width=850)
    grayImg=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    grayImg=cv2.GaussianBlur(grayImg,(21,21),0)
    if firstFrame is None:
        firstFrame=grayImg
        continue
    imgDiff=cv2.absdiff(firstFrame,grayImg)
    threshImg=cv2.threshold(grayImg,150,255,cv2.THRESH_BINARY)[1]
    threshImg=cv2.dilate(threshImg,None,iterations=2)
    cnts=cv2.findContours(threshImg.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c)<area:
            continue
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
        text="Moving Object Detected"
    cv2.putText(image,text,(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4)
    cv2.imshow("Detector",image)
    key = cv2.waitKey(1) & 0XFF
    if key == 13:
        break
    print(text)
    if text == "Moving Object Detected":
        cv2.imwrite("thief.jpg", image)
        guy += 1
        break

cam.release()
cv2.destroyAllWindows()

if text == "Moving Object Detected":
    sendSMS()
    sendIMG()
    os.remove("thief.jpg")
