from StaticContentServer import StaticContentServer
from UiDataGenerator import UiDataGenerator
from WebSocket import WebSocket
from Constants import Constants
import sys
sys.path.append('.')
import sensors
import detectors
import configparser
from wifi_handler import WIFI_handler


# settings files
CONFIG_FILE = "CosmicPi.config"
IMU_SETTINGS_FILE = "IMU_settings"

# read configuration
# Todo: Implement proper error catching for configparser (e.g. non existent keys or file)
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
_GPS_enable = config.getboolean("Location Provider", "enable_GPS")
_geoIP_enable = config.getboolean("Location Provider", "enable_geoIP")
_UI_enable = config.getboolean("UI", "enable_UI")


# start Wifi connection
wifi = WIFI_handler(CONFIG_FILE)

# start UI
if _UI_enable:
    StaticContentServer.async_start(port=Constants.static_content_port)
    WebSocket.async_start(port=Constants.web_socket_port)


# set up the IMU
imu = sensors.IMU_Reader(IMU_SETTINGS_FILE)

# set up and start the location provider
if _geoIP_enable and _GPS_enable:
    location = sensors.Combined_location_provider()
elif _GPS_enable:
    location = sensors.GPS_location_provider()
elif _geoIP_enable:
    location = sensors.IP_location_provider()
else:
    raise RuntimeError("No location provider was specified! Please enable at least one in: " + str(CONFIG_FILE))

# start our detector
detector = detectors.simulated_detector(imu)

# start generator and subscribe to the detector
UiGenerator = UiDataGenerator(detector, imu, location, sensors.getserial())
UiGenerator.subscribe_to_detector()

