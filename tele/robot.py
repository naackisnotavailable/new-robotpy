import wpilib
from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
from ntcore import _ntcore
import wpilib.interfaces
import time
#from cscore import CameraServer
import functions as functions
#import vision



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

        self.leftMotors = wpilib.MotorControllerGroup(self.leftTalon1, self.leftTalon2)
        self.rightMotors = wpilib.MotorControllerGroup(self.rightTalon1, self.rightTalon2)

        self.myDrive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)
        self.stick = wpilib.XboxController(0) # its something 0-5 lol

    def teleopPeriodic(self):
        self.myDrive.curvatureDrive(-self.stick.getLeftY(), self.stick.getLeftX(), False) #consider squaring the controller value to be more precise at low speeds and still fast at high speeds
        print(self.leftTalon1.get())
        print(self.rightTalon1.get())

        if abs(self.stick.getRightX() >= 0.05):
            self.stick.getRightX()
            self.leftMotors.set(self.stick.getRightX())
            self.rightMotors.set(-self.stick.getRightX())
        #frame = vision.main(self.camera)
        #print(str(frame)))
        

if __name__ == "__main__":
    wpilib.run(Robot)