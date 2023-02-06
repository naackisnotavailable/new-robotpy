from funcs import autoBalance as balancePID
from funcs import spinPID

def drive(stick, drive):
    drive.curvatureDrive(stick.getLeftX(), stick.getLeftY(), True)
    drive.curvatureDrive(stick.getLeftX(), stick.getLeftY(), True)
def balanceCheck(stick, gyro, leftMotors, rightMotors, balancePID, spinPID):
    if stick.getBButtonPressed() == True:
            while True:
                if 1 == 2:
                    spinPID.main(gyro.getAngle(), leftMotors, rightMotors)
                if 2 == 1:
                    balancePID.main(gyro.getRoll(), leftMotors, rightMotors)
                if stick.getYButtonPressed() == True:
                    break