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

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.leftTalon1 = ctre.WPI_TalonFX(5)
        self.leftTalon2 = ctre.WPI_TalonFX(6)
        self.rightTalon1 = ctre.WPI_TalonFX(7)
        self.rightTalon2 = ctre.WPI_TalonFX(8)
        self.leftTalon1.configFactoryDefault()
        self.leftTalon2.configFactoryDefault()
        self.rightTalon1.configFactoryDefault()
        self.rightTalon2.configFactoryDefault()

        (self.left, self.right, self.gyro, self.spinPID, self.balancePID, self.stick, self.drive, self.tableMotor, self.inst) = initialize()
        self.left = wpilib.MotorControllerGroup(self.leftTalon1, self.leftTalon2)
        self.right = wpilib.MotorControllerGroup(self.rightTalon1, self.rightTalon2)

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.allMotors = (self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2)

        self.gyro = ahrs.create_spi()

        #timer
        self.timer = wpilib.Timer()
        self.timer.reset()
    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()
    def autonomousPeriodic(self):
        t = self.timer.get()

        self.pose = self.inst.getTable("limelight").getEntry("botpose").getDoubleArray([6])

        try:
            self.pose2 = geo.Pose2d(self.pose[0], self.pose[1], self.pose[2])
            self.desiredPose = self.trajectory1.sample(t)
            self.output = self.ramsete.calculate(self.pose2, self.desiredPose)
            self.wheelSpeeds = self.kinematic.toWheelSpeeds(self.output)
            self.wheelSpeeds.desaturate(0.8)
            self.drive.WheelSpeeds.left(self.wheelSpeeds.left)
            self.drive.WheelSpeeds.right(self.wheelSpeeds.right)
        except IndexError as e:
            print('uh oh spaghettio')
        

if __name__ == "__main__":
    wpilib.run(Robot)