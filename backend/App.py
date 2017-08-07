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
location = sensors.GPS_location_provider()

# start our detector
detector = detectors.simulated_detector()

# start generator and subscribe to the detector
UiGenerator = UiDataGenerator(detector, imu, location)
UiGenerator.subscribe_to_detector()

