from machine import Pin
relay_pin = Pin(22, Pin.OUT)

def relay_on():
    relay_pin.on()

def relay_off():
    relay_pin.off()