import ctre
import math

compC = 0
lastPos = 0

cc = 6*math.pi
class moveCm(object):
    def __init__(self, l1, l2, r1, r2,):
            
            self.l1 = l1
            self.l2 = l2
            self.r1 = r1
            self.r2 = r2

            self.l1.setSelectedSensorPosition(0, 0, 0)
            self.l2.setSelectedSensorPosition(0, 0, 0)
            self.r1.setSelectedSensorPosition(0, 0, 0)
            self.r2.setSelectedSensorPosition(0, 0, 0)
            


    def main(self, inches):
            self.ticks = inches * 497
            self.l1.set(ctre._ctre.ControlMode.Position, self.ticks)
            self.l2.set(ctre._ctre.ControlMode.Position, self.ticks)
            
            self.r1.set(ctre._ctre.ControlMode.Position, -self.ticks)
            self.r2.set(ctre._ctre.ControlMode.Position, -self.ticks)


    