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
UPDATE = "UPDATE"
IDLE = 0
STOP_INTERVAL = 0.1
HOST = "192.168.1.128" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
speed = 50
distance_covered = 0.0
speed_cumlative = 0.0
speed_num = 0
avg_speed = 0.0
running = 1
speedometer: Thread = None

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

    speedometer = Thread(target=speedometer_handler)
    speedometer.start()

def process_data(data=""):
    global speed

    if data != "":
        if data == FROWARD:
            print("moving forward")
            fc.forward(power=speed)
        elif data == BACKWARD:
            print("moving backward")
            fc.backward(power=speed)
        elif data == RIGHT:
            print("moving right")
            fc.turn_right(power=speed)
        elif data == LEFT:
            print("moving left")
            fc.turn_left(power=speed)
        elif data == STOP:
            print("stopping")
            fc.forward(IDLE)
        elif data == SPEEDUP:
            print("speeding up")
            speed = min(100, speed+10)
        elif data == SPEEDDOWN:
            print("slowing down")
            speed = max(10, speed-10)
        else:
            print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    fc.start_speed_thread()
    fire_up_thread()
    print("Listening....")
    try:
        while 1:
            try:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                data = data.decode("utf-8")
                process_data(data)
                direction = ""
                if data not in [STOP, SPEEDUP, SPEEDDOWN, UPDATE]:
                    direction = data.lower()
                power = str(round(fc.power_read(), 2)) + "V"
                speed = str(round(fc.speed_val(), 2)) + "cm/s"
                distance = str(round(distance_covered, 2)) + "cm"
                temp = str(round(fc.cpu_temperature(), 2)) + "C"
                ret_data = {
                    'direction': direction,
                    'power': power,
                    'speed': speed,
                    'distance': distance,
                    'temp': temp
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
