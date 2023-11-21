#!usr/bin/python
# -*- coding: UTF-8 -*-+`

#++++++++++++++++++++++++++++++++++++++++++++++++++-
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD  # 当使用树莓派版本的mycobot时，可以引用这两个变量进行MyCobot初始化

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

# 检测机械臂是否可烧入程序
if mc.is_controller_connected() != 1:
    print("请正确连接机械臂进行程序写入")
    exit(0)

# 对机械臂进行微调，确保调整后的位置所有卡口都对齐了
# 以机械臂卡口对齐为准，这里给出的仅是个案例
mc.send_angles([0, 0, 0, 0, 0, 0], 20)

# 对此时的位置进行校准，校准后的角度位置表示[0,0,0,0,0,0]，电位值表示[2048,2048,2048,2048,2048,2048]
# 该for循环相当于set_gripper_ini()这个方法
for i in range(1, 7):
    mc.set_servo_calibration(i)
