import socket
import picar_4wd as fc
import random
import json
from time import sleep

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"
IDLE = 0
STOP_INTERVAL = 0.1
HOST = "192.168.1.128" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
speed = 50

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
            speed = max(0, speed-10)
        else:
            print(data)
        sleep(STOP_INTERVAL)
        fc.forward(IDLE)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening....")
    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            data = data.decode("utf-8")
            process_data(data)
            ret_data = {
                'direction': data,
                'power': fc.power_read(),
                'speed': speed,
                'distance': random.randint(1, 5),
                'temp': fc.cpu_temperature()
            }
            print("data to send: {}".format(ret_data))
            try:
                client.sendall(\
                    bytes(json.dumps(ret_data)\
                        , "utf-8"))
            except Exception as e:
                print(e)
    except: 
        print("Closing socket")
        client.close()
        s.close()
