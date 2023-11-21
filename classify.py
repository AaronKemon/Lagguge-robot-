#!/home/heng/anaconda3/envs/pytorch/bin/python
import sys

sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import re
import torch
import torch.nn as nn
import numpy as np
import mediapipe as mp
import torch.nn.functional as F
import rospy
import cv2
import math
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from classfy.msg import hand


mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands=mpHands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.7)

def cal_rela(coors):
    cx1=coors[0,0]
    cy1=coors[0,1]
    origin=np.float32([]).reshape(0,2)
    temp=np.array([[cx1,cy1]])
    for i in range(21):
        origin=np.append(origin,temp,axis=0)
    cx2=coors[5,0]
    cy2=coors[5,1]
    rx,ry=(cx2-cx1,cy1-cy2)
    l=math.sqrt(math.pow(rx,2)+math.pow(ry,2))
    cosr=rx/l
    sinr=ry/l
    rotatemat=np.mat([[cosr,0-sinr],[sinr,cosr]])
    newmat=coors-origin
    finalmat=np.float32([]).reshape(0,2)
    for i in range(21):
        pointxy=newmat[i].T
        newpointxy=rotatemat*pointxy
        finalmat=np.append(finalmat,newpointxy.T,axis=0)
    finalmat=200*finalmat/l
    finalmat=finalmat.astype(int)
    return finalmat

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("node", Image, callback)
    rospy.spin()


def callback(imgmsg):

    rate = rospy.Rate(20)
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
    cv2.imshow("listener", img)
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    hand_index=0
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:
            label = re.findall(r'"([^"]*)"', str(results.multi_handedness[hand_index]))[0]
            hand_index=hand_index+1
            if label!='Right':
                print("Left hand, invalid!")
                continue


            j=0
            originmat=np.float32([]).reshape(0,2)

            x1=10000
            y1=10000
            x2=0
            y2=0
            d1x=0
            d2x=0
            d1y=0
            d2y=0
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                if cx<x1:
                    x1=cx
                if cx>x2:
                    x2=cx
                if cy<y1:
                    y1=cy
                if cy>y2:
                    y2=cy
                if id==5:
                    d1x=cx
                    d1y=cy
                if id==8:
                    d2x=cx
                    d2y=cy
                if j!=id:
                    break

                originmat=np.append(originmat,np.mat([cx,cy]),axis=0)
                j=j+1
            cv2.rectangle(img,(x1,y1),(x2,y2),(100,100,100),5)
            dx = d2x - d1x
            dy = d2y - d1y


            finalmat=cal_rela(originmat)
            finalmat=finalmat.flatten()[0]
            #print(finalmat)
            finalmat = torch.tensor(finalmat).float()
            result=net(finalmat).data

            maxindex = np.argmax(result).item()
            print(maxindex)
            index=rospy.get_param("last_index")
            time=rospy.get_param("same_time")
            if maxindex!=index:
                rospy.set_param("last_index",maxindex)
                rospy.set_param("same_time",0)
            else:
                rospy.set_param("same_time",time+1)


            if time==20:
                cv2.putText(img, str(maxindex), (50, 50), font, 0.7, (0, 255, 0), 2)
                cv2.imshow("result", img)
                pub = rospy.Publisher('handmsg', hand, queue_size=10)

                msg = hand()
                msg.x1 = x1
                msg.y1 = y1
                msg.x2 = x2
                msg.y2 = y2
                msg.dx = dx
                msg.dy = dy
                msg.mark = maxindex

                pub.publish(msg)
                rospy.loginfo("this publish hand message;[ %d, %d, %d, %d,%d,%d,%d]",
                              msg.x1, msg.y1, msg.x2, msg.y2, msg.dx,msg.dy,msg.mark)
                rate.sleep()

            

    cv2.waitKey(3)

font = cv2.FONT_HERSHEY_SIMPLEX
test_data=np.loadtxt('test.txt',dtype=np.int16)
x_t=test_data[:,0:42]
x_t=torch.tensor(x_t).float()


class Net(torch.nn.Module):
    def __init__(self,n_feature,n_hidden,n_output):
        super(Net,self).__init__()
        self.hidden=torch.nn.Linear(n_feature,n_hidden)
        self.out=torch.nn.Linear(n_hidden,n_output)

    def forward(self,x):
        x=F.relu(self.hidden(x))
        x=self.out(x)
        return x

net=Net(n_feature=42,n_hidden=210,n_output=3)
net.load_state_dict(torch.load('model_params.pkl'))
rospy.set_param("same_time",0)
rospy.set_param("last_index",0)
listener()
