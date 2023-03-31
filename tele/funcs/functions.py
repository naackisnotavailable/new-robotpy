import time
from funcs import swivelP

swP = swivelP.PID()

on1 = 0
on2 = 0
on3 = 0

gPos = 0

def setGPos(grabEncoder):
    global gPos
    gPos = grabEncoder.getPosition()


#
def drive(leftTalon1, leftTalon2, rightTalon1, rightTalon2, stick, drive, slowed, led):
    b = stick.getBButtonPressed()
    if b == True:
        slowed += 1
    if slowed % 2 == 1:
        lX = stick.getLeftX() * 0.3
        #Sameer drive if needed
        #lX = stick.getRightX() * 0.15
        lY = stick.getLeftY() * 0.2
        #red for slow blah
        led.set(-0.25)
    else:
        lX = stick.getLeftX() * 0.5 #pre 0.7
        #Sameer drive if needed
        #lX = stick.getRightX()
        lY = stick.getLeftY() * 0.7
        #green for fast
        led.set(0.75)

    if lX <= 1.0 and lY <= 1.0:
        drive.curvatureDrive(lX, lY, True)
    else:
        raise Exception("safety toggle, one or more inputs > 1")
    return slowed
def balanceCheck(l1, l2, r1, r2, stick, gyro, leftMotors, rightMotors, balancePID, spinPID, led):
    global on3
    
    if stick.getAButtonPressed() == True:
        on3 += 1
        print('on!')
        
    if on3 % 2 == 1:

        #rainbow for pid
        led.set(-0.99)
        balancePID.main(gyro.getPitch(), leftMotors, rightMotors)
        print('balancing: ' + str(gyro.getPitch()))
    else:
        pass


def getPose(inst):
    return inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])
def table(stick2, table):
    if stick2.getYButton() == True:
        table.set(0.125)
    elif stick2.getBButton() == True:
        table.set(-0.125)
    else:
        table.set(0.0)
def intake(stick2, b, t, io, ioEncoder, exPID, a, c):
    global on1
    global on2

    x = stick2.getXButton()
    if x == True:
        on1 += 1

    if a == False and c == False:

        if x == True:
            b.set(-0.75)
            t.set(0.75)
        else:
            b.set(0.0)
            t.set(0.0)

        a = stick2.getAButtonPressed()
        if a == True:
            on2 += 1
        if on2 % 2 == 1:
            io.set(exPID.main(ioEncoder, True))
        else:
            io.set(exPID.main(ioEncoder, False))
            

def lift(lift, liftEncoder, exPID2, stick2, a, b, lim):

    if a == False and b == False:
            spd = stick2.getLeftY()
            if spd < 0:
                spd = -1*(spd**2)
                lift.set(spd)
            elif spd > 0:
                spd = spd**2
                lift.set(spd)
            else:
                spd = 0
                lift.set(spd)
            #if lim == True:
            #    if spd > 0:
            #        lift.set(spd)
            #    elif spd < 0:
            #        lift.set(0.0)
            #else:
            #    lift.set(spd)

            #if spd < 0:
            #    spd = -1*(spd**2)
            #elif spd > 0 :
            #    spd = spd**2
            #lift.set(spd)

            #if stick2.getLeftBumper() == True:
            #    lift.set(exPID2.main(liftEncoder, True))
            #elif stick2.getLeftBumper() == False:
            #    lift.set(exPID2.main(liftEncoder, False)
    
def grab(grabby, grabbyEncoder, grab, grabEncoder, stick2, a, b):
    global gPos
    if a == False and b == False:
        curr = grabby.getOutputCurrent() / 100
        print(curr)
        if stick2.getRightY() > 0.1 :
            print('closing')
            #grabby.set(.main(grabbyEncoder.getPosition(), grabby, 0.3))
            grabby.set(0.35 - curr)#pre 0.6
        elif stick2.getRightY() < -0.1:
            print('opening')
            #grabby.set(gpi.main(grabbyEncoder.getPosition(), grabby, -2.5))
            grabby.set(-0.3 + curr)#pre -0.3       -0.3 + curr

        if abs(stick2.getRightTriggerAxis()) < 0.01 and abs(stick2.getLeftTriggerAxis()) < 0.01:
            swP.main(grabEncoder.getPosition(), grab, gPos)


        else:
            if stick2.getLeftTriggerAxis() > 0.1:
                print('down')
                grab.set(-0.3*(stick2.getLeftTriggerAxis()**2))
            elif stick2.getRightTriggerAxis() > 0.1:
                #print('up')
                grab.set(0.3*stick2.getRightTriggerAxis()**2)#pre .5
            else:
                grab.set(0.01)
            gPos = grabEncoder.getPosition()


