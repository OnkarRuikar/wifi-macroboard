import time
from machine import Pin, Timer
import gc
import requests
import utime
import uping
from wifi import *
from rotary_irq import RotaryIRQ
from TTP229 import key_read
import random

# settings
url="http://192.168.0.8:4321/"
api_call_debounce=500
# wifi settings
ssid = 'MyHomeLan'
password = '12345'

led = machine.Pin('LED', Pin.OUT)
led.on()
power_led = Pin(16, Pin.OUT)
power_led.on()

# pin definitions
#scl_pin = Pin(16, Pin.OUT)
#sdo_pin = Pin(17, Pin.IN)
buzzer = Pin(10, Pin.OUT)
wifi_led = Pin(3, Pin.OUT)
server_led = Pin(20, Pin.OUT)
button_led = Pin(21, Pin.OUT)

# TTP229 pins
scl = Pin(5, mode=Pin.OUT)
sdo = Pin(4, mode=Pin.IN, pull=Pin.PULL_UP)

tim = Timer()

buzzer.value(1)
time.sleep_ms(200)
buzzer.value(0)
wifi_led.value(0)
server_led.value(0)
button_led.value(0)
time.sleep(5)
led.off()

#keypad = Keypad(scl=scl_pin, sdo=sdo_pin, inputs=16, multi=False)

mute_pin = Pin(11, Pin.IN, Pin.PULL_UP)
rotary = RotaryIRQ(pin_num_clk=8,
              pin_num_dt=6,
              min_val=0,
              reverse=False,
              half_step=True,
              range_mode=RotaryIRQ.RANGE_UNBOUNDED)
rotary_old = rotary.value()

#file = open("log.py", "a")
def write(message):
    print(message)
    #global files
    #file.write(string)
    #file.flush()
    pass

def blink_led(led, n, delay):
    for i in range(n):
        led.toggle()
        time.sleep_ms(delay)

def read_key():
    global led
    k = key_read(scl, sdo) 
    if k == 0:
        return -1
    while True:
        new_k = key_read(scl, sdo)
        #print(str(k) + " = " + str(new_k))
        if k != new_k:
            led.off()
            break
        led.toggle()
        time.sleep_ms(random.randrange(10, 30))
    return k

def beep(duration):
    buzzer.value(1)
    time.sleep_ms(duration)
    buzzer.value(0)

def get(task):
    global times
    global url
    global button_led
    try:
        gc.collect()
        write('get: ' + url + task)
        button_led.value(1)
        requests.get(url + task)
        button_led.value(0)
        write('get: done')
    except ValueError as ve:
        write('Get error: ' + str(ve))
        button_led.value(0)

def server_connection_check():
    global server_led
    global url
    try:
        gc.collect()
        button_led.value(1)
        server_led.value(0)
        requests.get(url + "ping")
        button_led.value(0)
        server_led.value(1)
    except OSError:
        server_led.value(0)
        button_led.value(0)

def wifi_connect():
    try:
        write('connecting')
        wlan = connect(ssid, password, wifi_led)
        if wlan.isconnected() == False:
            write('not connnected')
            blink_led(wifi_led, 15, 150)
            machine.reset()
        write("connected\n")
        wifi_led.value(1)
        return wlan
    except Exception as e:
        write("wifi error: " + str(e) + "\n")
        blink_led(wifi_led, 5, 150)
        machine.reset()

wlan = wifi_connect()
ROUTER = wlan.ifconfig()[2]
server_connection_check()

def wifi_check(t):
    global ROUTER
    _, recieved = uping.ping(ROUTER, count = 1, timeout = 1000, quiet=False)
    if recieved == 1:
        wifi_led.value(1)
    else:
        wifi_led.value(0)

# ping router every 3min to keep Wi-Fi connection alive
tim.init(mode=Timer.PERIODIC, freq=0.00833, callback=wifi_check)

write(str(utime.localtime()) + " starting loop \n")

while True:
    time.sleep_ms(100)
    try:
        key: int = read_key()
        if key != -1:
            write('Key: ' + str(key))
            beep(110)
            if key == 1:
                server_connection_check()
            else:
                get("b/" + str(key))

        if mute_pin.value() == 0:
            while True:
                time.sleep_ms(10)
                if button.value() == 1:
                    break
            write('volume_mute')
            beep(110)
            get("volume_mute")
            time.sleep_ms(50)

        rotary_new = rotary.value()
        if rotary_old != rotary_new:
            beep(50)
            if rotary_old < rotary_new:
                write('volume increased')
                get("volume?direction=up")
            else:
                write('volume decreased')
                get("volume?direction=down")
            rotary_old = rotary_new

    except Exception as e:
        write(str(utime.localtime()) + " loop error " + str(e))
        button_led.value(0)
        if wlan.isconnected() == False:
            wifi_led.value(0)
        pass
