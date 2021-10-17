from django.shortcuts import render
import bluetooth

HOST = "E4:5F:01:43:7F:A9" # The address of Raspberry PI Bluetooth adapter on the server.
PORT = 1
sock: bluetooth.BluetoothSocket = None

def home(request):
    global sock
    if sock is None:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((HOST, PORT))
    return render(request, "sock is something")
