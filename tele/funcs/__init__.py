import ctre
from navx import AHRS as ahrs
import wpilib
import wpilib.drive
from funcs import autoBalance as balance
import cscore as cs
from funcs import spinPID as spin
import rev
import ntcore
from funcs import extendPID as ex
from funcs import extendPID2 as ex2
from funcs import swivelP

def __init__():
    leftTalon1 = ctre.WPI_TalonFX(5)
    leftTalon2 = ctre.WPI_TalonFX(6)
    rightTalon1 = ctre.WPI_TalonFX(7)
    rightTalon2 = ctre.WPI_TalonFX(8)

    leftTalon1.configFactoryDefault()
    leftTalon2.configFactoryDefault()
    rightTalon1.configFactoryDefault()
    rightTalon2.configFactoryDefault()

    leftTalon1.config_kP(0, 0.02, 0)
    leftTalon2.config_kP(0, 0.02, 0)
    leftTalon1.config_kD(0, 0.25, 0)
    leftTalon2.config_kD(0, 0.25, 0)

    rightTalon1.config_kP(0, 0.02, 0)
    rightTalon2.config_kP(0, 0.02, 0)
    rightTalon1.config_kD(0, 0.25, 0)
    rightTalon2.config_kD(0, 0.25, 0)

    leftTalon1.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
    leftTalon2.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
    rightTalon1.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
    rightTalon2.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)

    leftTalon1.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
    leftTalon2.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
    rightTalon1.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
    rightTalon2.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
    gyro = ahrs.create_spi()
    leftMotors = wpilib.MotorControllerGroup(leftTalon1, leftTalon2)
    rightMotors = wpilib.MotorControllerGroup(rightTalon1, rightTalon2)
    spinPID = spin.PID()
    balancePID = balance.PID()
    exPID = ex.PID()
    exPID2 = ex2.PID()
    swP = swivelP.PID()
    stick = wpilib.XboxController(0)
    stick2 = wpilib.XboxController(1)
    myDrive = wpilib.drive.DifferentialDrive(leftMotors, rightMotors)
    myDrive.setDeadband(0.03)
    grab = rev.CANSparkMax(14, rev.CANSparkMax.MotorType.kBrushless)
    grabEncoder = grab.getEncoder()
    grabby = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)
    grabbyEncoder = grabby.getEncoder()
    tableMotor = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)
    bottomIn = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
    topIn = rev.CANSparkMax(11, rev.CANSparkMax.MotorType.kBrushless)
    io = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
    lift = rev.CANSparkMax(12, rev.CANSparkMax.MotorType.kBrushless)
    liftEncoder = lift.getEncoder()
    ntinst = ntcore._ntcore.NetworkTableInstance.getDefault()
    ioEncoder = io.getEncoder()
    ioEncoder.setPosition(0)
    liftEncoder.setPosition(0)
    timer = 0
    gPos = 0
    lift.restoreFactoryDefaults()
    io.restoreFactoryDefaults()
    camera = cs.UsbCamera("usbcam", 0)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    leftTalon1.setNeutralMode(ctre._ctre.NeutralMode.Brake)
    leftTalon2.setNeutralMode(ctre._ctre.NeutralMode.Brake)
    rightTalon1.setNeutralMode(ctre._ctre.NeutralMode.Brake)
    rightTalon2.setNeutralMode(ctre._ctre.NeutralMode.Brake)
    return (leftTalon1, 
            leftTalon2, 
            rightTalon1, 
            rightTalon2, 
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
            gPos)


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