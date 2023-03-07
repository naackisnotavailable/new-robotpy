# auton go back 29 and then forward to 20 to place

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
from funcs import swivelPA
from funcs import autonComms as aCs
class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #self.camera = CameraServer.startAutomaticCapture()
        #self.camera.setResolution(320, 240)
        (self.leftTalon1,
         self.leftTalon2,
         self.rightTalon1, 
         self.rightTalon2,
         self.leftMotors, 
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
         self.grabbyEncoder,
         self.swP,
         self.gPos) = initialize()
        self.on = 0
        self.on2 = 0
        self.on3 = 0
        self.slowed = 0
        self.interrupted = False
        self.interrupted1 = False
        self.autonSwiv = swivelPA.PID()
        self.called = 0


        functions.setGPos(self.grabEncoder)

        self.moveBack1 = aCs.moveCm(self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2, 20)

        self.stage1C = False


    def autonomousPeriodic(self):
        if self.stage1C == False:
            self.moveBack1.main()
        #    if self.moveBack1.checkCompletion() == True:
        #        self.stage1C = aCs.moveOut(self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.io, self.ioEncoder, self.exPID, self.autonSwiv, self.grabby)
        #
        #if self.stage1C == True:
        #    aCs.moveIn()
            
        
#
    def teleopPeriodic(self):
        self.slowed = functions.drive(self.leftTalon1,
                                      self.leftTalon2,
                                      self.rightTalon1,
                                      self.rightTalon2,
                                      self.stick, self.myDrive, self.slowed)
        
        functions.table(self.stick2, self.tableMotor)
    

        functions.intake(self.stick2, self.bottomIn, self.topIn, self.io, self.ioEncoder, self.exPID, self.interrupted, self.interrupted1)

        functions.grab(self.grabby, self.grab, self.grabEncoder, self.stick2, self.interrupted, self.interrupted1)


        self.interrupted = functions.moveOut(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2)
        self.interrupted1 = functions.moveIn(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2)

        self.timer, self.on3 = functions.balanceCheck(self.stick, self.gyro, self.leftMotors, self.rightMotors, self.balancePID, self.spinPID, self.timer, self.on3)
        functions.lift(self.lift, self.liftEncoder, self.extendPID2, self.stick2, self.interrupted, self.interrupted1)

if __name__ == "__main__":
    wpilib.run(Robot)