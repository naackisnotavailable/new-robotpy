from navx import AHRS as ahrs
import wpilib
import wpilib.drive
from funcs import autoBalance as balance
#import cscore as cs
from funcs import spinPID as spin
import rev
import ntcore
from funcs import extendPID as ex
from funcs import extendPID2 as ex2
from funcs import swivelP
from funcs import grabbyPI as gPI

def __init__():
    leftMotor1 = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
    leftMotor2 = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
    rightMotor1 = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)
    rightMotor2 = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)

    leftMotor1.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
    leftMotor2.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
    rightMotor1.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
    rightMotor2.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)


    gyro = ahrs.create_spi()
    leftMotors = wpilib.MotorControllerGroup(leftMotor1, leftMotor2)
    rightMotors = wpilib.MotorControllerGroup(rightMotor1, rightMotor2)
    spinPID = spin.PID()
    balancePID = balance.PID()
    exPID = ex.PID()
    exPID2 = ex2.PID()
    gpi = gPI.PID()
    swP = swivelP.PID()
    stick = wpilib.XboxController(0)
    stick2 = wpilib.XboxController(1)
    myDrive = wpilib.drive.DifferentialDrive(leftMotors, rightMotors)
    myDrive.setDeadband(0.03)

    tableMotor = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
    bottomIn = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)
    topIn = rev.CANSparkMax(8, rev.CANSparkMax.MotorType.kBrushless)
    lift = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)
    grab = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
    io = rev.CANSparkMax(11, rev.CANSparkMax.MotorType.kBrushless)
    grabby = rev.CANSparkMax(12, rev.CANSparkMax.MotorType.kBrushless)

    led = wpilib.Spark(1)


    grabEncoder = grab.getEncoder()
    grabbyEncoder = grabby.getEncoder()


    liftEncoder = lift.getEncoder()
    leftEncoder = leftMotor1.getEncoder()
    rightEncoder = rightMotor1.getEncoder()
    ntinst = ntcore._ntcore.NetworkTableInstance.getDefault()
    ioEncoder = io.getEncoder()
    ioEncoder.setPosition(0)
    liftEncoder.setPosition(0)
    grabEncoder.setPosition(0)
    leftEncoder.setPosition(0)
    rightEncoder.setPosition(0)
    timer = 0
    gPos = 0
    lift.restoreFactoryDefaults()
    io.restoreFactoryDefaults()

    #wpilib.CameraServer.launch()

    

    #camera = cs.UsbCamera("usbcam", 0)
    #camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)

    return (leftMotor1, 
            leftMotor2, 
            rightMotor1, 
            rightMotor2, 
            leftMotors, 
            rightMotors, 
            gyro, 
            spinPID, 
            balancePID, 
            exPID, 
            stick, 
            stick2, 
            myDrive, 
            tableMotor, 
            bottomIn, 
            topIn, 
            io, 
            ioEncoder, 
            ntinst, 
            timer, 
            lift, 
            liftEncoder, 
            exPID2, 
            grab, 
            grabEncoder, 
            grabby, 
            grabbyEncoder, 
            swP, 
            gPos, 
            gpi,
            led, 
            leftEncoder, 
            rightEncoder) # bro


"""
Change Summary:

Brake P Controller for swivel.
Auton structure laid out + some code to test.
Cleaned up excessive print statemenets
Removed old folders of now useless files
Fixed logic for lift retraction button, incorrect if statement was included


TODO:
Add limits to swivel motor.
Test + debug autonomous.
Tune autobalance PID and set to brake mode.
Retest io motor to check for stalling / whatever that was




"""