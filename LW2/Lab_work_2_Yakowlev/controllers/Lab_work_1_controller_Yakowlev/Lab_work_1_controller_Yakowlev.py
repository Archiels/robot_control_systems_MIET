"""Lab_work_1_controller_Yakowlev controller."""

from controller import Robot
from math import pi

robot = Robot()

MAX_SPEED = 6.28
wheelRad = 0.0205
axleLength = 0.052

timestep = int(robot.getBasicTimeStep())

def delay(delay_ms):
    control_time = robot.getTime()
    while robot.step(timestep) != -1:
    
        if robot.getTime() - control_time >= delay_ms * 10**(-3):
            break

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

def stop():
    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)

def move_fwd(s, koef):
    t = s / (koef / 100 * MAX_SPEED * wheelRad)
    leftMotor.setVelocity(koef / 100 * MAX_SPEED)
    rightMotor.setVelocity(2 * koef / 100 * MAX_SPEED)
    delay(t * 1000)
    stop()

def turn_on_place(angle, koef):
    t = abs(angle) * axleLength * pi / (3.6 * wheelRad * koef * MAX_SPEED)
    velocity = koef * MAX_SPEED / 100
    if angle < 0:
        leftMotor.setVelocity(-velocity)
        rightMotor.setVelocity(velocity)
    else:
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(-velocity)
    delay(1000 * t)
    stop()
 
def turn_circle_1 (R, koef):
    t = (1.1 * 2 * pi * R) / (koef / 100 * MAX_SPEED * wheelRad) #1.1 добавил из-за погрешности поворота
    velocity = (koef / 100) * MAX_SPEED
    in_velocity = ((R - (axleLength / 2)) /  R) * velocity
    out_velocity = ((R + (axleLength / 2)) /  R) * velocity
    if R < 0:
        leftMotor.setVelocity(out_velocity)
        rightMotor.setVelocity(in_velocity)
    else:
        leftMotor.setVelocity(in_velocity)
        rightMotor.setVelocity(out_velocity)
    delay(1000 * t)
    stop()
    
turn_circle_1 (0.3, 75)

t = robot.getTime()
delay(1000)
print(robot.getTime() - t, 'seconds')

while robot.step(timestep) != -1:
    pass