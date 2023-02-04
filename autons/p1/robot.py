import wpilib
import wpilib.drive
import ctre
import wpilib.interfaces
import time
from wpimath import controller as control
from wpimath import geometry as geo
from wpimath import trajectory as traj
geo.Translation2d.distance()

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.leftTalon1 = ctre.TalonFX(5)
        self.leftTalon2 = ctre.TalonFX(6)
        self.rightTalon1 = ctre.TalonFX(7)
        self.rightTalon2 = ctre.TalonFX(8)
        self.leftTalon1.configFactoryDefault()
        self.leftTalon2.configFactoryDefault()
        self.rightTalon1.configFactoryDefault()
        self.rightTalon2.configFactoryDefault()

        self.allMotors = (self.leftTalon1, self.leftTalon2, self.rightTalon1, self.rightTalon2)
        self.trajconfig = traj.TrajectoryConfig(0.8, 2)
        self.traj = traj.TrajectoryGenerator.generateTrajectory(1, self.trajconfig)
        self.traject = control.RamseteController(2.1, 0.8)
        self.pose = geo.Pose2d(0, 0, 0)
        self.time = 0
    def autonomousPeriodic(self):

        print(str(self.traject.calculate(self.pose, )))
        
        

if __name__ == "__main__":
    wpilib.run(Robot)