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
        console.log(device.name);
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
