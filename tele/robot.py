# auton go back 29 and then forward to 20 to place
import wpilib

from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
import ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs
from wpimath import geometry as geo
from cscore import CameraServer
import cscore as cs
from funcs import functions
from funcs import autoBalance as balancePID
from funcs import spinPID as spinPID 
from funcs import __init__ as initialize
from funcs import swivelPA
from funcs import autonComms as aCs
import commands2 as cmds
import commands2.cmd
from robotcontainer import RobotContainer
from wpimath import trajectory
from wpimath import geometry as geo
from wpimath import controller
from wpimath import kinematics as kine

from subsystems import drivetrain



class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.lim = wpilib.DigitalInput(0)
        

        #self.camera = CameraServer.startAutomaticCapture()
        #self.camera.setResolution(320, 240)
        #self.stream = CameraServer.putVideo("Main", 320, 240)

        #self.camera = cs.UsbCamera("usbcam", 0)
        #self.camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
        #self.mjpegServer = cs.MjpegServer("httpserver", 8081)
        #self.mjpegServer.setSource(self.camera)

        #self.mjpeg = self.camera.
        (self.leftTalon1,
         self.leftTalon2,
         self.rightTalon1, 
         self.rightTalon2,
         self.leftMotors, 
         self.rightMotors, 
         self.gyro, 
         self.spinPID, 
         self.balancePID, 
         self.exPID, 
         self.stick, 
         self.stick2, 
         self.myDrive, 
         self.tableMotor, 
         self.bottomIn, 
         self.topIn, 
         self.io, 
         self.ioEncoder, 
         self.ntinst, 
         self.timer, 
         self.lift, 
         self.liftEncoder, 
         self.extendPID2,
         self.grab,
         self.grabEncoder,
         self.grabby,
         self.grabbyEncoder,
         self.swP,
         self.gPos,
         self.gpi) = initialize()
        self.on = 0
        self.on2 = 0
        self.on3 = 0
        self.slowed = 0
        self.interrupted = False
        self.interrupted1 = False
        self.autonSwiv = swivelPA.PID()
        self.called = 0


        functions.setGPos(self.grabEncoder)

        self.container = RobotContainer(self.gyro)

        self.traject = trajectory.TrajectoryGenerator().generateTrajectory(
            start= geo.Pose2d(geo.Translation2d(0, 0), geo.Rotation2d(0, 0)),
            interiorWaypoints= [geo.Translation2d(1, 0)],
            end= geo.Pose2d(geo.Translation2d(1, 0), geo.Rotation2d(0, 0)),
            config= trajectory.TrajectoryConfig(0.4, 2),
        )
        self.ramsete = controller.RamseteController()

        self.timer = wpilib.Timer()

        self.kinematic = kine.DifferentialDriveKinematics(0.544)

    def autonomousInit(self) -> None:
        self.timer.reset()
        self.dt = drivetrain.Drivetrain(self.gyro)
        self.dt.resetOdometry(geo.Pose2d(0, 0, 0))
        self.dt.resetEncoders()
        #"""This autonomous runs the autonomous command selected by your RobotContainer class."""
        #self.autonomousCommand = self.container.getAutonomousCommand()
#
        #if self.autonomousCommand:
        #    self.autonomousCommand.schedule()
        self.timer.start()
        pass

    def autonomousPeriodic(self) -> None:
        t = self.timer.get()
        self.currentPose = self.dt.getPose()
        self.dt.periodic()

        self.desiredPose = self.traject.sample(t)
        self.output = self.ramsete.calculate(self.currentPose, self.desiredPose)
            
        self.wheelSpeeds = self.kinematic.toWheelSpeeds(self.output)
        self.wheelSpeeds.desaturate(0.8)


            
        
    def teleopInit(self):
        functions.setGPos(self.grabEncoder)


    def teleopPeriodic(self):

        liftLimit = self.lim.get()

        self.slowed = functions.drive(self.leftTalon1,
                                      self.leftTalon2,
                                      self.rightTalon1,
                                      self.rightTalon2,
                                      self.stick, self.myDrive, self.slowed)
        
        functions.table(self.stick2, self.tableMotor)
    


        functions.intake(self.stick2, self.bottomIn, self.topIn, self.io, self.ioEncoder, self.exPID, self.interrupted, self.interrupted1)

        functions.grab(self.grabby, self.grabbyEncoder, self.grab, self.grabEncoder, self.stick2, self.interrupted, self.interrupted1)

        self.interrupted = functions.moveOut(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2, liftLimit)
        self.interrupted1 = functions.moveIn(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2, liftLimit)

        functions.balanceCheck(self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2, self.stick, self.gyro, self.leftMotors, self.rightMotors, self.balancePID, self.spinPID)
        functions.lift(self.lift, self.liftEncoder, self.extendPID2, self.stick2, self.interrupted, self.interrupted1, liftLimit)


if __name__ == "__main__":
    wpilib.run(Robot)