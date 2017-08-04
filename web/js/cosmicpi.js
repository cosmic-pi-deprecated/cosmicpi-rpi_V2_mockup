$(function() {
    const size = 20;
    let tempData = [];

    function addTempData(value) {
        if (tempData.length > size) {
            tempData.splice(0, 1);
        }
        tempData.push(value)
    }

    let tempChart = new Chart('tempChart', {
        type: 'line',
        data: {
            labels: Array.from(Array(size).keys()),
            datasets: [{
                label: 'temperature',
                data: tempData,
                backgroundColor: "rgba(153,51,255,0.4)"
            }]
        }
    });

    let ws = new WebSocket('ws://' + window.location.hostname + ':9000');

    ws.onopen = (event) => {
        console.log(event);
    };

    ws.onmessage = (event) => {
        let data = JSON.parse(event.data);

        if (data.data !== undefined) {
            for (let key in data.data) {
                console.log(key);
                document.getElementById(key).innerHTML = data.data[key];

                if (key === 'temperature') {
                    addTempData(data.data[key]);
                    tempChart.update();
                }
            }
        }
    };
});



