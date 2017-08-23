import configparser
import subprocess
import wifi


class WIFI_handler():
    def __init__(self, CONFIG_FILE):
        # read configuration
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        self._AP_enable = config.getboolean("Access Point", "enable")
        self._AP_name = config.get("Access Point", "name")
        self._AP_pw = config.get("Access Point", "password")#
        # Todo: Implement the reading of already used wifi networks
        self._AP_process = 0

        # start the AP if this is wanted
        if self._AP_enable:
            self._start_AP()



    def _start_AP(self):
        # start the AP via cmd
        cmd_list = ['sudo', '/usr/bin/create_ap', 'wlan0', 'eth0', self._AP_name, self._AP_pw]
        try:
            self._AP_process = subprocess.Popen(cmd_list)
        except:
            print("Unexpected error while starting Access Point: ", end='')
            print(sys.exc_info()[0])
        print("AP started")

    def _stop_AP(self):
        if self._AP_process == 0:
            print("No AP running, not stopping anything")
            return
        print("Turning of AP")
        self._AP_process.terminate()
        print("AP offline")
        self._AP_process = 0

