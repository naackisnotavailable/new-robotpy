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
        self.lim = wpilib.DigitalInput(0)
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
         self.gPos,
         self.gpi) = initialize()
        self.on = 0
        self.on2 = 0
        self.on3 = 0
        self.slowed = 0
        self.interrupted = False
        self.interrupted1 = False
        self.autonSwiv = swivelPA.PID()
        self.called = 0


        functions.setGPos(self.grabEncoder)

        self.moveA = aCs.moveCm(self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2)

        self.stageC = 0

        self.stageCount = 0

        self.tempCount = 0


        #auton 0: place and exit community; MAKE SURE TO NOT BE BEHIND CHARGE STATION (PLEASE)
        #auton 1: place and balance to charge station
        #auton 2: drive immediately out of community ; SETUP FACING FORWARD
        self.auton = 0


    def autonomousPeriodic(self):
        if self.auton == 0:

            if self.stageC == 0:
                self.moveA.main(-24)

                if self.moveA.checkCompletion():
                    self.stageC +=1


            elif self.stageC == 1:
                outC = aCs.moveOut(self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.io, self.ioEncoder, self.exPID, self.autonSwiv, self.grabby)

                if outC:
                    self.stageC +=1

            elif self.stageC == 2:
                self.moveA.main(2)
                if self.moveA.checkCompletion() == True:
                    self.tempCount += 1
                    if self.tempCount > 50:
                        self.grabby.set(-0.3)
                        self.stageC += 1
                        aCs.editCompC(2)
                        self.tempCount = 0
            elif self.stageC == 3:
                self.moveA.main(-23)
                self.tempCount += 1
                if self.tempCount > 50:
                    aCs.moveIn(self.lift, self.liftEncoder, self.grab, self.grabEncoder, self.grabby, self.io, self.exPID, self.ioEncoder, self.autonSwiv)
                if self.liftEncoder.getPosition() > -6:
                    self.stageC += 1
            elif self.stageC == 4:
                self.moveA.main(-145)
        
        if self.auton == 1: #wip
            if self.stageC == 0:
                self.moveA.main(-24)

                if self.moveA.checkCompletion():
                    self.stageC +=1


            elif self.stageC == 1:
                outC = aCs.moveOut(self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.io, self.ioEncoder, self.exPID, self.autonSwiv, self.grabby)

                if outC:
                    self.stageC +=1

            elif self.stageC == 2:
                self.moveA.main(2)
                if self.moveA.checkCompletion() == True:
                    self.tempCount += 1
                    if self.tempCount > 50:
                        self.grabby.set(-0.3)
                        self.stageC += 1
                        aCs.editCompC(2)
                        self.tempCount = 0
            elif self.stageC == 3:
                self.moveA.main(-23)
                self.tempCount += 1
                if self.tempCount > 50:
                    aCs.moveIn(self.lift, self.liftEncoder, self.grab, self.grabEncoder, self.grabby, self.io, self.exPID, self.ioEncoder, self.autonSwiv)
                if self.liftEncoder.getPosition() > -6:
                    self.stageC += 1
            elif self.stageC == 4:
                self.moveA.main(-35)
                if self.moveA.checkCompletion() == True:
                    print('balance engaged')
                    self.balancePID(self.gyro.getPitch(), self.leftMotors, self.rightMotors)



        if self.auton == 2:
            self.moveA.main(150)
            
        
    def teleopInit(self):
        functions.setGPos(self.grabEncoder)

    def teleopPeriodic(self):
        liftLimit = self.lim.get()


        self.slowed = functions.drive(self.leftTalon1,
                                      self.leftTalon2,
                                      self.rightTalon1,
                                      self.rightTalon2,
                                      self.stick, self.myDrive, self.slowed)
        
        functions.table(self.stick2, self.tableMotor)
    

        functions.intake(self.stick2, self.bottomIn, self.topIn, self.io, self.ioEncoder, self.exPID, self.interrupted, self.interrupted1)

        functions.grab(self.grabby, self.grabbyEncoder, self.grab, self.grabEncoder, self.stick2, self.interrupted, self.interrupted1)

        self.interrupted = functions.moveOut(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2, liftLimit)
        self.interrupted1 = functions.moveIn(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2, liftLimit)

        functions.balanceCheck(self.stick, self.gyro, self.leftMotors, self.rightMotors, self.balancePID, self.spinPID)
        functions.lift(self.lift, self.liftEncoder, self.extendPID2, self.stick2, self.interrupted, self.interrupted1, liftLimit)

if __name__ == "__main__":
    wpilib.run(Robot)