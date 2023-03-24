import time
class PID(object):
    def __init__(self):
        self.inte_last = 0


        self.Kp = 0.4 #tuning
        self.Ki = 0.0  #tuning


    def main(self, pos, grabby, Sp):

        err = Sp - pos
        prop = self.Kp * err
        inte = self.Ki * (self.inte_last + err * 0.2)
        self.inte_last = inte

        output = (prop + inte)
        print('GRABBYPI OUT: ' + str(output))
        #grabby.set(output)
        return output

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