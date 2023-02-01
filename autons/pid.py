import numpy as np
import time

def main(gyro_data):
    Kp = 1  #tuning
    Ki = 0.95  #tuning
    Kd = -10 #tuning


    err = 0 - gyro_data
    prop = Kp * err
    inte = Ki * (inte_last + err * 0.2)
    deri = Kd * (err_last-err / 0.2)
    err_last = err
    inte_last = inte

    output = (prop + inte + deri), err_last, inte_last
    return output

