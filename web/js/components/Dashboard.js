window.Dashboard = Vue.component('dashboard', {
    template: `
    <div>
        <div class="col-lg-4 col-md-6">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <div class="row">
                        <div class="col-xs-3">
                            <i class="fa fa-thermometer-quarter fa-5x"></i>
                        </div>
                        <div class="col-xs-9 text-right">
                            <div class="huge">{{ temperatureValue }}</div>
                            <div>{{ $t("Temperature") }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    
        <div class="col-lg-4 col-md-6">
            <div class="panel panel-success">
                <div class="panel-heading">
                    <div class="row">
                        <div class="col-xs-3">
                            <i class="fa fa-thermometer-full fa-5x"></i>
                        </div>
                        <div class="col-xs-9 text-right">
                            <div class="huge">{{ pressureValue }}</div>
                            <div>{{ $t("Pressure") }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div>
        <div class="col-lg-4 col-md-6">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <div class="row">
                        <div class="col-xs-3">
                            <i class="fa fa-microchip fa-5x"></i>
                        </div>
                        <div class="col-xs-9 text-right">
                            <div class="huge" style="font-size: 24px">{{ serialValue }}</div>
                            <div>{{ $t("Hardware Serial") }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    
    
        <div class="col-lg-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    {{ $t("Temperature") }}
                </div>
                <!-- /.panel-heading -->
                <div class="panel-body">
                    <canvas ref="temperature" style="width:100%;height:300px"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    {{ $t("Event Count") }}
                </div>
                <!-- /.panel-heading -->
                <div class="panel-body">
                    <canvas ref="combined_event_count" style="width:100%;height:300px"></canvas>
                </div>
            </div>
        </div>
    
        <div class="col-lg-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    {{ $t("Detector ADC readings") }}
                </div>
                <!-- /.panel-heading -->
                <div class="panel-body">
                    <canvas ref="ADC_readings" style="width:100%;height:300px"></canvas>
                </div>
            </div>
        </div>
    
        <div class="col-lg-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    {{ $t("Location") }}
                </div>
                <!-- /.panel-heading -->
                <div class="panel-body">
                    <div ref="location" style="width: 100%; height: 300px"></div>
                </div>
            </div>
        </div>
        
    </div>
    
    
    
  `,

    data() {
        return {
            temperatureValue: 'NA',
            pressureValue: 'NA',
            serialValue: 'NA'
        }
    },

    mounted() {
        this.initTemperatureBox();
        this.initTemperatureGraph();
        this.initCombinedEventCountGraph();
        this.initSerialBox();
        this.initLocationMap();
        this.initPressureBox();
        this.initADCGraph();
    },

    methods: {
        initPressureBox() {
            events.on('pressure', (value) => {
                this.pressureValue = value;
            });
        },

        initSerialBox() {
            events.on('serial', (value) => {
                this.serialValue = value;
            });
        },

        initLocationMap() {
			let marker = null;
			let map = khtml.maplib.Map(this.$refs.location);
			let mapZoomed = false;
			
            events.on('location', (value) => {
				if (mapZoomed === false) {
					mapZoomed = true;
					map.centerAndZoom(
						new khtml.maplib.LatLng(
							value.latitude, value.longitude
						), 16
					);
				}
                
				if (marker !== null) {
					marker.destroy();
				}
                marker = new khtml.maplib.overlay.Marker({
                    position: new khtml.maplib.LatLng(value.latitude, value.longitude),
                    map: map,
                    title: i18n.t('My Cosmic Pi')
                });
            });
        },

        initTemperatureBox() {
            events.on('temperature', (value) => {
                this.temperatureValue = value;
            });
        },

        initTemperatureGraph() {
            const tempSize = 100;
            let tempData = [];


            let tempChart = new Chart(this.$refs.temperature, {
                type: 'line',
                data: {
                    labels: Array.from(Array(tempSize).keys()),
                    datasets: [{
                        label: i18n.t('Temperature'),
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
            });
        },

        initADCGraph() {
            const detASize = 100;
            let detAData = [];
            let detBData = [];
            let labelsArray = Array.from(Array(detASize).keys());


            let ADCChart = new Chart(this.$refs.ADC_readings, {
                type: 'line',
                options: {
					animation: false
				},
                data: {
                    labels: labelsArray,
                    datasets: [{
                        label: i18n.t('Detector A: ADC measurement'),
                        data: detAData,
                        backgroundColor: "rgba(153,51,255,0.4)"
                    }, {
                        label: i18n.t('Detector B: ADC measurement'),
                        data: detBData,
                        backgroundColor: "rgba(255,150,0,0.4)"
                    }]
                }
            });

            events.on('set_ADC_readings', (arr) => {
                // Add data to chart
                // empty the original array
                detAData.splice(0,detAData.length);
                detBData.splice(0,detBData.length);
                labelsArray.splice(0,labelsArray.length);
                detAData.push(...arr[0]);
                detBData.push(...arr[1]);
                labelsArray.push(...Array.from(Array(detAData.length).keys()));
                ADCChart.update();
            });
        },

        initCombinedEventCountGraph() {
            const eventSize = 100;
            let eventData = [];


            let eventChart = new Chart(this.$refs.combined_event_count, {
                type: 'line',
                data: {
                    labels: Array.from(Array(eventSize).keys()),
                    datasets: [{
                        label: i18n.t('Combined Event Count'),
                        data: eventData,
                        backgroundColor: "rgba(153,51,255,0.4)"
                    }]
                }
            });

            events.on('combined_event_count', (value) => {
                // Add data to chart
                if (eventData.length > eventSize) {
                    eventData.splice(0, 1);
                }
                eventData.push(value);
                eventChart.update();
            });
        }
    }
});
