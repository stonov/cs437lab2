import bluetooth

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"
COMMANDS = {
    'w': FROWARD,
    's': BACKWARD,
    'd': RIGHT,
    'a': LEFT,
    'q': STOP,
    '+': SPEEDUP,
    '-': SPEEDDOWN
}
STARTUP_MSG = "Commands are as such:\n\tw -> FROWARD\n\ts -> BACKWARD\n\ta -> LEFT\n\td -> RIGHT\n\tq -> STOP\n\t+ -> SPEEDUP\n\t- -> SPEEDDOWN\nPress Enter after The Letter"

HOST_MAC_ADDRESS = "E4:5F:01:43:7F:A9" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
PORT = 1
MSG_SIZE = 1024

sock: bluetooth.BluetoothSocket = None

def run_client():
    global sock

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print("Waiting To Connect....")
    sock.connect((HOST_MAC_ADDRESS, PORT))
    while True:
        text = input("Enter Command #: ")
        if text == "quit":
            sock.send(command)
            break
        command = COMMANDS['q']
        if text in COMMANDS.keys():
            command = COMMANDS[text]
        sock.send(command)
        data = sock.recv(MSG_SIZE)
        print("from server: ", data)

if __name__ == "__main__":
    print(STARTUP_MSG)
    run_client()
    sock.close()


