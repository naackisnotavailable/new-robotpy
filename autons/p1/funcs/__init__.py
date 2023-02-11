import ctre
from navx import AHRS as ahrs
import wpilib
import wpilib.drive
from funcs import autoBalance as balance
from funcs import spinPID as spin
import rev
from wpimath import controller as control
from wpimath import trajectory as traj
import wpimath
from wpimath import kinematics as kine
from ntcore import _ntcore
from wpimath import geometry as geo

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

    #init controller && kinematics object
    ramsete = control.RamseteController()
    kinematic = kine.DifferentialDriveKinematics(0.544)

    #create the trajectory
    inst = _ntcore.NetworkTableInstance.getDefault()
    start = geo.Pose2d((0.0), (0.0), geo.Rotation2d.fromDegrees(0.0))
    end = geo.Pose2d((1.0), (0.0), geo.Rotation2d.fromDegrees(0.0))
    interior_waypoints = []
    interior_waypoints.append(geo.Translation2d((0.5), (0.0)))
    interior_waypoints.append(geo.Translation2d((0.75), (0.0)))
    config = traj.TrajectoryConfig(0.4, 2)
    trajectory1 = traj.TrajectoryGenerator.generateTrajectory(start, interior_waypoints, end, config)

    return (leftMotors, rightMotors, gyro, spinPID, balancePID, stick, myDrive, tableMotor, inst)

def init_traj():
    pass