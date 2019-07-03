import cv2,os
import numpy as np
#from PIL import Image
#import pickle
import sqlite3
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainningData1.yml')
casecadePath='classifier/haarcascade_frontalface_default.xml'
faceCascade=cv2.CascadeClassifier(casecadePath)
#path='datasets'
def getProfile(id):
    conn=sqlite3.connect('FaceBase.db')
    cmd="SELECT * FROM people WHERE ID= "+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
cam=cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_SIMPLEX
while(True):
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        id,conf=recognizer.predict(gray[y:y+h,x:x+w])
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(img, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.rectangle(img, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
        #cv2.putText(img, str("ankit"), (x,y-40), font, 1, (255,255,255), 3)
        print(id)

        profile=getProfile(id)
        if(profile!=None):
            cv2.putText(img,str('Name: '+profile[1]+'  {0:.2f}%'.format(round(100-conf),2)),(x,y-75),font,0.5,(255,255,255),2)
            cv2.putText(img,str('Age: '+str(profile[2])),(x,y-60),font,0.5,(255,255,255),1)
            cv2.putText(img,str('Sex: '+str(profile[3])),(x,y-45),font,0.5,(255,255,255),1)
            cv2.putText(img,str(profile[4]),(x,y),font,1,(0,0,255),3)
    cv2.imshow('Face',img);
    if cv2.waitKey(10) & 0xff==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
