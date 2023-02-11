import time
import ctre
class PID(object):
    def __init__(self):
        self.inte_last = 0
        self.err_last = 0
        
    def main(self, gyro_roll, left_motors, right_motors):
        Kp = 0.015  #tuning
        Ki = 0.0  #tuning
        Kd = 0.0 #tuning

        Sp = 0

        err = Sp - gyro_roll
        prop = Kp * err
        inte = Ki * (self.inte_last + err * 0.2)
        deri = Kd * (self.err_last-err / 0.2)
        self.err_last = err
        self.inte_last = inte

        output = (prop + inte + deri)

        left_motors.set(output)
        right_motors.set(-output)

        print(str(output))


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