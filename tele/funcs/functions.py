from funcs import autoBalance as balancePID
from funcs import spinPID

def drive(stick, drive):
    drive.curvatureDrive(stick.getLeftX(), stick.getLeftY(), True)
    drive.curvatureDrive(stick.getLeftX(), stick.getLeftY(), True)
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID):
    if stick.getAButtonPressed() == True:
            if gyro.getAngle() >= 15:
                spinPID.main(gyro.getAngle(), leftMotors, rightMotors)
            else:
                balancePID.main(gyro.getRoll(), leftMotors, rightMotors)
def getPose(inst):
    return inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])
def table(stick, table):
    if stick.getRightX() > 0.05:
        table.set(stick.getRightX())
    else:
        table.set(0.0)