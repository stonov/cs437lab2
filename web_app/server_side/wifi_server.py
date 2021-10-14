import socket
import picar_4wd as fc
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
            speed += 10
        elif data == SPEEDDOWN:
            print("slowing down")
            speed -= 10
        else:
            print(data)
        sleep(STOP_INTERVAL)
        fc.forward(IDLE)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            process_data(data.decode("utf-8"))
    except: 
        print("Closing socket")
        client.close()
        s.close()    
