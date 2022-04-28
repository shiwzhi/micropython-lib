import network
import webrepl

class WIFI:
    def __init__(self) -> None:
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

    def connect(self, ssid, password):
        self.wlan.active(True)
        self.wlan.connect(ssid, password)

    def setup_ap(self, ssid, password=""):
        self.ap.config(essid=ssid, password=password)
        self.ap.active(True)

    def start_webrepl(self, password=""):
        webrepl.start(password=password)

