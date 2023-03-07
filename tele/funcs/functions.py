import time
import ctre
from funcs import swivelP

swP = swivelP.PID()

on1 = 0
on2 = 0

gPos = 0

def setGPos(grabEncoder):
    global gPos
    gPos = grabEncoder.getPosition()

def drive(leftTalon1, leftTalon2, rightTalon1, rightTalon2, stick, drive, slowed):
    b = stick.getBButtonPressed()
    if b == True:
        slowed += 1
    if slowed % 2 == 1:
        lX = stick.getLeftX() * 0.15
        #Sameer drive if needed
        #lX = stick.getRightX() * 0.15
        lY = stick.getLeftY() * 0.15
        leftTalon1.setNeutralMode(ctre._ctre.NeutralMode.Brake)
        leftTalon2.setNeutralMode(ctre._ctre.NeutralMode.Brake)
        rightTalon1.setNeutralMode(ctre._ctre.NeutralMode.Brake)
        rightTalon2.setNeutralMode(ctre._ctre.NeutralMode.Brake)
    else:
        lX = stick.getLeftX()
        #Sameer drive if needed
        #lX = stick.getRightX()
        lY = stick.getLeftY()
        leftTalon1.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        leftTalon2.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        rightTalon1.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        rightTalon2.setNeutralMode(ctre._ctre.NeutralMode.Coast)
    if lX <= 1.0 and lY <= 1.0:
        drive.curvatureDrive(lX, lY, True)
    else:
        raise Exception("safety toggle, one or more inputs > 1")
    return slowed
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID, timer, on3):
    if stick.getAButton() == True:
        if on3 % 2 == 1:
            if timer < 50:
                leftMotors.set(0.0)#0.5)
                rightMotors.set(0.0)#-0.5)
                time.sleep(0.01)
                timer += 1
            if timer >= 50:
                print('engaged')
                if abs(gyro.getAngle()) >= 30:
                    print('spinning: ' + str(gyro.getYaw()))
                    spinPID.main(gyro.getYaw(), leftMotors, rightMotors)
                else:
                    balancePID.main(gyro.getPitch(), leftMotors, rightMotors)
                    print('balancing: ' + str(gyro.getPitch()))
                if stick.getAButton() == False:
                    timer = 0
        else:
            on += 1
    return timer, on3
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
    print(a, c)

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
def lift(lift, liftEncoder, exPID2, stick2, a, b):
    if a == False and b == False:
        if liftEncoder.getPosition() > 0.1:
            print('disabled')
            lift.set(0.0)
        elif liftEncoder.getPosition() < -105:
            print('disabled')
            lift.set(0.0)
        else:
            spd = stick2.getLeftY()
            if spd < 0:
                spd = -1*(spd**2)
            elif spd > 0:
                spd = spd**2
            else:
                spd = 0

            lift.set(spd)

            #if spd < 0:
            #    spd = -1*(spd**2)
            #elif spd > 0 :
            #    spd = spd**2
            #lift.set(spd)

            #if stick2.getLeftBumper() == True:
            #    lift.set(exPID2.main(liftEncoder, True))
            #elif stick2.getLeftBumper() == False:
            #    lift.set(exPID2.main(liftEncoder, False))
    
def grab(grabby, grab, grabEncoder, stick2, a, b):
    global gPos
    if a == False and b == False:
        curr = grabby.getOutputCurrent() / 100
        if stick2.getRightY() < -0.1 :
            print('closing')
            grabby.set(0.4 - curr)
        elif stick2.getRightY() > 0.1:
            print('opening')
            grabby.set(-0.2 + curr)

        if abs(stick2.getRightTriggerAxis()) < 0.01 and abs(stick2.getLeftTriggerAxis()) < 0.01:
            swP.main(grabEncoder.getPosition(), grab, gPos)
            print('BRAKE ENGAGED')


        else:
            if stick2.getLeftTriggerAxis() > 0.1:
                print('down')
                grab.set(-0.5*(stick2.getLeftTriggerAxis()**2))
            elif stick2.getRightTriggerAxis() > 0.1:
                print('up')
                grab.set(0.5*stick2.getRightTriggerAxis()**2)
            else:
                grab.set(0.0)
            gPos = grabEncoder.getPosition()


def moveOut(io, ioEncoder, exPID, grab, grabEncoder, lift, liftEncoder, grabby, stick2):
    curr = grabby.getOutputCurrent() / 100
    if stick2.getRightBumper() == True:
        global gPos
        gPos = grabEncoder.getPosition()

        interrupted = True

        print('closing')
        grabby.set(0.4 - curr)

        io.set(exPID.main(ioEncoder, True)) # intake moves out
        print('liftpos: ' + str(liftEncoder.getPosition()))

        if liftEncoder.getPosition() > -45: #lift begins moving
            lift.set(-0.4)
        else:
            lift.set(0.0)

        grab.set(-0.1)
    else:
        interrupted = False
    return interrupted

def moveIn(io, ioEncoder, exPID, grab, grabEncoder, lift, liftEncoder, grabby, stick2):
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

        grab.set(-0.1)

        if grabEncoder.getPosition() < -1:
            print('running t2')

            if liftEncoder.getPosition() < -5: #lift begins moving
                print('running t3')
                lift.set(0.4)
            else:
                lift.set(0.0)
        else:
            lift.set(0.0)
    else:
        interrupted = False
    return interrupted