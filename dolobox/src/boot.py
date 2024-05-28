# This file is executed on every boot (including wake-boot from deepsleep)
import network
from config import Config

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(Config.get_config("WIFI_NAME"),Config.get_config("WIFI_PASSWORD"))
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
try:
    do_connect()
    import main
except ImportError:
    print("main.py not found")

