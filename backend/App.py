from StaticContentServer import StaticContentServer
from UiDataGenerator import UiDataGenerator
from WebSocket import WebSocket
from Constants import Constants
import sys
sys.path.append('.')
import time
import sensors
import detectors


# start UI
StaticContentServer.async_start(port=Constants.static_content_port)
WebSocket.async_start(port=Constants.web_socket_port)

#DummyDataGenerator.async_start()

# set up the IMU
IMU_SETTINGS_FILE = "IMU_settings"
imu = sensors.IMU_Reader(IMU_SETTINGS_FILE)

# set up and start the GPS
gps = sensors.GPS_location_provider()

# start our detector
detector = detectors.simulated_detector()

# start generator and subscribe to the detector
UiGenerator = UiDataGenerator(detector, imu, gps)
UiGenerator.subscribe_to_detector()

'''
# set up the IMU
IMU_SETTINGS_FILE = "IMU_settings"
imu = sensors.IMU_Reader(IMU_SETTINGS_FILE)

# set up and start the GPS
gps = sensors.GPS_location_provider()



# def a recieving function
def do_something_with_new_detector_data(*args):
    print("Fresh new data now at the detector!")
    print(args)
    # print the last GPS data
    gps_data = gps.get_last_location_data()
    print("--> GPS: ", gps_data)
    # get imu data
    IMU_data = imu.get_IMU_and_Pressure_data()
    # print imu data
    imu.print_IMU_and_pressure_data(IMU_data)

# start our detector
detec = detectors.simulated_detector()
# subscribe to detector events
detec.on_publish_new_data += do_something_with_new_detector_data
'''

