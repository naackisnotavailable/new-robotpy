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
        (self.leftMotors, 
         self.rightMotors, 
         self.gyro, 
         self.spinPID, 
         self.balancePID, 
         self.exPID, 
         self.stick, 
         self.stick2, 
         self.myDrive, 
         self.tableMotor, 
         self.bottomIn, 
         self.topIn, 
         self.io, 
         self.ioEncoder, 
         self.ntinst, 
         self.timer, 
         self.lift, 
         self.liftEncoder, 
         self.extendPID2,
         self.grab,
         self.grabEncoder,
         self.grabby,
         self.grabbyEncoder) = initialize()
    def teleopPeriodic(self):
        functions.drive(self.stick, self.myDrive)
        #self.timer = functions.balanceCheck(self.stick, self.gyro, self.leftMotors, self.rightMotors, self.balancePID, self.spinPID, self.timer)
       # functions.table(self.stick2, self.tableMotor)
        functions.intake(self.stick2, self.bottomIn, self.topIn, self.io, self.ioEncoder, self.exPID)
        functions.lift(self.lift, self.liftEncoder, self.extendPID2, self.stick2)
        #functions.grab(self.grabby, self.grab, self.grabEncoder, self.stick2)
        print('grabEncoder' + str(self.grabEncoder.getPosition()))
        #functions.moveOut(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder)

if __name__ == "__main__":
    wpilib.run(Robot)