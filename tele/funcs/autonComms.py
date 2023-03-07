import ctre
import math
cc = 6*math.pi
class moveCm(object):
    def __init__(self, l1, l2, r1, r2, inches):
            self.inches = inches
            self.ticks = 1

            self.l1 = l1
            self.l2 = l2
            self.r1 = r1
            self.r2 = r2

            self.l1.setSelectedSensorPosition(0, 0, 0)
            self.l2.setSelectedSensorPosition(0, 0, 0)
            self.r1.setSelectedSensorPosition(0, 0, 0)
            self.r2.setSelectedSensorPosition(0, 0, 0)

            self.inte_last = 0



    def main(self):
            
            rot = self.inches / cc

            err = self.l1.getSelectedSensorPosition() - rot
            prop = 0.1 * err
            inte = 0.04 * (self.inte_last + err * 0.2)

            out = prop + inte

            self.l1.set(ctre._ctre.ControlMode.PercentOutput, out)
            self.l2.set(ctre._ctre.ControlMode.PercentOutput, out)
            
            self.r1.set(ctre._ctre.ControlMode.PercentOutput, out)
            self.r2.set(ctre._ctre.ControlMode.PercentOutput, out)


    def checkCompletion(self):
        if  self.l1.getSelectedSensorPosition() > self.ticks - 100 and self.r1.getSelectedSensorPosition() > self.ticks - 100:
              return True
        else:
              return False
def moveOut(grab, grabEncoder, lift, liftEncoder, io, ioEncoder, exPID, autonSwiv, grabby):
    curr = grabby.getOutputCurrent() / 100


    grabby.set(0.55 - curr)  #grab cone
    
    
    io.set(exPID.main(ioEncoder, True))  #intake out
    
    
    if liftEncoder.getPosition() > -60: #lift start going up
        lift.set(-0.4)
    else:
        lift.set(0.0)
    
    
    if liftEncoder.getPosition() > -55:  #swivel control
        grab.set(-0.1)
    else:
        autonSwiv.main(grabEncoder.getPosition(), grab, 21)
    

    if grabEncoder.getPosition() > 8: #late lift control movements
        if liftEncoder.getPosition() < -60 and liftEncoder.getPosition() > -75:
            lift.set(-0.25)
        else:
            lift.set(0.0)
    

    













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
        #if False == True:
        #    curr = grabby.getOutputCurrent() / 100
        #    print('SWIVEL ENCODER: ' + str(grabEncoder.getPosition()))
#
#
        #    print('running t1')
        #    print('closing')
        #    grabby.set(0.4 - curr)
        #    io.set(exPID.main(ioEncoder, True)) # intake moves out
        #    print('liftpos: ' + str(liftEncoder.getPosition()))
        #    grab.set(-0.1)
        #    if grabEncoder.getPosition() < -0.5:
        #        print('running t2')
        #        if liftEncoder.getPosition() < -5: #lift begins moving
        #            print('running t3')
        #            lift.set(0.2)
        #        else:
        #            lift.set(0.0)
        #    else:
        #        lift.set(0.0)
        #
        ## After moving back in, drive directly backward for currently undetermined distance
        ## After leaving community, drive up to charge station and engage PID until end of autonomous
        #if False == True:
        #    spinPID(gyro.getYaw(), leftMotors, rightMotors, 180)