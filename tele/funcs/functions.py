import time
def drive(stick, drive):
    lX = stick.getLeftX()
    lY = stick.getLeftY()
    if lX <= 1.0 and lY <= 1.0:
        drive.curvatureDrive(lX, lY, True)
    else:
        raise Exception("safety toggle, one or more inputs > 1")
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID):
    print('called')
    if stick.getAButton() == True:
        leftMotors.set(0.5)
        rightMotors.set(-0.5)
        time.sleep(1.0)
        leftMotors.set(0.0)
        rightMotors.set(0.0)
        while True:
            print('engaged')
            if gyro.getAngle() >= 15:
                print('spinning: ' + str(gyro.getAngle()))
                spinPID.main(gyro.getAngle(), leftMotors, rightMotors)
            else:
                balancePID.main(gyro.getPitch(), leftMotors, rightMotors)
                print('balancing: ' + str(gyro.getPitch()))
            if stick.getBButton() == True:
                break
def getPose(inst):
    return inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])
def table(stick2, table):
    if stick2.getYButton() == True:
        table.set(0.125)
    elif stick2.getBButton() == True:
        table.set(-0.125)
    else:
        table.set(0.0)
def intake(stick2, b, t, io):
    a = stick2.getXButton()
    if a == True:
        b.set(-0.75)
        t.set(0.75)
    elif a == False:
        b.set(0.0)
        t.set(0.0)
    io.set(stick2.getRightY())
