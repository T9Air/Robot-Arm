from machine import Pin, ADC, PWM
from utime import sleep

# Convert microseconds to duty cycle for the PWM
#   50MHz = 20ms period = 20000 microseconds
def DutyCycle(microseconds):
    dutyCycle = (microseconds/20000) * 100
    return int(dutyCycle * (65535/100))

# Servo min, max, and center values
#   These values are based on the servo used and may need to be adjusted
baseMin, baseMax, baseCenter = 525, 2375, 1450
bottom1Min, bottom1Max, bottom1Center = 510, 2409, 1459
# bottom2 min, max, and center are reversed because it is moving the opposite way of bottom1
bottom2Min, bottom2Max, bottom2Center = 2409, 510, 1460
topMin, topMax, topCenter = 510, 2466, 1498

currentBase = baseCenter
currentBottom1 = bottom1Center
currentBottom2 = bottom2Center
currentTop = topCenter

# Setup the servos
#   The servos are connected to the GPIO/PWM pins 12, 13, 14, and 15
#   Move the servos to their center positions
baseServo = PWM(Pin(12), freq=50)
baseServo.duty_u16(DutyCycle(baseCenter))
bottom1Servo = PWM(Pin(13), freq=50)
bottom1Servo.duty_u16(DutyCycle(bottom1Center))
bottom2Servo = PWM(Pin(14), freq=50)
bottom2Servo.duty_u16(DutyCycle(bottom2Center))
topServo = PWM(Pin(15), freq=50)
topServo.duty_u16(DutyCycle(topCenter))

# Setup the buttons
#   The buttons are connected to the GPIO pins 17, 18, 19, 20, 21, and 22
#   The buttons are pulled down to ground, so when pressed, they will be high
buttonUp = Pin(17, Pin.IN, Pin.PULL_DOWN) # Move up or rotate base servo right
buttonDown = Pin(18, Pin.IN, Pin.PULL_DOWN) # Move down or rotate base servo left
buttonRight = Pin(19, Pin.IN, Pin.PULL_DOWN) # Move right or rotate bottom1 and bottom2 servos right
buttonLeft = Pin(20, Pin.IN, Pin.PULL_DOWN) # Move left or rotate bottom1 and bottom2 servos left
buttonForward = Pin(21, Pin.IN, Pin.PULL_DOWN) # Move forward or rotate top servo right
buttonBackward = Pin(22, Pin.IN, Pin.PULL_DOWN) # Move backward or rotate top servo left

# Setup the move amount potentiometer
#   The potentiometer is connected to the GPIO pin 27
#   The potentiometer is used to set the move amount in microseconds for the servos
moveAmountPot = ADC(Pin(27))
# The starting move amount is 10 microseconds
moveAmount = 10

# Alarm and Move LED on the board until using 2 seperate LEDs
led = Pin('LED', Pin.OUT)

while True:
    # Read the potentiometer value and convert it to microseconds
    #   The potentiometer value is between 0 and 65535
    #   The move amount is between 1 and 100 microseconds
    moveAmount = int((moveAmountPot.read_u16() / 65535) * 100)
    sleep(0.01)
    if buttonUp.value() == 1:
        currentBase += moveAmount
        if currentBase > baseMax:
            currentBase = baseMax
        elif currentBase < baseMin:
            currentBase = baseMin
        led.on()
        baseServo.duty_u16(DutyCycle(currentBase))
        sleep(moveAmount / 1000)
    elif buttonDown.value() == 1:
        currentBase -= moveAmount
        if currentBase > baseMax:
            currentBase = baseMax
        elif currentBase < baseMin:
            currentBase = baseMin
        led.on()
        baseServo.duty_u16(DutyCycle(currentBase))
        sleep(moveAmount / 1000)
    elif buttonRight.value() == 1:
        currentBottom1 += moveAmount
        currentBottom2 -= moveAmount
        if currentBottom1 > bottom1Max:
            currentBottom1 = bottom1Max
            currentBottom2 = bottom2Min
        elif currentBottom1 < bottom1Min:
            currentBottom1 = bottom1Min
            currentBottom2 = bottom2Max
        led.on()
        bottom1Servo.duty_u16(DutyCycle(currentBottom1))
        bottom2Servo.duty_u16(DutyCycle(currentBottom2))
        sleep(moveAmount / 1000)
    elif buttonLeft.value() == 1:
        currentBottom1 -= moveAmount
        currentBottom2 += moveAmount
        if currentBottom1 < bottom1Min:
            currentBottom1 = bottom1Min
            currentBottom2 = bottom2Max
        elif currentBottom1 > bottom1Max:
            currentBottom1 = bottom1Max
            currentBottom2 = bottom2Min
        led.on()
        bottom1Servo.duty_u16(DutyCycle(currentBottom1))
        bottom2Servo.duty_u16(DutyCycle(currentBottom2))
        sleep(moveAmount / 1000)
    elif buttonForward.value() == 1:
        currentTop += moveAmount
        if currentTop > topMax:
            currentTop = topMax
        elif currentTop < topMin:
            currentTop = topMin
        led.on()
        topServo.duty_u16(DutyCycle(currentTop))
        sleep(moveAmount / 1000)
    elif buttonBackward.value() == 1:
        currentTop -= moveAmount
        if currentTop > topMax:
            currentTop = topMax
        elif currentTop < topMin:
            currentTop = topMin
        led.on()
        topServo.duty_u16(DutyCycle(currentTop))
        sleep(moveAmount / 1000)
    led.off()
    sleep(0.01) # sleep 10ms