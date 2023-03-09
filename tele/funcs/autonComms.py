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


    def checkCompletion(self):
        global compC
        global lastPos

        if compC == 0:
            if abs(self.l1.getMotorOutputVoltage()) < 0.05 and abs(self.r2.getMotorOutputVoltage()) < 0.05 and abs(self.r1.getSelectedSensorPosition()) > 3000:
                lastPos = self.r1.getSelectedSensorPosition()
                compC += 1
                return True
            

            else:
                  return False
        
        elif compC == 1:
            if self.r1.getSelectedSensorPosition() > -450:
                lastPos = self.r1.getSelectedSensorPosition()
                return True
            

            else:
                  return False
        

            
             
        
             
             
             
            
def moveOut(grab, grabEncoder, lift, liftEncoder, io, ioEncoder, exPID, autonSwiv, grabby):
    if liftEncoder.getPosition() > -82:
        curr = grabby.getOutputCurrent() / 100


        grabby.set(0.55)  #grab cone

        print('ioEncoder: ' + str(ioEncoder.getPosition()))
        io.set(exPID.main(ioEncoder, True))  #intake out


        if liftEncoder.getPosition() > -60: #lift start going up
            lift.set(-0.4)
        else:
            lift.set(0.0)


        if liftEncoder.getPosition() > -60.0:  #swivel control
            grab.set(-0.125)
        else:
            if grabEncoder.getPosition() < 17:
                autonSwiv.main(grabEncoder.getPosition(), grab, 16)
            else:
                grab.set(0.07)


        if grabEncoder.getPosition() > 8: #late lift control movements
            if liftEncoder.getPosition() < -60 and liftEncoder.getPosition() > -80:
                lift.set(-0.25)
            else:
                lift.set(0.0)
                return True
    

def moveIn(lift, liftEncoder, grab, grabEncoder, grabby, io, exPID, ioEncoder, autonSwiv):
    io.set(exPID.main(ioEncoder, True)) # intake moves out
    print('liftpos: ' + str(liftEncoder.getPosition()))
    grab.set(-0.09)
    grabby.set(0.15)
    if grabEncoder.getPosition() < -0.5:
        print('running t2')
        if liftEncoder.getPosition() < -8: #lift begins moving
            print('running t3')
            lift.set(0.45)
        else:
            lift.set(0.0)
    else:
        lift.set(0.0)
    

    

def editCompC(v):
    global compC
    compC = v











#
        #    
#
#
#
        #if liftEncoder.getPosition() < -70 and grabbyEncoder.getPosition() > 4:
        #    print('opening')
        #    grabby.set(-0.2 + curr)
#
#
        ##NEED TO CHECK WHEN EXTENDED, THEN PLACE
#
        ##part 2; move everything back in // NOT WORKING PROBABLY
#
        
        #
        ## After moving back in, drive directly backward for currently undetermined distance
        ## After leaving community, drive up to charge station and engage PID until end of autonomous
        #if False == True:
        #    spinPID(gyro.getYaw(), leftMotors, rightMotors, 180)