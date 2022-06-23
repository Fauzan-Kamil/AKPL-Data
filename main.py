#Start Library
from importlib.resources import path
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
#End Library

#Start Pengenalan data wajah
path="data"
images=[]
name=[]
myList=os.listdir(path)
print("\nLoading....\n")
#print(myList)
for person in myList:
    Image=cv2.imread(f"{path}/{person}")
    #cv2.imshow("Foto",Image)
    #cv2.waitKey(0)
    images.append(Image)
    name.append(os.path.splitext(person)[0])
#print(images)
#print(name)
#End Pengenalan data wajah

#Start Training Wajah
def findEncodings(images):
    encodeList=[]
    #Perulangan untuk mengambil data wajah
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeKnownImage=findEncodings(images)
#print(encodeKnownImage)
print("\nPresensi Berhasil Dijalankan....\n")
#End Training Wajah

#Start Reporting / Laporan presensi
def markAttendance(name):
    with open('laporan.csv','r+') as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dtString=now.strftime('%H:%M:%S')
            dtTanggal=now.strftime('%Y-%b-%d')
            f.writelines(f'\n{name},{dtString},{dtTanggal}')
#End Reporting / Laporan presensi

#Start Akses Webcam dan Identifikasi Wajah
cap=cv2.VideoCapture(0)
#cap.set(3,1080)
#cap.set(4,580)
while True:
    succes,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    facescurFrame=face_recognition.face_locations(imgS)
    encodecurFrame=face_recognition.face_encodings(imgS,facescurFrame)
    for encodeFace,FaceLoc in zip(encodecurFrame,facescurFrame):
        #Start Face Recognition
        matches=face_recognition.compare_faces(encodeKnownImage,encodeFace)
        #name="Unknown"
        faceDis=face_recognition.face_distance(encodeKnownImage,encodeFace)
        #print(faceDis)
        matchIndex=np.argmin(faceDis)
        if matches[matchIndex]:
            #name=name[matchIndex]
            Identity=name[matchIndex]
        #else:
            #name="Unknown"
            # print(Identity)
        #End Face Recognition
    
        #print(FaceLoc)
            y1,x2,y2,x1=FaceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            #Bounding Box
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),3)
            #Start Nama User
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),2,cv2.FILLED)
            cv2.putText(img,Identity,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            #Data User Di Laporan
            markAttendance(Identity)
            #End Nama User 
#End Akses Webcam dan Identifikasi Wajah
    cv2.imshow("Presensi Face Recogniton Untuk Siswa",img)
    #cv2.waitKey(1)
    #=========================================
    #if cv2.waitKey(0) & 0xFF ==ord('k'):
    #    break
    #cap.release()
    #cv2.destroyAllWindows()
    #=========================================
    k = cv2.waitKey(30) & 0xff
    if k == 27: # tekan 'ESC' buat keluar
        break
cap.release()
cv2.destroyAllWindows()
#'''
#End Akses Webcam

#Jika data user tidak ada di data base, maka user tidak dapat melakukan presensi 
# atau tidak muncul rectangle di wajah user
