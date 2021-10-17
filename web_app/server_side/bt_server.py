import bluetooth
import picar_4wd as fc
from time import *
from threading import *
import json

HOST_MAC_ADDRESS = "E4:5F:01:43:7F:A9" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
PORT = 1
BACKLOG = 1
MSG_SIZE = 1024

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"
UPDATE = "UPDATE"

power_val = 50
distance_covered = 0.0
speed_cumlative = 0.0
speed_num = 0
avg_speed = 0.0
running = 1
socket: bluetooth.BluetoothSocket = None
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
        elif data == STOP:
            fc.stop()

def process_client_data(data, clientInfo):
    print("From {}: {}".format(clientInfo[0], data))
    process_data(data)

def send_feedback(data):
    direction = ""
    if data not in [STOP, SPEEDUP, SPEEDDOWN, UPDATE]:
        direction = data.lower()
    power = str(round(fc.power_read(), 2)) + "V"
    speed_val = str(round(fc.speed_val(), 2)) + "cm/s"
    distance = str(round(distance_covered, 2)) + "cm"
    temp = str(round(fc.cpu_temperature(), 2)) + "C"
    ultra_val = str(round(fc.get_distance_at(0))) + "cm"
    ret_data = {
        'direction': direction,
        'power': power,
        'speed': speed_val,
        'distance': distance,
        'temp': temp,
        'ultra': ultra_val
    }
    return json.dumps(ret_data)

def run_server():
    global socket

    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socket.bind((HOST_MAC_ADDRESS, PORT))
    socket.listen(BACKLOG)
    print("listening on port {}".format(PORT))

    try:
        client, clientInfo = socket.accept()
        while True:
            data = client.recv(MSG_SIZE)
            data = data.decode("utf-8")
            if data == "quit":
                break
            process_client_data(data, clientInfo)
            car_stats = send_feedback(data)
            client.send(car_stats)
    except Exception as e:
        print("Closing socket with Exception: {}".format(e))
        client.close()
        socket.close()

if __name__ == "__main__":
    fire_up_thread()
    run_server()
    fc.left_rear_speed.deinit()
    fc.right_rear_speed.deinit()
    speedometer.join()
    running = 0

