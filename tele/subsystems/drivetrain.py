from commands2 import SubsystemBase

from wpilib import MotorControllerGroup, PWMSparkMax, Encoder, AnalogGyro
from wpilib.drive import DifferentialDrive

from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds

import constants

import ctre

import navx

#leftTalon1 = ctre.WPI_TalonFX(5)
#leftTalon2 = ctre.WPI_TalonFX(6)
#rightTalon1 = ctre.WPI_TalonFX(7)
#rightTalon2 = ctre.WPI_TalonFX(8)
#leftTalon1.configFactoryDefault()
#leftTalon2.configFactoryDefault()
#rightTalon1.configFactoryDefault()
#rightTalon2.configFactoryDefault()
#leftTalon1.config_kP(0, 0.02, 0)
#leftTalon2.config_kP(0, 0.02, 0)
#leftTalon1.config_kD(0, 0.25, 0)
#leftTalon2.config_kD(0, 0.25, 0)
#rightTalon1.config_kP(0, 0.02, 0)
#rightTalon2.config_kP(0, 0.02, 0)
#rightTalon1.config_kD(0, 0.25, 0)
#rightTalon2.config_kD(0, 0.25, 0)
#leftTalon1.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
#leftTalon2.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
#rightTalon1.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
#rightTalon2.configIntegratedSensorInitializationStrategy(ctre.SensorInitializationStrategy.BootToZero, 0)
#leftTalon1.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
#leftTalon2.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
#rightTalon1.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
#rightTalon2.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor, 0)
#
#
#class Drivetrain(SubsystemBase):
#    def __init__(self, gyro):
#        super().__init__()
#
#        # Create the motor controllers and their respective speed controllers.
#        self.leftMotors = MotorControllerGroup(
#            leftTalon1,
#            leftTalon2
#        )
#
#        self.rightMotors = MotorControllerGroup(
#            rightTalon1,
#            rightTalon2
#        )

        # Create the differential drivetrain object, allowing for easy motor control.
#        self.drive = DifferentialDrive(self.leftMotors, self.rightMotors)


        # Create the gyro, a sensor which can indicate the heading of the robot relative
        # to a customizable position.
#        self.gyro = gyro

        # Create the an object for our odometry, which will utilize sensor data to
        # keep a record of our position on the field.
#        self.odometry = DifferentialDriveOdometry(
#            self.gyro.getRotation2d(),
#            (leftTalon1.getSelectedSensorPosition() +
#            leftTalon2.getSelectedSensorPosition()) /2,
#            (rightTalon1.getSelectedSensorPosition() +
#             rightTalon2.getSelectedSensorPosition()) /2,
#        )

        # Reset the encoders upon the initilization of the robot.
#        self.resetEncoders()
#
#    def periodic(self):
#        """
#        Called periodically when it can be called. Updates the robot's
#        odometry with sensor data.
#        """
#        self.odometry.update(
#            self.gyro.getRotation2d(),
#            (leftTalon1.getSelectedSensorPosition() +
#            leftTalon2.getSelectedSensorPosition()) /2,
#            (rightTalon1.getSelectedSensorPosition() + 
#            rightTalon2.getSelectedSensorPosition()) /2,
#        )
#
#    def getPose(self):
#        """Returns the current position of the robot using it's odometry."""
#        return self.odometry.getPose()
#
#    def getWheelSpeeds(self):
#        """Return an object which represents the wheel speeds of our drivetrain."""
#        speeds = DifferentialDriveWheelSpeeds(
#            (leftTalon1.getSelectedSensorVelocity() +
#            leftTalon2.getSelectedSensorVelocity())/2,
#            (rightTalon1.getSelectedSensorVelocity() + 
#            rightTalon2.getSelectedSensorVelocity())/2
#        )
#        return speeds
#
#    def resetOdometry(self, pose):
#        """Resets the robot's odometry to a given position."""
#        self.resetEncoders()
#        self.odometry.resetPosition(
#            self.gyro.getRotation2d(),
#            (leftTalon1.getSelectedSensorPosition() +
#            leftTalon2.getSelectedSensorPosition())/2,
#            (rightTalon1.getSelectedSensorPosition() + 
#            rightTalon2.getSelectedSensorPosition())/2,
#            pose,
#        )
#
#    def arcadeDrive(self, fwd, rot):
#        """Drive the robot with standard arcade controls."""
#        self.drive.arcadeDrive(fwd, rot)
#
#    def tankDriveVolts(self, leftVolts, rightVolts):
#        """Control the robot's drivetrain with voltage inputs for each side."""
#        # Set the voltage of the left side.
#        self.leftMotors.setVoltage(leftVolts)
#
#        # Set the voltage of the right side. It's
#        # inverted with a negative sign because it's motors need to spin in the negative direction
#        # to move forward.
#        self.rightMotors.setVoltage(-rightVolts)
#
#        # Resets the timer for this motor's MotorSafety
#        self.drive.feed()
#
#    def resetEncoders(self):
#        """Resets the encoders of the drivetrain."""
#        leftTalon1.setSelectedSensorPosition(0, 0, 0)
#        leftTalon2.setSelectedSensorPosition(0, 0, 0)
#        rightTalon1.setSelectedSensorPosition(0, 0, 0)
#        rightTalon2.setSelectedSensorPosition(0, 0, 0)
#
#    def getAverageEncoderDistance(self):
#        """
#        Take the sum of each encoder's traversed distance and divide it by two,
#        since we have two encoder values, to find the average value of the two.
#        """
#        return (leftTalon1.getSelectedSensorPosition() +
#                leftTalon2.getSelectedSensorPosition() + rightTalon1.getSelectedSensorPosition() +
#                rightTalon2.getSelectedSensorPosition()) / 4
#
#    def getLeftEncoder(self):
#        """Returns the left encoder object."""
#        return (leftTalon1.getSelectedSensorPosition() +
#                leftTalon2.getSelectedSensorPosition())/2
#
#    def getRightEncoder(self):
#        """Returns the right encoder object."""
#        return (rightTalon1.getSelectedSensorPosition() +
#                rightTalon2.getSelectedSensorPosition()) /2
#
#    def setMaxOutput(self, maxOutput):
#        """Set the max percent output of the drivetrain, allowing for slower control."""
#        self.drive.setMaxOutput(maxOutput)
#
#    def zeroHeading(self):
#        """Zeroes the gyro's heading."""
#        self.gyro.reset()
#
#    def getHeading(self):
#        """Return the current heading of the robot."""
#        return self.gyro.getRotation2d().getDegrees()
#
#    def getTurnRate(self):
#        """Returns the turning rate of the robot using the gyro."""
#
        # The minus sign negates the value.
#        return -self.gyro.getSelectedSensorVelocity()