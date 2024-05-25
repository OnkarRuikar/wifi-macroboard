import network
import socket
from time import sleep

import machine

def connect(ssid, password, alive):
    wlan = network.WLAN(network.STA_IF)
    print("Activating WLAN")
    wlan.active(True)
    print("Connecting to Wi-Fi")
    wlan.connect(ssid, password)

    for j in range(30):
        if wlan.isconnected() == False:
            print('Waiting for connection...' + str(j))
            alive.value(0)
            sleep(0.8)
            alive.value(1)
            sleep(1)

    if wlan.isconnected() == False:
        wlan.connect(ssid, password)
        for j in range(30):
            if wlan.isconnected() == False:
                print('Waiting for connection again...' + str(j))
                alive.value(0)
                sleep(0.8)
                alive.value(1)
                sleep(1)

    print(wlan.ifconfig())
    return wlan
