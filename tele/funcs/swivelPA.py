import time
import ctre
class PID(object):
    def __init__(self):
        self.inte_last = 0
        self.err_last = 0


    def main(self, pos, swivel, Sp):
        if pos < 6:
            self.Kp = 0.0075  #tuning
            self.Ki = 0.008 #tuning
            self.Kd = 0.0075 #tuning
        elif pos < 9.5:
            self.Kp = 0.02  #tuning
            self.Ki = 0.0175 #tuning
            self.Kd = 0.01 #tuning
        else:
            self.Kp = 0.03  #tuning
            self.Ki = 0.02 #tuning
            self.Kd = 0.03 #tuning
            

        err = Sp - pos
        prop = self.Kp * err
        inte = self.Ki * (self.inte_last + err * 0.2)
        deri = self.Kd * ((err - self.err_last) / 0.2)
        self.err_last = err
        self.inte_last = inte

        output = (prop + inte + deri)
        
        swivel.set(output)

#pid = PID()
#input = 115
#x = 0
#while x < 5:
#
#    #sample calc
#    output = pid.main(input)
#    input = output - 10 * output
#    print(str(output))
#    x+=1

# 0.025 * 12 +0 +0
# 0.3 