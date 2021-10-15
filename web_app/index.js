document.onkeydown = updateKey;
document.onkeyup = resetKey;

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"

var server_port = 65432;
var server_addr = "192.168.1.128";   // the IP address of your Raspberry PI
var data_tobe_sent = ""

function sendMoveForwardCommand() {
    data_tobe_sent = FROWARD
}

function sendMoveBackwardCommand() {
    data_tobe_sent = BACKWARD
}

function sendMoveLeftCommand() {
    data_tobe_sent = LEFT
}

function sendMoveRightCommand() {
    data_tobe_sent = RIGHT
}

function sendStopCommand() {
    data_tobe_sent = STOP
}

function sendSpeedUp() {
    data_tobe_sent = SPEEDUP
}

function sendSpeedDown() {
    data_tobe_sent = SPEEDDOWN
}

function client(data="") {
    if (data == "") {
        return;
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
        data_json = JSON.parse(data.toString())
        document.getElementById("power").innerHTML = data_json['power'];
        document.getElementById("direction").innerHTML = data_json['direction'];
        document.getElementById("speed").innerHTML = data_json['speed'];
        document.getElementById("distance").innerHTML = data_json['distance'];
        document.getElementById("temperature").innerHTML = data_json['temp'];
        console.log(data_json);
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {
    e = e || window.event;
    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        sendMoveForwardCommand();
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        sendMoveBackwardCommand();
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        sendMoveLeftCommand();
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        sendMoveRightCommand();
    }
    else if (e.keyCode == '81') {
        // stop (e)
        sendStopCommand();
    }
    else if (e.keyCode == '187') {
        // increase speed (e)
        sendSpeedUp();
    }
    else if (e.keyCode == '189') {
        // decrease speed (e)
        sendSpeedDown();
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
        client(data_tobe_sent);
        data_tobe_sent = ""
        // console.log("client sending data");
    }, 100);
}

