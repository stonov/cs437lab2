from bluetooth.macos import BluetoothSocket
from django.shortcuts import render
import bluetooth

HOST = "DC:A6:32:80:7D:87" # The address of Raspberry PI Bluetooth adapter on the server.
PORT = 1
sock: BluetoothSocket = None

def home(request):
    global sock
    if sock is None:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((HOST, PORT))
    return render(request, "sock is something")
