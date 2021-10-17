import bluetooth

hostMACAddress = "E4:5F:01:43:7F:A9" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 1
backlog = 1
size = 1024
INITIALIZED_TEXT = "INITIALIZED_TEXT"
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        print("server recv from: ", clientInfo)
        data = client.recv(size)
        if data:
            data = data.decode("utf-8")
            print(data)
            if data == INITIALIZED_TEXT:
                client.send("connection Initialized")
            else:
                client.send(data) # Echo back to client
except Exception as e:
    print("Closing socket with Exception: {}".format(e))
    client.close()
    s.close()

