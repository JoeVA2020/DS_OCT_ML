import cv2
import mediapipe as mp

mphands=mp.solutions.hands
mpdrawing=mp.solutions.drawing_utils

hand=mphands.Hands(max_num_hands=1)

video=cv2.VideoCapture(1)
while True:
    suc,img=video.read()
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=hand.process(img1)
    tipids = [4,8,12,16,20]
    lmlist = []

    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                cx, cy = lm.x, lm.y
                lmlist.append([id, cx, cy])

            if len(lmlist) != 0 and len(lmlist) == 21:
                fingercount = []

                # Thumb
                if lmlist[12][1] < lmlist[20][1]:  # LEFT HAND
                    fingercount.append(1 if lmlist[4][1] < lmlist[3][1] else 0)
                else:                              # RIGHT HAND
                    fingercount.append(1 if lmlist[4][1] > lmlist[3][1] else 0)

                # Other four fingers
                for i in range(1, 5):
                    fingercount.append(1 if lmlist[tipids[i]][2] < lmlist[tipids[i] - 2][2] else 0)

                # Interpret gestures
                if sum(fingercount) == 5:
                    cv2.putText(img, "Open Hand", (35,400), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 3)
                elif sum(fingercount) == 0:
                    cv2.putText(img, "Closed Fist", (35,400), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 3)
                elif fingercount[0] == 1 and fingercount[1] == 1 and sum(fingercount[2:]) == 0:
                    if lmlist[8][2] < lmlist[6][2]:
                        cv2.putText(img, "Pointing Up", (35,400), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 3)
                    elif lmlist[8][2] > lmlist[6][2]:
                        cv2.putText(img,"Pointing down",(35,400),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),3)
                elif fingercount[1] == 1 and fingercount[2] == 1 and sum(fingercount) == 2:
                    if lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2]:
                        cv2.putText(img, "Victory", (35,400), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 3)
                elif fingercount[0] == 1 and sum(fingercount) == 1:
                    if lmlist[4][2] < lmlist[0][2] and lmlist[4][1] < lmlist[6][1]:
                        cv2.putText(img, "Thumbs Up", (35,400), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 3)
                else:
                    cv2.putText(img, "None", (35,400), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 3)

                        
        mpdrawing.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
            
    cv2.imshow("FINGERCOUNT",img)
    if cv2.waitKey(1)&0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
