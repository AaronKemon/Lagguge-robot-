#!usr/bin/python
# -*- coding: UTF-8 -*-+`

#++++++++++++++++++++++++++++++++++++++++++++++++++-
from pymycobot import PI_PORT, PI_BAUD  # 当使用树莓派版本的mycobot时，可以引用这两个变量进行MyCobot初始化
from pymycobot.mycobot import MyCobot
import time
import socket 


#open serve
address = ('192.168.137.76', 8888)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
s.bind(address)  
s.listen(5)  
  
ss, addr = s.accept()  
print 'got connected from',addr  
ss.send('connected')  
    
def gripper_test(mc):
    print("Start check IO part of api\n")
    # 检测夹爪是否正在移动
    flag = mc.is_gripper_moving()
    print("Is gripper moving: {}".format(flag))
    time.sleep(1)

    # Set the current position to (2048).
    # Use it when you are sure you need it.
    # Gripper has been initialized for a long time. Generally, there
    # is no need to change the method.
    # mc.set_gripper_ini()
    # 设置关节点7,让其转动到2048这个位置
    #mc.send_angle(7,-90,20)
    #time.sleep(3)
    #mc.send_angle(6,180,20)
    #time.sleep(3)
    #mc.set_gripper_value(4096,20)
    #time.sleep(2)
    # 设置六个关节位，让机械臂以20的速度转动到该位置
    #mc.set_encoders([2048,2048, 1024, 2048, 1024, 1024], 20)
    #time.sleep(3)
    
    # 设置夹爪的状态，让其以70的速度快速打开爪子
    mc.set_gripper_state(0, 70)
    time.sleep(3)
    mc.send_angles([90,0,0,70,0,0],20)
    time.sleep(3)
    # 获取关节点1的位置信息
    print(mc.get_encoder(1))
    print(mc.get_encoder(2))
    print(mc.get_encoder(3))
    print(mc.get_encoder(4))
    print(mc.get_encoder(5))
    print(mc.get_encoder(6))


    # 设置夹爪转动到2048这个位置
    #mc.set_encoder(7, 2048)
    #time.sleep(3)
    # 设置夹爪让其转到1300这个位置
    #mc.set_encoder(7, 1300)
    #time.sleep(3)
 
    # 以70的速度让夹爪到达2048状态
    #mc.set_gripper_value(2048, 70)
    #time.sleep(3)
    # 以70的速度让夹爪到达1500状态
    #mc.set_gripper_value(1500, 70)
    #time.sleep(3)
    # set angle to 3000
    #mc.set_gripper_value(3000,70)
    #time.sleep(3)
    # set angle to 0
    #mc.set_gripper_value(0,70)
    #time.sleep(3)
    
    #before grasp
    mc.send_angle(3,10,20)
    time.sleep(5)
    mc.set_encoder(7,0)
    print(mc.get_encoder(7))
    time.sleep(3)
    #after grasp, raise it,turn 90 degree 
    mc.send_angle(4,10,20)
    time.sleep(3)
    mc.send_angle(1,0,20)
    time.sleep(3)
    #mc.send_angle(5,10,20)
    #time.sleep(3)
    # 设置夹爪的状态，让其以70的速度快速收拢爪子
    mc.set_gripper_state(1, 70) 
    time.sleep(3)
    # mc.set_encoders([2048, 2048, 2048, 2048, 2048, 2048], 20)

    # 获取夹爪的值
    print("")
    print(mc.get_gripper_value())
    rc=ss.recv(1)
    print rc
    if rc=='0':
        #release it
        mc.send_angle(4,90,20)
        time.sleep(3)
        mc.set_gripper_state(0,70)
        time.sleep(2)
    
    


if __name__ == "__main__":
    # MyCobot 类初始化需要两个参数：
    #   第一个是串口字符串， 如：
    #       linux： "/dev/ttyUSB0"
    #       windows: "COM3"
    #   第二个是波特率：
    #       M5版本为： 115200
    #
    #   Example:
    #       mycobot-M5:
    #           linux:
    #              mc = MyCobot("/dev/ttyUSB0", 115200)
    #           windows:
    #              mc = MyCobot("COM3", 115200)
    #       mycobot-raspi:
    #           mc = MyCobot(PI_PORT, PI_BAUD)
    #
    # 初始化一个MyCobot对象
    # 下面为树莓派版本创建对象代码
    mc = MyCobot(PI_PORT, PI_BAUD)
    # 让其移动到零位
    mc.set_encoders([2048, 2048, 2048, 2048, 2048, 2048], 20)
    time.sleep(3)
    ra = ss.recv(512)
    print ra
    rb = ss.recv(512)  
    print rb 
    if ra=='1':
         str1=rb.split('-',3)
         print str1
         print str1[0]
         print str1[1]
         print str1[2]
         print str1[3]
         gripper_test(mc)
         ss.close()  
         s.close()  
    else:
        print ('waiting for command')
