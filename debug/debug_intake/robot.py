import wpilib
from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
from ntcore import _ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)

    def teleopPeriodic(self):
        self.io.set(0.5)


        

if __name__ == "__main__":
    wpilib.run(Robot)