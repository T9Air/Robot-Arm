from machine import Pin, ADC, PWM
from utime import sleep

buttonUp = Pin(17, Pin.IN, Pin.PULL_DOWN)
buttonDown = Pin(18, Pin.IN, Pin.PULL_DOWN)
buttonRight = Pin(19, Pin.IN, Pin.PULL_DOWN)
buttonLeft = Pin(20, Pin.IN, Pin.PULL_DOWN)
buttonForward = Pin(21, Pin.IN, Pin.PULL_DOWN)
buttonBackward = Pin(22, Pin.IN, Pin.PULL_DOWN)

while True:
    try:
        if buttonUp.value() == 1:
            print("Button Up")
        elif buttonDown.value() == 1:
            print("Button Down")
        elif buttonRight.value() == 1:
            print("Button Right")
        elif buttonLeft.value() == 1:
            print("Button Left")
        elif buttonForward.value() == 1:
            print("Button Forward")
        elif buttonBackward.value() == 1:
            print("Button Backward")
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
print("Finished.")
