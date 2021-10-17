from django.shortcuts import render
import bluetooth

HOST = "E4:5F:01:43:7F:A9" # The address of Raspberry PI Bluetooth adapter on the server.
PORT = 1
sock: bluetooth.BluetoothSocket = None
INITIALIZED_TEXT = "INITIALIZED_TEXT"

def home(request):
    global sock
    if sock is None:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((HOST, PORT))
        text = INITIALIZED_TEXT
        sock.send(text)
        data_returned = sock.recv(1024)
        return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': data_returned})
    return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': 'NULL'})
