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
        self.gyro = ahrs.create_spi()
    def teleopPeriodic(self):
        print('ang: ' + str(self.gyro.getAngle()))
        print('rol: ' + str(self.gyro.getPitch()))


        

if __name__ == "__main__":
    wpilib.run(Robot)