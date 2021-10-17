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
        data_returned = data_returned.decode("utf-8")
        return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': data_returned})
    return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': 'sock is not null'})

def send_data(request):
    global sock
    data = str(request.GET.get('data'))
    print(data)
    if sock is None:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((HOST, PORT))
    sock.send(data)
    data_returned = sock.recv(1024)
    data_returned = data_returned.decode("utf-8")
    return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': data_returned})

def recieve_data(request):
    print("we are in recieve_data")
    if request.is_ajax and request.method == 'POST':
        data = request.POST.get('data')
        print(data)
        return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': data})
    return render(request, "backend_app/base.html", {'sock': sock, 'returned_val': None})
