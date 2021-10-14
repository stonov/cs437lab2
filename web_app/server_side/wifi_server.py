import socket
import picar_4wd as fc

HOST = "192.168.1.128" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def process_data(data=""):
    if data != "":
        if data == "forward":
            print("moving forward")
        elif data == "backward":
            print("moving backward")
        elif data == "right":
            print("moving right")
        elif data == "left":
            print("moving left")
        else:
            print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            process_data()
    except: 
        print("Closing socket")
        client.close()
        s.close()    
