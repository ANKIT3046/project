import cv2
import numpy as np
import sqlite3
face_casecade=cv2.CascadeClassifier('classifier/haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
def insertOrUpdate(Id,Name):
    conn=sqlite3.connect('hellodata.db')
    cmd="SELECT * FROM hello WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE hello SET Name="+str(Name)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO hello(ID,Name) Values("+str(Id)+","+str(Name)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()
id=input('enter uniqe id:')
name=input('enter name: ')
insertOrUpdate(id,name)
cap=cv2.VideoCapture(0)
count=0
while(count<50):
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces=face_casecade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        
        frame=gray[y:y+h,x:x+w]
        cv2.imwrite("datasets/User."+str(id)+"."+str(count)+".jpg",frame)
        cv2.waitKey(300)
        cv2.imshow("CAPTURED PHOTO",frame)
        count=count+1
    cv2.imshow('Face recognition system capture faces',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print('face capture for subject is completed')
cap.release()
cv2.destroyAllWindows()

