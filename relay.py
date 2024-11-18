from machine import Pin

def relay_on():
    relay = Pin(22,Pin.OUT)
    relay.value(1)
    return()

def relay_off():
    relay = Pin(22,Pin.OUT)
    relay.value(0)
    return()