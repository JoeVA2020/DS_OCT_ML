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
    #print(res.multi_hand_landmarks)
    tipids=[4,8,12,16,20]
    lmlist=[]
    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
               # print(id,lm)
                cx=lm.x # x coordinate landmarks are stored here
                cy=lm.y # y coordinate landmarks are stored here
                lmlist.append([id,cx,cy])
                # print(lmlist)
                if len(lmlist)!=0 and len(lmlist)==21: # counts the fingers if hand is vivible and all points are visible
                    fingercount=[]
                    # Thumb
                    
                    if lmlist[12][1] <lmlist[20][1]:    # LEFT HAND
                        if lmlist[4][1]>lmlist[3][1]:
                            fingercount.append(0)
                        else:
                            fingercount.append(1)
                    else:                               # RIGHT HAND
                        if lmlist[4][1] <lmlist[3][1]:
                            fingercount.append(0)
                        else:
                            fingercount.append(1)
                    
                    
                    # All fingers except thumb
                    for i in range(1,5): # tipid[1] = 8 Excluds thumb from loop
                        if lmlist[tipids[i]][2] > lmlist[tipids[i]-2][2]:   
                            fingercount.append(0)
                        else:
                            fingercount.append(1)
                            
                            
                    #print(sum(fingercount))
                    
                    if len(fingercount)!=0:
                        fingercount1=fingercount.count(1)
                    #print(fingercount1)
                    
                    cv2.putText(img,"Count: "+str(fingercount1),(35,400),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0),3)
        mpdrawing.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
            
    cv2.imshow("FINGERCOUNT",img)
    if cv2.waitKey(1)&0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()


#eneumarate : it is a function that will be useded to find the 
# tipid of the points and their respective 8y >

#  for 4 Fingers if y-Coordinate value 
#  for THUMB if x-cordinate value of 4x > 3x THUMB is CLOSED for one hand and 4x < 3x THUMB is CLOSED for the other.