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



    def autonomousPeriodic(self):  #test just drivetrain movement before anything else.

        def moveCm(rot):
            self.called += 1
            
            if self.called == 1:
                self.leftTalon1.setSelectedSensorPosition(0, 0, 0)
                self.leftTalon2.setSelectedSensorPosition(0, 0, 0)
                self.rightTalon1.setSelectedSensorPosition(0, 0, 0)
                self.rightTalon2.setSelectedSensorPosition(0, 0, 0)

            ticks = rot * 9550

            self.leftTalon1.set(ctre._ctre.ControlMode.Position, ticks)
            self.leftTalon2.set(ctre._ctre.ControlMode.Position, ticks)
            
            self.rightTalon1.set(ctre._ctre.ControlMode.Position, ticks)
            self.rightTalon2.set(ctre._ctre.ControlMode.Position, ticks)

        

        print('grab pos: ' + str(self.grabEncoder.getPosition()))
        moveCm(1)

        print('active')

        curr = self.grabby.getOutputCurrent() / 100

        

        # part one; place preloaded cube

        # Move 24 in back from start to place preloaded cube, CHECK DIRECTION BEFORE TESTING


        #print('closing')
        #self.grabby.set(0.55 - curr)
#
        #self.io.set(self.exPID.main(self.ioEncoder, True)) # intake moves out
#
#
        #print('liftpos: ' + str(self.liftEncoder.getPosition()))
#
        #if self.liftEncoder.getPosition() > -60: #lift begins moving
        #    self.lift.set(-0.4)
        #else:
        #    self.lift.set(0.0)
#
#
#
        #if self.liftEncoder.getPosition() > -55:
        #    self.grab.set(-0.1)
        #else:
        #    self.autonSwiv.main(self.grabEncoder.getPosition(), self.grab, 21)
#
#
        #
        #if self.grabEncoder.getPosition() > 8:
        #    if self.liftEncoder.getPosition() < -60 and self.liftEncoder.getPosition() > -75:
        #        self.lift.set(-0.25)
        #    else:
        #        self.lift.set(0.0)
        #
#
        #    
#
#
#
        #if self.liftEncoder.getPosition() < -70 and self.grabbyEncoder.getPosition() > 4:
        #    print('opening')
        #    self.grabby.set(-0.2 + curr)
#
#
        ##NEED TO CHECK WHEN EXTENDED, THEN PLACE
#
        ##part 2; move everything back in // NOT WORKING PROBABLY
#
        #if False == True:
        #    curr = self.grabby.getOutputCurrent() / 100
        #    print('SWIVEL ENCODER: ' + str(self.grabEncoder.getPosition()))
#
#
        #    print('running t1')
        #    print('closing')
        #    self.grabby.set(0.4 - curr)
        #    self.io.set(self.exPID.main(self.ioEncoder, True)) # intake moves out
        #    print('liftpos: ' + str(self.liftEncoder.getPosition()))
        #    self.grab.set(-0.1)
        #    if self.grabEncoder.getPosition() < -0.5:
        #        print('running t2')
        #        if self.liftEncoder.getPosition() < -5: #lift begins moving
        #            print('running t3')
        #            self.lift.set(0.2)
        #        else:
        #            self.lift.set(0.0)
        #    else:
        #        self.lift.set(0.0)
        #
        ## After moving back in, drive directly backward for currently undetermined distance
        ## After leaving community, drive up to charge station and engage PID until end of autonomous
        #if False == True:
        #    self.spinPID(self.gyro.getYaw(), self.leftMotors, self.rightMotors, 180)
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