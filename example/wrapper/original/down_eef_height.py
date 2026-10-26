#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: cartesian online trajectory planning mode
"""
MAX_SPEED = 20
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)


# set mode: cartesian online trajectory planning mode
# the running command will be interrupted when the next command is received
arm.set_mode(7)
arm.set_state(0)
time.sleep(1)


# ToDo: ここで、最初の姿勢から全く動かないコードを書く。下の位置を書き換えるだけでいい。
# "speed = 10" means, 10 mm/s 

speed = 3
speed = max(speed, MAX_SPEED)

# here is the default rmb initial robot joints: x=325.564, y=-1.945497, z=124.241219, roll=179.0, pitch=-0.0106, yaw=0.809589
arm.set_position(x=325.564, y=-1.945497, z=124.241219, roll=179.0, pitch=-0.0106, yaw=0.809589, speed=20, is_radian=False, wait=True)


time.sleep(5)

for i in range(100):
    # run on mode(7)
    z_height = 124.241219 - i*10.0
    # the running command will be interrupted, and run the new command
    arm.set_position(x=325.564, y=-1.945497, z=z_height, roll=179.0, pitch=-0.0106, yaw=0.809589, speed=speed, is_radian=False, wait=True)
    time.sleep(2)
    # the running command will be interrupted, and run the new command
    print(f"i: {i}, z_height:{z_height}")


arm.set_state(0)
arm.disconnect()
