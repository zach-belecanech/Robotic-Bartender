from gpiozero import Servo
from time import sleep
import math


from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
global val
val = 200
val2 = 30

upperBaseServ = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
lowerMidServ = Servo(3, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
lowerBaseServ = Servo(14, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
claw = Servo(15, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
turnClaw = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
upperMidServ = Servo(16, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

def startRoutine():
    lowerBaseServ.mid()
    upperBaseServ.value = math.sin(math.radians(0))
    lowerMidServ.value = math.sin(math.radians(180))
    upperMidServ.mid()
    turnClaw.value = math.sin(math.radians(270))
    claw.min()



def grabShotGlass():
    global val
    global count
    global raiseArmCount
    global countPlusOffset
    global endvalUpperBase
    global endValUpperMidServ
    global endValLowerMidServ
    raiseArmCount = 270
    count = 0
    for i in range(180, 270): #loop that moves the arm from the start position to the lower position to grab the shot glass
        upperBaseServ.value = math.sin(math.radians(i))
        if (i == 250):
            endvalUpperBase = upperBaseServ.value
        if (count < 30):
            upperMidServ.value = math.sin(math.radians(count))
            if (count == 26):
                endValUpperMidServ = upperMidServ.value
        if (count < 20):
            lowerMidServ.value = math.sin(math.radians(180+count))
            if (count == 17):
                endValLowerMidServ = lowerMidServ.value
        count += 1
        sleep(0.01)
    
    
    for i in range(270, 180, -1): #Loop that actually grabs the shot glass
        claw.value = math.sin(math.radians(i))
        sleep(0.03)

    countPlusOffset = 32
    for i in range(270, 180, -1): #Loop that brings up the shot glass to be able to be moved around
        upperBaseServ.value = math.sin(math.radians(raiseArmCount))
        if (raiseArmCount <= 235):
            val = val + 1.5
            lowerMidServ.value = math.sin(math.radians(val))
        if (raiseArmCount <= 200):
            countPlusOffset -= 1
            upperMidServ.value = math.sin(math.radians(countPlusOffset))
        raiseArmCount-=1
        sleep(0.04)

    for i in range(180, 150, -1): #takes it from the 90 degree angle to the one past it
        upperBaseServ.value = math.sin(math.radians(i))
        if (countPlusOffset < 80):
             countPlusOffset-=1
             upperMidServ.value = math.sin(math.radians(countPlusOffset))
        sleep(0.04)

def pour():
    global val
    global count
    global raiseArmCount
    global countPlusOffset
    for i in range(180, 150, -1): # turns the whole arm to line up for re-extenstion
        lowerBaseServ.value = math.sin(math.radians(i))
        sleep(0.02)
    sleep(3)

    for i in range(150, 195): #re-extends the arm to be over the glass
        upperBaseServ.value = math.sin(math.radians(i))
        countPlusOffset+=1
        upperMidServ.value = math.sin(math.radians(countPlusOffset))
        sleep(0.04)

    for i in range(270, 170, -1):# turns the claw to pour
        turnClaw.value = math.sin(math.radians(i))
        sleep(0.08)

    sleep(1)

    for i in range(170, 270): #turns the claw back to horizonal position
        turnClaw.value = math.sin(math.radians(i))
        sleep(0.01)


    for i in range(150, 180):#moves the whole arm to be facing forward again
        lowerBaseServ.value = math.sin(math.radians(i))
        sleep(0.07)  

def putDownShotGlass():
    global val
    global count
    global raiseArmCount
    global countPlusOffset
    global endvalUpperBase
    global endValUpperMidServ
    global endValLowerMidServ

    # upperBaseServ.value = endvalUpperBase
    # upperMidServ.value = endValUpperMidServ
    # lowerMidServ.value = endValLowerMidServ
    
    
    for i in range(195, 270): #Loop that brings the shot glass back to the table
        upperBaseServ.value = math.sin(math.radians(i))
        if (i <= 235):
            val = val + 1.3
            lowerMidServ.value = math.sin(math.radians(val))
        if (i <= 200):
            countPlusOffset += 1.1
            upperMidServ.value = math.sin(math.radians(countPlusOffset))
        sleep(0.01)

    sleep(0.5)
    for i in range(180, 270): #Loop that releases the shot glass
        claw.value = math.sin(math.radians(i))
        sleep(0.07)

    
sleep(5)
startRoutine()
sleep(3)
grabShotGlass()
sleep(2)
pour()
sleep(1)
putDownShotGlass()
sleep(1)
startRoutine()

 



    
    
    
