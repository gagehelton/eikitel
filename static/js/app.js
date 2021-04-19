let devices;
let url = "192.168.61.200:5000"

function setButtonState(key){
  if(devices[key]['state'] == 1){document.getElementById(key).className = "btn btn-active";}
  else{document.getElementById(key).className = "btn btn-inactive";}
}

function control(key) {
    document.getElementById(key).className = "btn btn-wait";
    let request = new XMLHttpRequest();
    let name = devices[key];
    let state;
    if(devices[key]['state'] == 1) {state = "0";}
    else {state = "1";}
    
    request.open("POST", `http://${url}/control?name=${key}&state=${state}`)
    request.send();
    request.onload = () => {
        console.log(request);
        if(request.status === 200) {
            devices[key]['state'] = JSON.parse(request.response)['success'];
            setButtonState(key);
        } else {
            console.log(`error ${request.status} ${request.statusTest}`);
        }
    }

}

function getDevices() {
    let request = new XMLHttpRequest();
    request.open("GET", `http://${url}/get`);
    request.send();
    request.onload = () => {
        console.log(request);
        if(request.status === 200) {
            devices = JSON.parse(request.response);
            console.log(devices);
            for (let [key,value] of Object.entries(devices)) {
                var button = document.createElement("button");
                button.id = key;
                button.innerHTML = key;
                document.getElementById("devices").appendChild(button);
                document.getElementById("devices").appendChild(document.createElement("br"));
                document.getElementById("devices").appendChild(document.createElement("br"));
                document.getElementById(key).addEventListener('click', () => control(key));
                setButtonState(key);
            }
            document.getElementById("loader").remove();
        } else {
            console.log(`error ${request.status} ${request.statusTest}`);
        }
    }
}

//events
document.addEventListener('DOMContentLoaded', function() {
    getDevices();
}, false);