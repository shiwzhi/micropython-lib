import network
import webrepl


class WIFI:
    def __init__(self) -> None:
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

    def connect(self, ssid, password):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)

    def setup_ap(self, ssid, password=""):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=ssid, password=password,
                       authmode=network.AUTH_WPA_WPA2_PSK)

    def start_webrepl(self, password=""):
        webrepl.start(password=password)
