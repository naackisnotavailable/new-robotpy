import wpilib
import wpilib.drive
import ctre
import wpilib.interfaces
import time
from func import autoBalance
from navx import AHRS as ahrs

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

        self.leftMotors = wpilib.MotorControllerGroup(self.leftTalon1, self.leftTalon2)
        self.rightMotors = wpilib.MotorControllerGroup(self.rightTalon1, self.rightTalon2)

        self.allMotors = (self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2)

        self.time = 0

        self.balance = autoBalance.PID()
        self.gyro = ahrs.create_spi()

    def autonomousPeriodic(self):
        self.balance.main(self.gyro.getRoll, self.leftMotors, self.rightMotors)
        

if __name__ == "__main__":
    wpilib.run(Robot)
