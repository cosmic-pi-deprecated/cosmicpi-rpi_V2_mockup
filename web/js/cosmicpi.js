const events = new EventEmitter();
const port = 9000;


// Temperature
const tempSize = 20;
let tempData = [];
let tempChart = new Chart('tempChart', {
    type: 'line',
    data: {
        labels: Array.from(Array(tempSize).keys()),
        datasets: [{
            label: 'temperature',
            data: tempData,
            backgroundColor: "rgba(153,51,255,0.4)"
        }]
    }
});

events.on('temperature', (value) => {
    // Add data to chart
    if (tempData.length > tempSize) {
        tempData.splice(0, 1);
    }
    tempData.push(value);
    tempChart.update();

    // Show data
    document.getElementById('temperature').innerHTML = value;
});


// Pressure
events.on('pressure', (value) => {
    // Show data
    document.getElementById('pressure').innerHTML = value;
});


// Location
events.on('location', (value) => {
    let map = khtml.maplib.Map(document.getElementById('location'));
    map.centerAndZoom(
        new khtml.maplib.LatLng(
            value.latitude, value.longitude
        ), 10
    );

    let marker = new khtml.maplib.overlay.Marker({
        position: new khtml.maplib.LatLng(value.latitude, value.longitude),
        map: map,
        title: 'My Cosmic Pi'
    });
});


// Magnetism
events.on('magnetism', (value) => {
    document.getElementById('magnetism').innerHTML = value;
});


let ws = new WebSocket('ws://' + window.location.hostname + ':' + port);
ws.onmessage = (e) => {
    let json = JSON.parse(e.data);
    for (let key in json) {
        console.log(key);
        events.emit(key, json[key]);
    }
};

