import ctre
from navx import AHRS as ahrs
import wpilib
import wpilib.drive
from funcs import autoBalance as balance
from funcs import spinPID as spin
import rev

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
    stick = wpilib.XboxController(0)
    myDrive = wpilib.drive.DifferentialDrive(leftMotors, rightMotors)
    myDrive.setDeadband(0.03)
    tableMotor = rev.CANSparkMax(14, rev.CANSparkMax.MotorType.kBrushless)
    return (leftMotors, rightMotors, gyro, spinPID, balancePID, stick, myDrive, tableMotor)