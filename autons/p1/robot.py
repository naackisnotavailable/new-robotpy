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
            self.wheelSpeeds.desaturate(10.0)
            print('wheelSpeeds: ' + str(self.wheelSpeeds))
            self.left.set(self.wheelSpeeds.left / 20)
            self.right.set(self.wheelSpeeds.right / 20)

        except IndexError as e:
            print('uh oh spaghettio')
        

if __name__ == "__main__":
    wpilib.run(Robot)