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
        self.leftTalon1 = ctre.TalonFX(5)
        self.leftTalon2 = ctre.TalonFX(6)
        self.rightTalon1 = ctre.TalonFX(7)
        self.rightTalon2 = ctre.TalonFX(8)

        self.leftTalon1.configFactoryDefault()
        self.leftTalon2.configFactoryDefault()
        self.rightTalon1.configFactoryDefault()
        self.rightTalon2.configFactoryDefault()

        self.leftTalon1.config_kP(0, 0.125, 0)
        self.leftTalon2.config_kP(0, 0.125, 0)
        self.leftTalon1.config_kD(0, 0.2, 0)
        self.leftTalon2.config_kD(0, 0.2, 0)

        self.rightTalon1.config_kP(0, 0.125, 0)
        self.rightTalon2.config_kP(0, 0.125, 0)
        self.rightTalon1.config_kD(0, 0.2, 0)
        self.rightTalon2.config_kD(0, 0.2, 0)

        self.leftTalon1.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
        self.leftTalon2.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)

        self.rightTalon1.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
        self.rightTalon2.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)

        self.leftTalon1.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
        self.leftTalon2.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)

        self.rightTalon1.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
        self.rightTalon2.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
        #self.leftMotors = wpilib.MotorControllerGroup(self.leftTalon1, self.leftTalon2)
        #self.rightMotors = wpilib.MotorControllerGroup(self.rightTalon1, self.rightTalon2)
    def autonomousPeriodic(self):
        print('active')
        self.leftTalon1.set(ctre._ctre.ControlMode.Position, 0)
        self.leftTalon2.set(ctre._ctre.ControlMode.Position, 0)

        self.rightTalon1.set(ctre._ctre.ControlMode.Position, 0)
        self.rightTalon2.set(ctre._ctre.ControlMode.Position, 0)

if __name__ == "__main__":
    wpilib.run(Robot)