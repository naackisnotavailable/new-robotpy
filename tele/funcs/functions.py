def drive(stick, drive):
    lX = stick.getLeftX()
    lY = stick.getLeftY()
    if lX <= 1.0 and lY <= 1.0:
        drive.curvatureDrive(lX, lY, True)
    else:
        raise Exception("safety toggle, one or more inputs > 1")
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID):
    if stick.getAButton() == True:
        if gyro.getAngle() >= 15:
            print('spinning: ' + str(gyro.getAngle()))
            spinPID.main(gyro.getAngle(), leftMotors, rightMotors)
        else:
            balancePID.main(gyro.getRoll(), leftMotors, rightMotors)
            print('balancing: ' + str(gyro.getRoll()))
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
def encoderSafetyChecks(pos) -> bool:
    if abs(pos) < 1:
        return True
    else:
        return False
def testEncoders(io, ioEncoder, exPID):
    pos = ioEncoder.getPosition()
    spd = exPID.main(io, ioEncoder)
    io.set(spd)
    #io.set(-0.4)
    #if encoderSafetyChecks(pos) == False:
    #    io.set(0.0)
    #elif encoderSafetyChecks(pos) == True:
    #    io.set(0.5)
    #if pos > 1:
    #    io.set(-0.1)
    #elif pos <1:
    #    io.set(0.1)
    print(str(pos))