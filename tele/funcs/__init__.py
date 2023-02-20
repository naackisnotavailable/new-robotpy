import ctre
from navx import AHRS as ahrs
import wpilib
import wpilib.drive
from funcs import autoBalance as balance
from funcs import spinPID as spin
import rev
import ntcore
from funcs import extendPID

def __init__():
    leftTalon1 = ctre.WPI_TalonFX(5)
    leftTalon2 = ctre.WPI_TalonFX(6)
    rightTalon1 = ctre.WPI_TalonFX(7)
    rightTalon2 = ctre.WPI_TalonFX(8)
    leftTalon1.configFactoryDefault()
    leftTalon2.configFactoryDefault()
    rightTalon1.configFactoryDefault()
    rightTalon2.configFactoryDefault()
    gyro = ahrs.create_spi()
    leftMotors = wpilib.MotorControllerGroup(leftTalon1, leftTalon2)
    rightMotors = wpilib.MotorControllerGroup(rightTalon1, rightTalon2)
    spinPID = spin.PID()
    balancePID = balance.PID()
    exPID = extendPID.PID()
    stick = wpilib.XboxController(0)
    stick2 = wpilib.XboxController(1)
    myDrive = wpilib.drive.DifferentialDrive(leftMotors, rightMotors)
    myDrive.setDeadband(0.03)
    tableMotor = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)
    bottomIn = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
    topIn = rev.CANSparkMax(11, rev.CANSparkMax.MotorType.kBrushless)
    io = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
    ntinst = ntcore._ntcore.NetworkTableInstance.getDefault()
    ioEncoder = io.getEncoder()
    ioEncoder.setPosition(0)
    return (leftMotors, rightMotors, gyro, spinPID, balancePID, exPID, stick, stick2, myDrive, tableMotor, bottomIn, topIn, io, ioEncoder, ntinst)