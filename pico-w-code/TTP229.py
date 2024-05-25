#!/usr/bin/env python
# -*- coding: utf8 -*-

#  MIT License

# Copyright (c) 2022 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape

# This is version for MicroPython v1.18
# TTP229 Touch Keypad

from machine import Pin
from gc import collect
from utime import sleep_ms, sleep_us

def _key_map(data: list) -> int:
    key: int = 0
    for bit in data:
        if bit != 0:
            key += 1
        else:
            break
    # print(f"key = {(key // 2) + 1}")
    return ((key // 2) + 1)

def key_read(scl: Pin, sdo: Pin, mode: int=32) -> int:
    data: list = []
    wait: int = 0
    key: int = 0
    
    scl.high() # change polarity of [scl] to high
    data.clear() # clear the data[]
    wait = 0 # zero the wait
    sleep_us(103) # when sdo was 0, wait 103us for data.
    # DV = 93us, Tw = 10us. DV + Tw = 103us.
    while wait != mode: # I need 32ms to read data in 16keyMode.
    # while wait != _8_KEY_MODE: # I need 16ms to read data in 8keyMode.
        data.append(sdo.value()) # read and append the value of [sdo] as bit of data
        scl.toggle() # make 1 khz clock to read 32bit data. if 1s / 1000 = 1ms, each cycle of clock is 1ms
        sleep_ms(1) # wait 1ms and change the polarity of [scl]
        wait += 1
    # print(data) # data has funny format!
    scl.low() # after reading, set [scl] to low.
    if 0 in data:
        key: int = _key_map(data) # call function to map the data to key.
    sleep_ms(2) # wait 2ms for next data. if I hold my finger on current-key, I should wait 2ms to read it.
    collect()
    #print(str(key))
    return key
