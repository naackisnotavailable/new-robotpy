import wpilib
from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
from ntcore import _ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs
 #hehe simran was here when she was setting up git for sameer

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
        self.gyro = ahrs.create_spi()
        self.leftMotors = wpilib.MotorControllerGroup(self.leftTalon1, self.leftTalon2)
        self.rightMotors = wpilib.MotorControllerGroup(self.rightTalon1, self.rightTalon2)
        self.stick = wpilib.XboxController(0)
        self.stick2 = wpilib.XboxController(1)
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)
        self.drive.setDeadband(0.03)
        self.b = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)

    def teleopPeriodic(self):
        self.b.set(0.5)
        lX = self.stick.getLeftX()
        print('lX: ' + str(lX))
        lY = self.stick.getLeftY()
        print('lY: ' + str(lY))
        if lX <= 1.0 and lY <= 1.0:
            self.drive.curvatureDrive(lX, lY, True)
            print('leftSpeed: ' + str(self.leftMotors.get()))
            print('rightSpeed: ' + str(self.rightMotors.get()))
        else:
            raise Exception("safety toggle, one or more inputs > 1")



        

if __name__ == "__main__":
    wpilib.run(Robot)