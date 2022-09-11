import cv2
import face_recognition
import os


path = 'pic2'
imgs = []
myList = os.listdir(path)

for i in myList:
    img = cv2.imread(f'{path}/{i}')
    imgs.append(img)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def MaHoa(imgs):
    enCodeList = []
    for img in imgs:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enCode = face_recognition.face_encodings(img)
        enCodeList.append(enCode)
    return enCodeList

enCodeList = MaHoa(imgs)
print('Ma hoa thanh cong')

cap = cv2.VideoCapture(0)

while True:
    set, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face = face_recognition.face_locations(frame)
    encode = face_recognition.face_encodings(frame)

    if len(face) == 0 or len(encode) == 0:
        break
    KetQua1 = 0
    KetQua2 = 0
    for en in enCodeList:
        KQ = face_recognition.compare_faces(en, encode[0])
        if len(KQ) != 0:
            if str(KQ[0]) == 'True':
                KetQua1 += 1
            else:
                KetQua2 += 1
        SS = face_recognition.face_distance(en, encode[0])
        SaiSo = SS

    cv2.rectangle(frame, (face[0][3], face[0][0]), (face[0][1], face[0][2]), (255, 0, 255), 2)

    if KetQua1 >= KetQua2 and SaiSo < 0.4:
        frame = cv2.putText(frame, 'True', (face[0][3], face[0][2]+30), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 255), 2)
    else:
        frame = cv2.putText(frame, 'False', (face[0][3], face[0][2]+30), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 0), 2)

    cv2.imshow('ohshit', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()