import wpilib
import wpilib.drive
import ctre
import wpilib.interfaces
import time
from ntcore import _ntcore
from wpimath import controller as control
from navx import AHRS as ahrs
import math
from funcs import __init__ as initialize
from wpimath import geometry as geo
from wpimath import kinematics as kine
from wpimath import units as units
class Robot(wpilib.TimedRobot):
    def robotInit(self):
                # NEED TO UPDATE MOTOR ID
        (self.left, self.right, self.gyro, self.spinPID, self.balancePID, self.stick, self.drive, self.tableMotor, self.inst, self.ramsete, self.trajectory1, self.time, self.kinematic) = initialize()
        self.kinematic = kine.DifferentialDriveKinematics(4)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.gyro = ahrs.create_spi()
        self.time.reset()
    def autonomousInit(self):
        self.time.reset()
        self.time.start()
    def autonomousPeriodic(self):
        t = self.time.get()
        print('t: '+ str(t))
        self.pose = self.inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])
        print('limepose: ' + str(self.pose))
        try:
            self.pose2 = geo.Pose2d(self.pose[0], self.pose[1], self.pose[2])
            self.desiredPose = self.trajectory1.sample(t)
            print('desPose: ' + str(self.desiredPose))
            self.output = self.ramsete.calculate(self.pose2, self.desiredPose)
            print('out: ' + str(self.output))
            self.wheelSpeeds = self.kinematic.toWheelSpeeds(self.output)
            self.wheelSpeeds.desaturate(0.5)
            print('wheelSpeeds: ' + str(self.wheelSpeeds))
            #self.wheelString = str(self.wheelSpeeds).removeprefix('DifferentialDriveWheelSpeeds(left=').removesuffix(')')
            #self.wheelList = self.wheelString.split(', ')
            #self.leftString = self.wheelList[0]
            #self.rightString = self.wheelList[1].removeprefix('right=')
            #print('\nleft: ' + self.leftString)
            #print('\nright: ' + self.rightString)
            #self.leftSpeed = float(self.leftString)
            #self.rightSpeed = float(self.rightString)
            #self.drive.WheelSpeeds.left(self.leftSpeed)
            #self.drive.WheelSpeeds.right(self.rightSpeed)
            self.left.set(self.wheelSpeeds.left)
            self.right.set(self.wheelSpeeds.right)
           # print('leftspeed: ' + str(units.feetToMeters(self.wheelSpeeds.left_fps)))
           # print('rightspeed: ' + str(units.feetToMeters(self.wheelSpeeds.right_fps)))

        except IndexError as e:
            print('uh oh spaghettio')
        

if __name__ == "__main__":
    wpilib.run(Robot)