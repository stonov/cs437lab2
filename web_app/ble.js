// const connectToDeviceAndSubscribeToUpdates = async () => {
//     const device = await navigator.bluetooth
//        .requestDevice({
//            filters: [{ services: ['battery_service']}]
//        });
//        console.log(device)
//  };


function FindBluetoothDevices() {
    console.log("find bluetooth button clicked");
    navigator.bluetooth.requestDevice({ 
        filters: [{ 
            name: 'raspberrypi'
        }],
        optionalServices: ['battery_service'] // Required to access service later.
    })
    .then(device => {
        alert(device.name);
        return device.gatt.connect();
    })
    .then(server => {
    // Getting Battery Service…
    print(server)
    return server.getPrimaryService('battery_service');
    })
    .then(service => {
    // Getting Battery Level Characteristic…
    return service.getCharacteristic('battery_level');
    })
    .then(characteristic => {
    // Reading Battery Level…
    return characteristic.readValue();
    })
    .then(value => {
    console.log(`Battery percentage is ${value.getUint8(0)}`);
    })
    .catch(error => { console.error(error); });
}

function connectToDeviceAndSubscribeToUpdates() {
    var messageToPi = document.getElementById('message').value;
    console.log(messageToPi);
    navigator.bluetooth.requestDevice({
        filters: [{
          name: 'raspberrypi'
        }],
        optionalServices: ['battery_service'] // Required to access service later.
      })
      .then(device => { 
        console.log(device.name);
       })
      .catch(error => { console.error(error); });
}
