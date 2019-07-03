import cv2
import sqlite3
cam=cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('classifier/haarcascade_frontalface_default.xml')

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect('FaceBase.db')
    cmd="SELECT * FROM people WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0=
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE people SET Name="+str(Name)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO people(ID,Name) Values("+str(Id)+","+str(Name)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()
id=input('enter uniqe id:')
name=input('enter name: ')
insertOrUpdate(id,name)
sampleNo=0
while(True):
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        sampleNo=sampleNo+1
        cv2.imwrite('datasets/User'+str(id)+"."+str(sampleNo)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(100);
    cv2.imshow('Face',img)
    cv2.waitKey(1);
    if(sampleNo>30):
        break

cam.release()
cv2.destroyAllWindows()
