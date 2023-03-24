import time
class PID(object):
    def __init__(self):
        self.inte_last = 0
        self.err_last = 0
        
    def main(self, liftEncoder, set):
        if set == True:
            Sp = -95.0 #some encoder value
        elif set == False:
            Sp = 0.0
        Kp = 0.01  #tuning
        Ki = 0.00  #tuning
        Kd = 0.00 #tuning

        err = Sp - liftEncoder.getPosition()
        prop = Kp * err
        inte = Ki * (self.inte_last + err * 0.2)
        deri = Kd * (self.err_last-err / 0.2)
        self.err_last = err
        self.inte_last = inte

        output = (prop + inte + deri)
        if output >= 0.3:
            output = 0.3
        elif output <= -0.3:
            output = -0.3
        return output