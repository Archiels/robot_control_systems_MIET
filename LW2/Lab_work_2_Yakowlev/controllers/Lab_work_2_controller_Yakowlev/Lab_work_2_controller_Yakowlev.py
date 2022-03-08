"""Lab_work_2_controller_Yakowlev controller."""
from controller import Robot, DistanceSensor, Motor
from math import pi

robot = Robot() # Создаём объект класса Robot 

# Получить временной шаг для текущего мира симуляции
TIME_STEP = int(robot.getBasicTimeStep())

MAX_SPEED = 6.28 # Максимальная скорость вращения колеса (рад/с)
wheelRad = 0.0205
axleLength = 0.052

ps = [] # Создаём список для хранения имён датчиков
# Объявляем имена датчиков приближения
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i])) # Добавляем по очереди имя датчикам в список ps
    ps[i].enable(TIME_STEP) #Ждём один такт времени симуляции для установки каждого датчика

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

leftMotor.setPosition(float('inf')) # Разрешаем поворачиваться колесу на полный оборот
rightMotor.setPosition(float('inf')) # Аналогично для другого колеса
leftMotor.setVelocity(0.0) # Устанавливаем скорость вращения колеса 0 (рад/с)
rightMotor.setVelocity(0.0) # Аналогично для другого колеса

# Main loop: - бесконечный цикл
# - Выполняет шаги симуляции, пока Webots не остановит контроллер
def delay(delay_ms):
    control_time = robot.getTime()
    while robot.step(TIME_STEP) != -1:
    
        if robot.getTime() - control_time >= delay_ms * 10**(-3):
            break

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
    
while robot.step(TIME_STEP) != -1:
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    print(psValues)
    front_obstacle = psValues[0] > 150.0 or psValues[7] > 150.0
    leftSpeed = 0.5  * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
    if front_obstacle:
        break
while robot.step(TIME_STEP) != -1:
    #Считываем данные с датчиков
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    print(psValues) # Выводим значения с датчиков в монитор порта
    
    # Определяем, с какой стороны препятствие
    front_obstacle = psValues[0] > 150.0 or psValues[7] > 150.0
    left_obstacle = psValues[4] > 150.0 or psValues[5] > 150.0 or psValues[6] > 150.0

    if front_obstacle:
        turn_on_place(80, 50)
        leftSpeed = 0  * MAX_SPEED
        rightSpeed = 0 * MAX_SPEED
    else:
        if left_obstacle:
            leftSpeed = 0.6  * MAX_SPEED
            rightSpeed = 0.5 * MAX_SPEED
        else:
            leftSpeed = 0  * MAX_SPEED
            rightSpeed = 0.5 * MAX_SPEED
    # Устанавливаем скорость
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
    pass
