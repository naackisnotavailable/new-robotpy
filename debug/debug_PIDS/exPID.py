import time
import ctre
class PID(object):
    def __init__(self):
        self.inte_last = 0
        self.err_last = 0
        
    def main(self, ioEncoder):
        Kp = 0.1  #tuning
        Ki = 0.00  #tuning
        Kd = 0.0 #tuning
        Sp = 0

        err = Sp - ioEncoder.getPosition()
        prop = Kp * err
        inte = Ki * (self.inte_last + err * 0.2)
        deri = Kd * (self.err_last-err / 0.2)
        self.err_last = err
        self.inte_last = inte
        output = (prop + inte + deri) / 2

        print('output: ' + str(output))
        print('prop: ' + str(prop))
        print('inte: ' + str(inte))
        print('deri: ' + str(deri))

        return output