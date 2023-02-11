import wpilib
from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
import ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs
from wpimath import geometry as geo
#from cscore import CameraServer
from funcs import functions
from funcs import autoBalance as balancePID
from funcs import spinPID as spinPID
from funcs import __init__ as initialize

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #self.camera = CameraServer.startAutomaticCapture()
        #self.camera.setResolution(320, 240)
        (self.leftMotors, self.rightMotors, self.gyro, self.spinPID, self.balancePID, self.stick, self.myDrive, self.tableMotor, self.ntinst) = initialize()
    def teleopPeriodic(self):
        functions.drive(self.stick, self.myDrive)
        functions.balanceCheck(self.stick, self.gyro, self.leftMotors, self.rightMotors, self.balancePID, self.spinPID)
        functions.table(self.stick, self.tableMotor)
        #self.currentPose = functions.getPose(self.ntinst)


if __name__ == "__main__":
    wpilib.run(Robot)