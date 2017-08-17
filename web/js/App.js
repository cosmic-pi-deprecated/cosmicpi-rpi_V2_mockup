const events = new EventEmitter();
const port = 9000;
const eventsToBacked = ['wifiSetting'];

let ws = new WebSocket('ws://' + window.location.hostname + ':' + port);
ws.onmessage = (e) => {
    let json = JSON.parse(e.data);
    for (let key in json) {
        events.emit(key, json[key]);
    }
};

eventsToBacked.forEach((key, value) => {
    events.on(key, (params) => {
        params['action'] = key;
        ws.send(JSON.stringify(params));
    });
});
