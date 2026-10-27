from xarm.wrapper import XArmAPI
import time
arm = XArmAPI('192.168.1.244')

arm.clean_error()
time.sleep(1)
arm.motion_enable(enable=True)
time.sleep(2)
arm.set_ft_sensor_enable(True) # Enable the force torque sensor
arm.set_ft_collision_detection(True)    # Enable force torque collision detection
arm.set_ft_collision_rebound(True)      # Set rebound after force torque collision
arm.set_ft_collision_threshold([200, 200, 10, 2, 2, 0.4]) # Set Z-axis force threshold to 30N

time.sleep(0.5)

print("Start mode setting")
arm.set_mode(7)
arm.set_state(0)
arm.set_position(x=300, y=0, z=150, roll=180, pitch=0, yaw=0, speed=10, wait=True) # Move to initial position

code = arm.set_position(x=300, y=0, z=100, roll=180, pitch=0, yaw=0, speed=10, wait=False)

passed_time = 0
while True:
    print('raw_force: {}'.format([f'{x:.3f}' for x in arm.ft_raw_force]))
    print('exe_force: {}'.format([f'{x:.3f}' for x in arm.ft_ext_force]))

    time_duration = 0.5
    time.sleep(time_duration)
    passed_time +=0.5
    if passed_time > 20:
        break
    # if arm.has_err_warn:
    #     print("Error or warning detected, a collision may have occurred.")
    #     break


print("Collision detection example finished.")

time.sleep(1)
arm.clean_error()  # Clear the error
arm.set_ft_collision_detection(False) # Disable force torque collision detection