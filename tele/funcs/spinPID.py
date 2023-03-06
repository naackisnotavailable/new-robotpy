import time
import ctre
class PID(object):
    def __init__(self):
        self.inte_last = 0
        self.err_last = 0

        self.Kp = 0.03  #tuning
        self.Ki = 0.00  #tuning
        self.Kd = 0.0 #tuning


    def main(self, gyro_angle, left_motors, right_motors, Sp):

        err = Sp - gyro_angle
        prop = self.Kp * err
        inte = self.Ki * (self.inte_last + err * 0.2)
        deri = self.Kd * (self.err_last-err / 0.2)
        self.err_last = err
        self.inte_last = inte

        output = (prop + inte + deri)

        left_motors.set(output)
        right_motors.set(output)

        print('spin out: '+str(output))


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