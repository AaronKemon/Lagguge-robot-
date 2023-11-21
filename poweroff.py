#!usr/bin/python
# -*- coding: UTF-8 -*-+`

#++++++++++++++++++++++++++++++++++++++++++++++++++-
from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD  # 当使用树莓派版本的mycobot时，可以引用这两个变量进行MyCobot初始化

mc = MyCobot(PI_PORT, PI_BAUD)
mc.power_off()
mc.power_on()
