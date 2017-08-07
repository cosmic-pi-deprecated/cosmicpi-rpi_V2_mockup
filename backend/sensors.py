import threading
import copy
import time
import os.path
import RTIMU
from gpspy3 import gps



class IMU_Reader():

    def __init__(self, IMU_SETTINGS_FILE):
        # ---------  Set up IMU
        print("Using settings file " + IMU_SETTINGS_FILE + ".ini")
        if not os.path.exists(IMU_SETTINGS_FILE + ".ini"):
            print("Settings file does not exist, will be created")

        self.s = RTIMU.Settings(IMU_SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.s)
        self.pressure = RTIMU.RTPressure(self.s)

        print("IMU Name: " + self.imu.IMUName())
        print("Pressure Name: " + self.pressure.pressureName())

        if (not self.imu.IMUInit()):
            print("IMU Init Failed")
            raise RuntimeError("Could not initilize IMU! Is I2C enabled? Are you on the Pi? Did you check that the IMU is visible via I2C?")
        else:
            print("IMU Init Succeeded");

        # this is a good time to set any fusion parameters

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        if (not self.pressure.pressureInit()):
            print("Pressure sensor Init Failed")
            raise RuntimeError("Could not initilize pressure sensor! Did you check that the sensor is visible via I2C?")
        else:
            print("Pressure sensor Init Succeeded")

        self.poll_interval = self.imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % self.poll_interval)
        print("IMU init successfully finished!")

    def get_IMU_and_Pressure_data(self, average=1):
        if average > 1:
            raise NotImplementedError("For now no averaging has been implemented! Only the usage of 1 is feasible.")
        average = 1

        # gat Data from IMU
        while self.imu.IMURead() is not True:
            time.sleep(self.poll_interval * 1.0 / 1000.0)
        data = self.imu.getIMUData()
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = self.pressure.pressureRead()
        time.sleep(self.poll_interval * 1.0 / 1000.0)

        return data

    def print_IMU_and_pressure_data(self, data):
        # accel
        if data["accelValid"] == True:
            print("Accel: ", data["accel"])
        else:
            print("Accel data NOT valid!")
        # gyro
        if data["gyroValid"] == True:
            print("Gyro: ", data["gyro"])
        else:
            print("Gyro data NOT valid!")
        # compass
        if data["compassValid"] == True:
            print("Compass: ", data["compass"])
        else:
            print("Compass data NOT valid!")
        # pressure
        if (data["pressureValid"]):
            print("Pressure: %f" % (data["pressure"]))
        else:
            print("Pressure data NOT valid!")
        # temperature
        if (data["temperatureValid"]):
            print("Temperature: %f" % (data["temperature"]))
        else:
            print("Temperature data NOT valid!")
        # fused position
        print("Fused position: ", data["fusionPose"])


class location_provider():

    def __init__(self, provider_name):
        self.location_data = {
                        'lon': 0,
                        'lat': 0,
                        'alt': 0,
                        'err_lon_meter': 999,
                        'err_lat_meter': 999,
                        'err_alt_meter': 999,
                        'update_time_string': '1970-01-01T00:00:00.000Z',
                        '_internal_timestamp': time.time()
                    }
        self.output_lock = threading.Lock()
        self.provider_name = provider_name

    def _update_location_data(self, ext_location_data):
        with self.output_lock:
            self.location_data = copy.deepcopy(ext_location_data)

    def get_last_location_data(self):
        with self.output_lock:
            return copy.deepcopy(self.location_data)


class GPS_location_provider(location_provider, threading.Thread):
    def __init__(self):
        location_provider.__init__(self, "GPS")
        threading.Thread.__init__(self)

        # Listen on port 2947 (gpsd) of localhost
        self.session = gps.GPS("localhost", "2947")
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        # start our own thread
        self.start()

    def _get_next_GPS_update(self):
        report = self.session.next()
        # Wait for a 'TPV' report
        if report['class'] == 'TPV':
            # check if the report contains location and time data
            if ('time' in report) and ('lon' in report):
                internal_localion_data = {}
                internal_localion_data['lon'] = report['lon']
                internal_localion_data['lat'] = report['lat']
                internal_localion_data['alt'] = report['alt']
                internal_localion_data['err_lon_meter'] = report['epx']
                internal_localion_data['err_lat_meter'] = report['epy']
                internal_localion_data['err_alt_meter'] = report['epv']
                internal_localion_data['update_time_string'] = report['time']
                internal_localion_data['_internal_timestamp'] = time.time()
                # update our loc data
                self._update_location_data(internal_localion_data)
            else:
                pass;

    def run(self):
        while True:
            connect_error_counter = 0
            try:
                self._get_next_GPS_update()
                connect_error_counter = 0
                time.sleep(0.02)
            except KeyError:
                pass
            except StopIteration as e:
                if connect_error_counter < 20:
                    print("Is GPSD still up? Will retry in a bit")
                    connect_error_counter += 1
                else:
                    raise RuntimeError("GPSD seems to have stopped, and too many retries to reconnect were made!")