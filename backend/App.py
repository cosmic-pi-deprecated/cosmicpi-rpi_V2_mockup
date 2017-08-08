from StaticContentServer import StaticContentServer
from UiDataGenerator import UiDataGenerator
from WebSocket import WebSocket
from Constants import Constants
import sys
sys.path.append('.')
import time
import sensors
import detectors
import configparser


# settings files
CONFIG_FILE = "CosmicPi.config"
IMU_SETTINGS_FILE = "IMU_settings"

# read configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
_enable_GPS = config.getboolean("Location_Provider", "enable_GPS")
_enable_geoIP = config.getboolean("Location_Provider", "enable_geoIP")
_enable_UI = config.getboolean("UI", "enable_UI")


# start UI
if _enable_UI:
    StaticContentServer.async_start(port=Constants.static_content_port)
    WebSocket.async_start(port=Constants.web_socket_port)

#DummyDataGenerator.async_start()

# set up the IMU
imu = sensors.IMU_Reader(IMU_SETTINGS_FILE)

# set up and start the location provider
if _enable_geoIP and _enable_GPS:
    location = sensors.Combined_location_provider()
elif _enable_GPS:
    location = sensors.GPS_location_provider()
elif _enable_geoIP:
    location = sensors.IP_location_provider()
else:
    raise RuntimeError("No location provider was specified! Please enable at least one in: " + str(CONFIG_FILE))

# start our detector
detector = detectors.simulated_detector()

# start generator and subscribe to the detector
UiGenerator = UiDataGenerator(detector, imu, location, sensors.getserial())
UiGenerator.subscribe_to_detector()

