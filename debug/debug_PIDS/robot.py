import wpilib
from wpilib.drive import DifferentialDrive
import wpilib.drive
import ctre
import rev
from ntcore import _ntcore
import wpilib.interfaces
import time
from navx import AHRS as ahrs
import exPID


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.ioEncoder = self.io.getEncoder()
        self.pc = exPID.PID()

    def teleopPeriodic(self):
        out = self.pc.main(self.ioEncoder)
        print('out: ' + str(out))
        self.io.set(out)
        print('current pos: ' + str(self.ioEncoder.getPosition()))

        

if __name__ == "__main__":
    wpilib.run(Robot)