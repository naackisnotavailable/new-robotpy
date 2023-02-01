import wpilib
from autons.pid import main
import wpilib.drive
import ctre
import wpilib.interfaces
import time



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

        self.time = 0

    def autonomousPeriodic(self):
        self.time += 0.02
        print(str(self.time))
        
        

if __name__ == "__main__":
    wpilib.run(Robot)
