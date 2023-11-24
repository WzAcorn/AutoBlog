from machine import pin
import time

pin = pin("LED", pin.OUT)

while True:
    pin.toggle()
    time.sleep(0.5)