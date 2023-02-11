from funcs import autoBalance as balancePID
from funcs import spinPID

def drive(stick, drive):
    drive.curvatureDrive(stick.getLeftX(), stick.getLeftY(), True)
    drive.curvatureDrive(stick.getLeftX(), stick.getLeftY(), True)
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID):
    if stick.getBButtonPressed() == True:
            while True:
                if gyro.getAngle() >= 15:
                    spinPID.main(gyro.getAngle(), leftMotors, rightMotors)
                else:
                    balancePID.main(gyro.getRoll(), leftMotors, rightMotors)
                    
                if stick.getYButtonPressed() == True:
                    break
def getPose(inst):
    return inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])
def table(stick, table):
    table.set(stick.getRightX())