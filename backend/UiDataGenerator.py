from EventEmitter import EventEmitter
import time
import random
import threading

"""
This module only generates events. `EventEmitter.get()` should be implemented into the core
of Cosmic Pi application.

Idea behind EventEmitter is to push event (call on_something() method) every time some event
happened. Once method is called event is propagated to rest of the system.
"""
class UiDataGeneratorHandler(object):
    def run(self):
        while True:
            time.sleep(0.2)
            EventEmitter.get().on_temperature(round(random.uniform(20, 30), 2))
            EventEmitter.get().on_pressure(round(random.uniform(950, 1100), 2))
            EventEmitter.get().on_magnetism(round(random.uniform(0, 1), 2))

class UiDataGenerator(object):
    @staticmethod
    def async_start():
        dummy_data_generator_handler = DummyDataGeneratorHandler()
        thread = threading.Thread(target=dummy_data_generator_handler.run)
        thread.start()

    def _push_data_to_UI(self, data):
        # get imu data
        IMU_data = self._imu.get_IMU_and_Pressure_data()
        # temperature
        if (IMU_data["temperatureValid"]):
            EventEmitter.get().on_temperature(round(IMU_data["temperature"], 2))
        # pressure
        if (IMU_data["pressureValid"]):
            EventEmitter.get().on_pressure(round(IMU_data["pressure"], 1))

        # get location data
        location_data = self._location.get_last_location_data()
        # TODO: remove a strange bug here!
        EventEmitter.get().on_location({'latitude': location_data['lat'], 'longitude': location_data['lon']})

        # get detector data
        EventEmitter.get().on_combined_event_count(float(data['event_counter_AB']))
        EventEmitter.get().set_ADC_readings(data['event_stack_AB'])

        # push the serial
        EventEmitter.get().on_serial(self._serial)

        # old printing
        print("Fresh new data now at the detector!")
        print(data)
        # print the last GPS data
        location_data = self._location.get_last_location_data()
        print("--> GPS: ", location_data)
        # get imu data
        IMU_data = self._imu.get_IMU_and_Pressure_data()
        # print imu data
        self._imu.print_IMU_and_pressure_data(IMU_data)

    def __init__(self, detector, imu, location, serial):
        # the function must recieve an already initalized detector, imu and gps
        self._detector = detector
        self._imu = imu
        self._location = location
        self._serial = serial


    def subscribe_to_detector(self):
        self._detector.on_publish_new_data += self._push_data_to_UI


