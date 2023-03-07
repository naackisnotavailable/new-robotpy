import time
import ctre
class PID(object):
    def __init__(self):
        self.inte_last = 0
        self.err_last = 0
        
    def main(self, ioEncoder, set):
        if set == True:
            Sp = 10.5 #some encoder value
        elif set == False:
            Sp = 0.0
        Kp = 0.15  #tuning
        Ki = 0.0175  #tuning
        Kd = 0.0150 #tuning

        err = Sp - ioEncoder.getPosition()
        prop = Kp * err
        inte = Ki * (self.inte_last + err * 0.2)
        deri = Kd * (self.err_last-err / 0.2)
        self.err_last = err
        self.inte_last = inte

        output = (prop + inte + deri) / 3.0

        return output