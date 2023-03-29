# auton go back 29 and then forward to 20 to place
import wpilib
#import wpilib.GenericHID.RumbleType;
from wpilib.drive import DifferentialDrive
import wpilib.drive
import rev
import ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs
from wpimath import geometry as geo
#from cscore import CameraServer
#import cscore as cs
from funcs import functions
from funcs import autoBalance as balancePID
from funcs import spinPID as spinPID 
from funcs import __init__ as initialize
from funcs import swivelPA
import commands2 as cmds
import commands2.cmd
#from robotcontainer import RobotContainer
from wpimath import trajectory
from wpimath import geometry as geo
from wpimath import controller
from wpimath import kinematics as kine

#from subsystems import drivetrain



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
         self.gpi,
         self.led,
         self.leftEncoder,
         self.rightEncoder) = initialize()
        self.on = 0
        self.on2 = 0
        self.on3 = 0
        self.slowed = 0
        self.interrupted = False
        self.interrupted1 = False
        self.autonSwiv = swivelPA.PID()
        self.called = 0


        functions.setGPos(self.grabEncoder)

        #self.container = RobotContainer(self.gyro, self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2)

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
        #self.dt = drivetrain.Drivetrain(self.gyro, self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2)
        #self.dt.resetOdometry(geo.Pose2d(0, 0, 0))
        #self.dt.resetEncoders()
        #"""This autonomous runs the autonomous command selected by your RobotContainer class."""
        #self.autonomousCommand = self.container.getAutonomousCommand()
#
        #if self.autonomousCommand:
        #    self.autonomousCommand.schedule()
        self.timer.start()
        

    def autonomousPeriodic(self) -> None:
        #Auton 0 = move out long side, set facing node  against nodes, 160 inches does not place curves towards 30 side
        #auton 1 = place and move out, set facing node 24 inches from node legs, moves out 85 inches, short side


        
        
        
        
        auton = 1
        if auton == 0:
            functions.moveCM(self.leftMotors, self.rightMotors, self.leftEncoder, self.rightEncoder, -160, 0.1)# -84 for shortside 0 for middle and -160 for long side
        elif auton == 1:
            functions.moveOutAuton(self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.io,self.ioEncoder, self.exPID, self.autonSwiv, self.grabby )
            if self.timer.get() > 6.5 and self.timer.get() < 8.7:
                functions.moveCM(self.leftMotors, self.rightMotors, self.leftEncoder, self.rightEncoder, 24, 0.1)
            if self.timer.get() > 7.8:
                #self.grab.set(0.09)
                self.grabby.set(-0.07) 
                #NEGATIVE IS OPEN
            if self.timer.get() > 9.2:
                functions.moveCM(self.leftMotors, self.rightMotors, self.leftEncoder, self.rightEncoder, 0, 0.2) # -84 for shortside 0 for middle and -160 for long side
                #self.grabby.set(-0.07) 
        #elif auton == 2:
        #    if self.timer.get() < 6:
        #        functions.moveCM(self.leftMotors, self.rightMotors, self.leftEncoder, self.rightEncoder, 24, 0.1)
        #    if self.timer.get() > 6:
        #        functions.moveCM(self.leftMotors, self.rightMotors, self.leftEncoder, self.rightEncoder, -84, 0.2)
        
        
        
        
        

        
        #26.5 inches per second at 0.1
        #114 inches at 3.6 sec
        #105 inches at 3.6
        #114
        #116
        #117
        #116
        

            
        
    def teleopInit(self):
        functions.setGPos(self.grabEncoder)


    def teleopPeriodic(self):

        liftLimit = self.lim.get()
        #print('grabpos: ' + str(self.grabEncoder.getPosition()))
        print('liftpos: ' + str(self.liftEncoder.getPosition()))
        #print('rightpos: ' + str(self.rightEncoder.getPosition()))
        #print('leftpos: ' + str(self.leftEncoder.getPosition()))
        self.slowed = functions.drive(self.leftTalon1,
                                      self.leftTalon2,
                                      self.rightTalon1,
                                      self.rightTalon2,
                                      self.stick, self.myDrive, self.slowed, self.led)
        
        functions.table(self.stick2, self.tableMotor)
    
        #print('liftpos: ' + str(self.liftEncoder.getPosition()))
        #functions.shelfHeight(self.lift, self.liftEncoder, self.stick2, self.led)

        functions.intake(self.stick2, self.bottomIn, self.topIn, self.io, self.ioEncoder, self.exPID, self.interrupted, self.interrupted1)

        functions.grab(self.grabby, self.grabbyEncoder, self.grab, self.grabEncoder, self.stick2, self.interrupted, self.interrupted1)

        self.interrupted = functions.moveOut(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2, liftLimit)
        self.interrupted1 = functions.moveIn(self.io, self.ioEncoder, self.exPID, self.grab, self.grabEncoder, self.lift, self.liftEncoder, self.grabby, self.stick2, liftLimit)

        functions.balanceCheck(self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2, self.stick, self.gyro, self.leftMotors, self.rightMotors, self.balancePID, self.spinPID, self.led)
        functions.lift(self.lift, self.liftEncoder, self.extendPID2, self.stick2, self.interrupted, self.interrupted1, liftLimit)
        #functions.rumble(self.liftEncoder, self.stick2)
        #if self.liftEncoder.getPosition > -75 or self.liftEncoder.getPosition < 0:
        #    self.stick2.setRumble(GenericHID.RumbleType.kRightRumble, 1)


if __name__ == "__main__":
    wpilib.run(Robot)