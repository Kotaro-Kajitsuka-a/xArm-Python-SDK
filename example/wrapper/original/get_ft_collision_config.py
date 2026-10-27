#!/usr/bin/env python3
"""Read F/T collision settings; only motion_enable changes robot settings.

Usage: python get_ft_collision_config.py [robot_ip]
Requires controller firmware >= 2.6.103.
"""

import sys
from configparser import ConfigParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from xarm.wrapper import XArmAPI


def check_code(name, code):
    if code != 0:
        raise RuntimeError(f"{name} failed: code={code}")


config = ConfigParser()
config.read(Path(__file__).resolve().parents[1] / "robot.conf")
ip = sys.argv[1] if len(sys.argv) > 1 else config.get("xArm", "ip")

arm = XArmAPI(ip)
try:
    check_code("motion_enable", arm.motion_enable(enable=True))

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
finally:
    arm.disconnect()
