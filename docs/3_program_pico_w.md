# Raspberry Pi Pico W

Pico W is a [microcontroller board](https://en.wikipedia.org/wiki/Single-board_microcontroller) with Wi-Fi. For more information refer the [datasheet](./pico-w-datasheet.pdf).

## Setup Pico W

Download [the latest firmware](https://micropython.org/download/RPI_PICO_W) `.uf2` file for Pico W from `micropython.org`.

Use [Raspberry Pi Pico W Getting Started](https://youtu.be/vgjvAVe_EUg?si=Jy1m6aa9m-iPZy-c) video tutorial to setup the Pico W and install [Thonny](https://thonny.org) IDE.

Execute following code in Thonny to check Wi-Fi connectivity:

```py
import machine
import network
import ubinascii
from time import sleep

led=machine.Pin('LED', machine.Pin.OUT)
led.on()

print('starting')
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
print('mac: ' + str(mac))
accesspoints=wlan.scan()
for ap in accesspoints:
    print(ap)

ssid='LLan22'
password='44github'

wlan.connect(ssid, password)
for j in range(30):
    if wlan.isconnected() == False:
        print('Waiting for connection...' + str(j))
        sleep(2)

if wlan.isconnected() == False:
    wlan.connect(ssid, password)
    for i in range(30):
        if wlan.isconnected() == False:
            print('Waiting for connection...2 ' + str(i))
            sleep(2)

print(wlan.ifconfig())
print('done')
```

It is observed that when connected using USB the Wi-Fi connection happens quickly. But when connected to only battery power, the Wi-Fi connection may take more time, so be patient.

## Copy macro pad code to Pico W

Get `.py` files under [pico-w-code/*](../pico-w-code) on Pico W. Simplest way is to create new files with same name-extension on Pico W using Thonny and copy paste code in them.

Make following changes in the code and save on Pico W.

1. wifi.py: Update name of your Wi-Fi network and password.
2. main.py: Update macro server URL (IP address and port).

This is it for now. Close Thonny and disconnect the Pico W. We'll revisit Pico W programming after we've soldered all the components together.

## Next

[Assemble componentes](./4_assembling.md)