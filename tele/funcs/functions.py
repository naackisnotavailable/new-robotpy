import time
def drive(stick, drive):
    lX = stick.getLeftX()
    lY = stick.getLeftY()
    if lX <= 1.0 and lY <= 1.0:
        drive.curvatureDrive(lX, lY, True)
    else:
        raise Exception("safety toggle, one or more inputs > 1")
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID, timer):
    if stick.getAButton() == True:
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
    return timer
def getPose(inst):
    return inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])
def table(stick2, table):
    if stick2.getYButton() == True:
        table.set(0.125)
    elif stick2.getBButton() == True:
        table.set(-0.125)
    else:
        table.set(0.0)
def intake(stick2, b, t, io, ioEncoder, exPID):
    x = stick2.getXButton()
    if x == True:
        b.set(-0.75)
        t.set(0.75)
    elif x == False:
        b.set(0.0)
        t.set(0.0)
    ioC = stick2.getAButton()
    io.set(exPID.main(ioEncoder, ioC))
def lift(lift, liftEncoder, exPID2, stick2):
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
def grab(grabby, grab, grabEncoder, stick2):
    curr = grabby.getOutputCurrent() / 100
    if stick2.getRightY() < -0.1 :
        print('closing')
        grabby.set(0.4 - curr)
    elif stick2.getRightY() > 0.1:
        print('opening')
        grabby.set(-0.2 + curr)
    

    if stick2.getLeftTriggerAxis() > 0.1:
        print('down')
        grab.set(-0.5*(stick2.getLeftTriggerAxis()**2))
    elif stick2.getRightTriggerAxis() > 0.1:
        print('up')
        grab.set(0.5*stick2.getRightTriggerAxis()**2)
    else:
        grab.set(0.0)


def moveOut(io, ioEncoder, exPID, grab, grabEncoder, lift, liftEncoder, grabby, stick2):
    curr = grabby.getOutputCurrent() / 100
    if stick2.getRightBumper() == True:

        print('closing')
        grabby.set(0.4 - curr)

        io.set(exPID.main(ioEncoder, True)) # intake moves out
        print('liftpos: ' + str(liftEncoder.getPosition()))

        if liftEncoder.getPosition() > -50: #lift begins moving
            lift.set(-0.2)
        else:
            lift.set(0.0)

        grab.set(-0.1)

def moveIn(io, ioEncoder, exPID, grab, grabEncoder, lift, liftEncoder, grabby, stick2):
    curr = grabby.getOutputCurrent() / 100
    if stick2.getLeftBumper() == True:
    
        print('opening')
        grabby.set(-0.2 + curr)

        io.set(exPID.main(ioEncoder, True)) # intake moves out
        print('liftpos: ' + str(liftEncoder.getPosition()))

        if liftEncoder.getPosition() < -5: #lift begins moving
            lift.set(0.2)
        else:
            lift.set(0.0)

        grab.set(-0.1)



    
