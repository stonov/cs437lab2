document.onkeydown = updateKey;
document.onkeyup = resetKey;

const FORWARD = "FORWARD"
const BACKWARD = "BACKWARD"
const LEFT = "LEFT"
const RIGHT = "RIGHT"
const STOP = "STOP"
const SPEEDUP = "SPEEDUP"
const SPEEDDOWN = "SPEEDDOWN"
const UPDATE = "UPDATE"
const POWER = "POWER"

var server_port = 65432;
var server_addr = "192.168.1.147";   // the IP address of your Raspberry PI

function sendMoveForwardCommand() {
    client(FORWARD);
}

function sendMoveBackwardCommand() {
    client(BACKWARD);
}

function sendMoveLeftCommand() {
    client(LEFT);
}

function sendMoveRightCommand() {
    client(RIGHT);
}

function sendStopCommand() {
    client(STOP);
}

function sendSpeedData(val) {
    console.log(val)
    str = "POWER " + val
    console.log(str)
    client(str);
}

function client(data="") {
    if (data == "") {
        return;
    }
    if (data == "message") {
        data = document.getElementById("message").value;
    }
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${data}`);
    });

    // get the data from the server
    client.on('data', (data) => {
        processServerData(data);
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });

}

function processServerData(data) {
    data_json = JSON.parse(data.toString())
    if (data_json['power'] != "") {
        document.getElementById("power").innerHTML = data_json['power'];
    }
    if (data_json['direction'] != "") {
        document.getElementById("direction").innerHTML = data_json['direction'];
    }
    if (data_json['speed'] != "") {
        document.getElementById("speed").innerHTML = data_json['speed'];
    }
    if (data_json['speed_percent'] != "") {
        document.getElementById("speed_percent").innerHTML = data_json['power_val'];
    }
    if (data_json['distance'] != "") {
        document.getElementById("distance").innerHTML = data_json['distance'];
    }
    if (data_json['temperature'] != "") {
        document.getElementById("temperature").innerHTML = data_json['temp'];
    }
    if (data_json['ultra'] != "") {
        document.getElementById("ultra").innerHTML = data_json['ultra'];
    }
}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {
    e = e || window.event;
    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        sendMoveForwardCommand();
    } else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        sendMoveBackwardCommand();
    } else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        sendMoveLeftCommand();
    } else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        sendMoveRightCommand();
    } else if (e.keyCode == '81') {
        // stop (e)
        sendStopCommand();
    } else if (e.keyCode >= '48') {
        val = parseInt(e.keyCode) - 48
        if (val == 0) {
            val = 10
        }
        sendSpeedData((val*10).toString())
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

function run_client() {
    setInterval(function(){
        // get image from python server
        client(UPDATE);
    }, 1000);
}