def moveOut(io, ioEncoder, exPID, grab, grabEncoder, lift, liftEncoder, grabby, stick2, lim):
    curr = grabby.getOutputCurrent() / 100
    if stick2.getRightBumper() == True:
        global gPos
        gPos = grabEncoder.getPosition()

        interrupted = True

        print('closing')
        grabby.set(0.55 - curr)#pre 0.4

        io.set(exPID.main(ioEncoder, True)) # intake moves out
        print('liftpos: ' + str(liftEncoder.getPosition()))

        if liftEncoder.getPosition() > -78: #lift begins moving pre -45 -70
            
            print('liftpos: ' + str(liftEncoder.getPosition()))
            lift.set(-0.4)
        else:
            lift.set(0.0)

        grab.set(-0.06)  #pre -0.08
    else:
        interrupted = False
    return interrupted

#def rumble(liftEncoder, stick2):
#    if liftEncoder.getPosition > -75 or liftEncoder.getPosition < 0:
#        stick2.setRumble(RumbleType.kRightRumble, 1.0)


def moveIn(io, ioEncoder, exPID, grab, grabEncoder, lift, liftEncoder, grabby, stick2, lim):
    global gPos
    curr = grabby.getOutputCurrent() / 100

    if stick2.getLeftBumper() == True:
        gPos = grabEncoder.getPosition()
        interrupted = True
        print('running t1')

        if liftEncoder.getPosition() > -15:
            print('opening')
            grabby.set(-0.2 + curr)
        else:
            print('closing')
            grabby.set(0.4 - curr)
    
        io.set(exPID.main(ioEncoder, True)) # intake moves out
        print('liftpos: ' + str(liftEncoder.getPosition()))

        grab.set(-0.065)

        if grabEncoder.getPosition() < -1:
            print('running t2')
            grab.set(-0.04)
            if liftEncoder.getPosition() < -5: #lift begins moving
                print('running t3')
                lift.set(0.4)
            else:
                lift.set(0.0)
                grabby.set(-0.07)
        else:
            lift.set(0.0)
    else:
        interrupted = False
    return interrupted

#def shelfHeight(lift, liftEncoder, stick2, led):
#    if stick2.getRawAxis(1):
#        led.set(0.17)
#        if liftEncoder.getPosition() > -75:
#            lift.set(-0.4)


def moveOutAuton(grab, grabEncoder, lift, liftEncoder, io, ioEncoder, exPID, autonSwiv, grabby):
    if liftEncoder.getPosition() > -61:   #-82
        curr = grabby.getOutputCurrent() / 100
        print('liftpos: ' + str(liftEncoder.getPosition()))
        print('grabpos: ' + str(grabEncoder.getPosition()))
        global gPos
        gPos = grabEncoder.getPosition()
        grabby.set(0.1)  #grab cube
        #print('ioEncoder: ' + str(ioEncoder.getPosition()))
        io.set(exPID.main(ioEncoder, True))  #intake out
        if liftEncoder.getPosition() > -60: #lift start going up
            lift.set(-0.4)
        else:
            lift.set(0.0)
        if liftEncoder.getPosition() > -60.0:  #swivel control
            grab.set(-0.125)
        else:
            if grabEncoder.getPosition() < 12:  #pre 15
                #autonSwiv.main(grabEncoder.getPosition(), grab, 2)  #pre 19
                grab.set(0.07)
            else:
                grab.set(0.01) #pre.07
        if grabEncoder.getPosition() > 2: #late lift control movements pre 8
            if liftEncoder.getPosition() < -60 and liftEncoder.getPosition() > -61: #pre-80
                lift.set(-0.1)
            else:
                lift.set(0.0)
                return True

            

def moveCM(leftMotors, rightMotors, leftEncoder, rightEncoder, inches, speed):
    ticks = inches * 0.249
    
    print(ticks)
    if ticks > 0:
        if rightEncoder.getPosition() > -ticks:
            rightMotors.set(speed * -1.12)
        else:
            rightMotors.set(0.0)
        if leftEncoder.getPosition() < ticks:
            leftMotors.set(speed * 1)
        else:
            leftMotors.set(0.0)
    elif ticks < 0:
        if rightEncoder.getPosition() < -ticks:
            rightMotors.set(speed * 1.35)#25 pre
        else:
            rightMotors.set(0.0)
        if leftEncoder.getPosition() > ticks:
            leftMotors.set(speed * -1)
        else:
            leftMotors.set(0.0)

def moveCM55(leftMotors, rightMotors, leftEncoder, rightEncoder, inches, speed):
    ticks = inches * 0.249
    
    print(ticks)
    if ticks > 0:
        if rightEncoder.getPosition() > -ticks:
            rightMotors.set(speed * -1)
        else:
            rightMotors.set(0.0)
        if leftEncoder.getPosition() < ticks:
            leftMotors.set(speed * 1.02)
        else:
            leftMotors.set(0.0)
    elif ticks < 0:
        if rightEncoder.getPosition() < -ticks:
            rightMotors.set(speed * 1)
        else:
            rightMotors.set(0.0)
        if leftEncoder.getPosition() > ticks:
            leftMotors.set(speed * -1.02)
        else:
            leftMotors.set(0.0)