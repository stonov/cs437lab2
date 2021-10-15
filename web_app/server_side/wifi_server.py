import socket
import picar_4wd as fc
import random
import json
from time import *
from threading import *

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"
SERVO_RIGHT = "SERVO_RIGHT"
SERVO_LEFT = "SERVO_LEFT"
UPDATE = "UPDATE"
IDLE = 0
STOP_INTERVAL = 0.1
HOST = "192.168.1.128" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
power_val = 50
distance_covered = 0.0
speed_cumlative = 0.0
speed_num = 0
avg_speed = 0.0
running = 1
speedometer: Thread = None
servo_angle = 0

def turn_servo(dir: int, at=18):
    global servo_angle

    if dir == 0:
        servo_angle = min(fc.max_angle, servo_angle + at)
    else:
        servo_angle = max(fc.min_angle, servo_angle - at)
    fc.servo.set_angle(servo_angle)

def speedometer_handler():
    global speed_num
    global speed_cumlative
    global avg_speed
    global distance_covered
    global running

    while running:
        first_speed = fc.speed_val()
        sleep(1)
        current_speed = fc.speed_val()
        distance_covered += ((first_speed + current_speed)/2) * 1

def fire_up_thread():
    global speedometer

    fc.start_speed_thread()
    speedometer = Thread(target=speedometer_handler)
    speedometer.start()

def process_data(data=""):
    global power_val

    if data != "":
        if data == FROWARD:
            fc.forward(power=power_val)
        elif data == BACKWARD:
            fc.backward(power=power_val)
        elif data == RIGHT:
            fc.turn_right(power=power_val)
        elif data == LEFT:
            fc.turn_left(power=power_val)
        elif data == SPEEDUP:
            power_val = min(100, power_val+10)
        elif data == SPEEDDOWN:
            power_val = max(10, power_val-10)
        elif data == SERVO_RIGHT:
            turn_servo(1)
        elif data == SERVO_LEFT:
            turn_servo(0)
        elif data == STOP:
            fc.stop()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
        s.listen()
        fc.servo.set_angle(servo_angle)
        fire_up_thread()
        print("Listening....")
        while 1:
            try:
                client, clientInfo = s.accept()
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                data = data.decode("utf-8")
                print("From {}: {}".format(clientInfo[0], data))
                process_data(data)
                direction = ""
                if data not in [STOP, SPEEDUP, SPEEDDOWN, UPDATE]:
                    direction = data.lower()
                power = str(round(fc.power_read(), 2)) + "V"
                speed_val = str(round(fc.speed_val(), 2)) + "cm/s"
                distance = str(round(distance_covered, 2)) + "cm"
                temp = str(round(fc.cpu_temperature(), 2)) + "C"
                ultra_val = str(round(fc.get_distance_at(0))) + "cm"
                servo_angle_val = str(servo_angle)
                ret_data = {
                    'direction': direction,
                    'power': power,
                    'speed': speed_val,
                    'distance': distance,
                    'temp': temp,
                    'ultra': ultra_val,
                    'servo': servo_angle_val
                }
                client.sendall(bytes(json.dumps(ret_data), "utf-8"))
            except Exception as e:
                print(e)
    except:
        print("Closing socket")
        fc.left_rear_speed.deinit()
        fc.right_rear_speed.deinit()
        speedometer.join()
        running = 0
        client.close()
        s.close()
