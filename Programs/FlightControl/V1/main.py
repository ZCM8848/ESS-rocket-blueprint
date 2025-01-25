from microbit import *
import Servo
from time import sleep
import math

# define math functions
def lerp(vec1, vec2, t):
    return t * vec2 + (1 - t) * vec1

def clamp(num, limit1, limit2):
    return max(min(num, max(limit1, limit2)), min(limit1, limit2))
    
def calibrate_accelerometer(duration=5000):
    """
    校准Micro:bit加速度计。
    :param duration: 校准时间，单位为毫秒，默认为5000毫秒（5秒）
    :return: 一个包含X、Y、Z三个方向偏移量的元组
    """
    print("开始校准，请将Micro:bit静止放置...")
    start_time = running_time()
    end_time = start_time + duration

    # 初始化数据存储
    x_values = []
    y_values = []
    z_values = []

    while running_time() < end_time:
        # 获取加速度读数
        x, y, z = accelerometer.get_values()
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)
        sleep(10)  # 每10毫秒读取一次，避免过快采样

    # 计算平均值
    offset_x = sum(x_values) / len(x_values)
    offset_y = sum(y_values) / len(y_values)
    offset_z = sum(z_values) / len(z_values)

    print("校准完成！")
    return offset_x, offset_y, offset_z

def vector_add(v1, v2):
    """
    向量加法
    :param v1: 第一个向量 (x1, y1, z1)
    :param v2: 第二个向量 (x2, y2, z2)
    :return: 结果向量 (x1+x2, y1+y2, z1+z2)
    """
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]

def vector_subtract(v1, v2):
    """
    向量减法
    :param v1: 第一个向量 (x1, y1, z1)
    :param v2: 第二个向量 (x2, y2, z2)
    :return: 结果向量 (x1-x2, y1-y2, z1-z2)
    """
    return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]

def vector_magnitude(v):
    """
    计算向量的模（长度）
    :param v: 向量 (x, y, z)
    :return: 向量的模
    """
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def vector_angle(v1, v2):
    """
    计算两个向量之间的夹角（以角度为单位）
    :param v1: 第一个向量 (x1, y1, z1)
    :param v2: 第二个向量 (x2, y2, z2)
    :return: 两个向量之间的夹角（角度制）
    """
    dot_product = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    magnitude_v1 = vector_magnitude(v1)
    magnitude_v2 = vector_magnitude(v2)
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0
    cosine_theta = dot_product / (magnitude_v1 * magnitude_v2)
    angle_radians = math.acos(cosine_theta)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees
  

# define PID controller
class PID:
    def __init__(self):
        self.d_prev = None
        self.i_prev = None
        self.p_prev = None
        self.result = None
        self.ep = True
        self.ei = True
        self.ed = True
        self.kp = 1
        self.ki = 0
        self.kd = 1
        self.sd = 0
        self.diff = 0
        self.integral = 0
        self.integral_limit = 1
        self.error_prev = 0
        self.first = True
        self.second = True
        self.dumpf = None

    def update(self, error, dt):
        if self.first:
            self.first = False
            self.error_prev = error
        elif self.second:
            self.second = False
            self.diff = (error - self.error_prev) / dt

        self.integral += error * dt * self.ki
        self.integral = clamp(self.integral, self.integral_limit, -self.integral_limit)
        self.diff = lerp(self.diff, (error - self.error_prev) / dt, 1 - self.sd)
        p = -error * self.kp
        i = -self.integral
        d = -self.diff * self.kd
        self.result = p * (1 if self.ep else 0) + i * (1 if self.ei else 0) + d * (1 if self.ed else 0)

        self.p_prev = p
        self.i_prev = i
        self.d_prev = d
        self.error_prev = error
        return self.result

# define servos
servo_LF = Servo.Servo(pin8)
servo_RF = Servo.Servo(pin9)
servo_LR = Servo.Servo(pin12)
servo_RR = Servo.Servo(pin13)

#initiate accelerometer
accelerometer.set_range(16)
offsets = calibrate_accelerometer(duration=5000)

pid_x = PID()
pid_y = PID()

pid_x.kp = 0.5
pid_x.kd = 0.1
pid_x.ki = 0.01
pid_x.integral_limit = 10

pid_y.kp = 0.5
pid_y.kd = 0.1
pid_y.ki = 0.01
pid_y.integral_limit = 10

neutral_angle = 90
servo_LF.angle(neutral_angle)
servo_RF.angle(neutral_angle)
servo_LR.angle(neutral_angle)
servo_RR.angle(neutral_angle)

alpha = 0.8
filtered_x = 0
filtered_y = 0
filtered_z = 0

while True:
    raw_x, raw_y, raw_z = accelerometer.get_values()
    raw_x -= offsets[0]
    raw_y -= offsets[1]
    raw_z -= offsets[2]

    filtered_x = alpha * filtered_x + (1 - alpha) * raw_x
    filtered_y = alpha * filtered_y + (1 - alpha) * raw_y
    filtered_z = alpha * filtered_z + (1 - alpha) * raw_z

    horizontal_acceleration_x = filtered_x
    horizontal_acceleration_y = filtered_y

    dt = 0.1

    correction_x = pid_x.update(horizontal_acceleration_x, dt)
    correction_y = pid_y.update(horizontal_acceleration_y, dt)

    servo_LF_angle = neutral_angle + correction_x - correction_y
    servo_RF_angle = neutral_angle - correction_x - correction_y
    servo_LR_angle = neutral_angle + correction_x + correction_y
    servo_RR_angle = neutral_angle - correction_x + correction_y

    servo_LF_angle = clamp(servo_LF_angle, 0, 180)
    servo_RF_angle = clamp(servo_RF_angle, 0, 180)
    servo_LR_angle = clamp(servo_LR_angle, 0, 180)
    servo_RR_angle = clamp(servo_RR_angle, 0, 180)

    servo_LF.angle(servo_LF_angle)
    servo_RF.angle(servo_RF_angle)
    servo_LR.angle(servo_LR_angle)
    servo_RR.angle(servo_RR_angle)

    # print(f"Raw Accel X: {raw_x}, Raw Accel Y: {raw_y}, Raw Accel Z: {raw_z}")
    # print(f"Filtered Accel X: {filtered_x}, Filtered Accel Y: {filtered_y}, Filtered Accel Z: {filtered_z}")
    # print(f"Correction X: {correction_x}, Correction Y: {correction_y}")
    # print(f"Servo LF: {servo_LF_angle}, Servo RF: {servo_RF_angle}, Servo LR: {servo_LR_angle}, Servo RR: {servo_RR_angle}")

    sleep(0.1)