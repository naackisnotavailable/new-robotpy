import wpilib
from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
from ntcore import _ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs

#from cscore import CameraServer
from funcs import functions as functions
import funcs.autoBalance as balancePID
import funcs.spinPID as spinPID




class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #self.camera = CameraServer.startAutomaticCapture()
        #self.camera.setResolution(320, 240)
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

        self.myDrive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)
        self.stick = wpilib.XboxController(0) # its something 0-5 lol

        self.spinPID = spinPID.PID()
        self.balancePID = balancePID.PID()

    def teleopPeriodic(self):
        functions.drive(self.stick, self.myDrive)
        self.angle = self.gyro.getAngle()
        self.roll = self.gyro.getRoll()


        

if __name__ == "__main__":
    wpilib.run(Robot)