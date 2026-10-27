#!/usr/bin/env python3
"""Configure F/T collision detection and rebound without sending motion commands.

Usage: python set_ft_collision_config.py [robot_ip]
Requires a UFACTORY F/T sensor and controller firmware >= 2.6.103.
Existing sensor load/zero compensation and control mode are used as-is.
Settings remain enabled after disconnect; readback does not verify collision response.
"""

import sys
import time
from configparser import ConfigParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from xarm.wrapper import XArmAPI

# SDK ranges: force 5..200 N, torque 0.1..4 Nm. 2 N is outside the documented range.
# DEFAULT_THRESHOLDS = [30, 30, 30, 0.0, 0.0, 0.0]
THRESHOLDS = [10, 10, 10, 3, 3, 3]
# SDK ranges: translation 2..500 mm, rotation 0.2..50 degrees.
# DEFAULT_REBOUND_DISTANCES = [10.0, 10.0, 10.0, 2.0, 2.0, 2.0]

REBOUND_DISTANCES = [2, 2, 2, 0.2, 0.2, 0.2]


def check_code(name, code):
    if code != 0:
        raise RuntimeError(f"{name} failed: code={code}")


config = ConfigParser()
config.read(Path(__file__).resolve().parents[1] / "robot.conf")
ip = sys.argv[1] if len(sys.argv) > 1 else config.get("xArm", "ip")

arm = XArmAPI(ip)
try:

    check_code("clean_error", arm.clean_error())
    time.sleep(1)
    check_code("motion_enable", arm.motion_enable(enable=True))
    time.sleep(1)
    check_code("set_ft_sensor_enable", arm.set_ft_sensor_enable(1))
    time.sleep(0.2)

    check_code("set_ft_collision_threshold", arm.set_ft_collision_threshold(THRESHOLDS))
    check_code(
        "set_ft_collision_reb_distance",
        arm.set_ft_collision_reb_distance(REBOUND_DISTANCES.copy(), is_radian=False),
    )
    check_code("set_ft_collision_rebound", arm.set_ft_collision_rebound(1))
    check_code("set_ft_collision_detection", arm.set_ft_collision_detection(1))

    code, enabled = arm.get_ft_collision_detection()
    check_code("get_ft_collision_detection", code)
    print("F/T collision detection:", enabled)

    code, rebound = arm.get_ft_collision_rebound()
    check_code("get_ft_collision_rebound", code)
    print("F/T collision rebound:", rebound)

    code, thresholds = arm.get_ft_collision_threshold()
    check_code("get_ft_collision_threshold", code)
    print("Thresholds [Fx, Fy, Fz, Tx, Ty, Tz] (N, N, N, Nm, Nm, Nm):", thresholds)

    code, distances = arm.get_ft_collision_reb_distance(is_radian=False)
    check_code("get_ft_collision_reb_distance", code)
    print("Rebound [x, y, z, Rx, Ry, Rz] (mm, mm, mm, deg, deg, deg):", distances)


    while arm.connected and arm.error_code == 0:
        print('raw_force: {}'.format([f'{x:.3f}' for x in arm.ft_raw_force]))
        print('exe_force: {}'.format([f'{x:.3f}' for x in arm.ft_ext_force]))
        # # get_ft_sensor_data() will get the last ext_force
        # code, ext_force = arm.get_ft_sensor_data()
        # if code == 0:
        #     print('exe_force: {}'.format(ext_force))
        time.sleep(0.5)


    print("Settings remain enabled after disconnect. No motion commands were sent.")
finally:
    arm.disconnect()
