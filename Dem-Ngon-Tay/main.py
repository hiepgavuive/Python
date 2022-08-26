import cv2
import os
import time
import hand as htm

pTime = 0
cap = cv2.VideoCapture(0)

folder = 'Fingers'
lst = os.listdir(folder)
lst_2 = []

for i in lst:
    img = cv2.imread(f'{folder}/{i}')
    print(f'{folder}/{i}')
    lst_2.append(img)

detector = htm.handDetector(detectionCon = 1)
daungontay = [4, 8, 12, 16, 20]

while True:
    set, frame = cap.read()

    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) != 0:
        duyet = 0

        if lmList[daungontay[0]][1] < lmList[daungontay[0]-1][1]:
            duyet = duyet + 1

        for i in range(1,5):
            if lmList[daungontay[i]][2] < lmList[daungontay[i]-2][2]:
                duyet = duyet + 1

        xet = duyet
        if duyet == 0:
            h, w, c = lst_2[5].shape
            frame[:h, :w] = lst_2[5]
        else:
            h, w, c = lst_2[xet-1].shape
            frame[:h, :w] = lst_2[xet-1]

        cv2.rectangle(frame, (0, 130), (110, 250), (0, 255, 0), -1)
        cv2.putText(frame, str(duyet), (19, 250), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0, 0), 5)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame, f'fps = {int(fps)}', (130, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 1)

    cv2.imshow('ohshit', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()