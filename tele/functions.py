import math

def tankDrive(x, y):
    """Drives the robot using arcade y."""
    # variables to determine the quadrants
    
    left_motor = 0 #my trashy code
    right_motor = 0 #my trashy code
    y = math.sqrt(x*x + y*y) #my trashy code

    maximum = max(abs(y), abs(x))
    total, difference = y + x, y - x

    # set speed according to the quadrant that the values are in
    if y >= 0:
        if x >= 0:  # I quadrant
            left_motor = maximum
            right_motor = difference
        else:            # II quadrant
            left_motor = total
            right_motor = maximum
    else:
        if x >= 0:  # IV quadrant
            left_motor = total
            right_motor = -maximum
        else:            # III quadrant
            left_motor = -maximum
            right_motor = difference
    return(left_motor, right_motor)

#hehe Sameer was here

def moveArm(toggleRT):
        return toggleRT
def balancePreset(wheelCir):
        return moveDist(100)
def moveDist(x):
            pi = 3.141592
            wheelDia = 20
            revDist = wheelDia * pi
            deg = x * 360 / revDist
            return deg
def gyroCalc(gyro_roll):
        pass
def getConeSpeed(weighted_average):
        
        if weighted_average <= 180:
            if weighted_average >= 80:
                return 0.3
            elif 80 >= weighted_average >= 30:
                return 0.15
            elif 30 >= weighted_average >= 10:
                return 0.05
            elif 10 >= weighted_average:
                return 0.0
        elif 180 <= weighted_average <= 360:
            if weighted_average >= 280:
                return -0.3
            elif 280 <= weighted_average <= 330:
                return -0.15
            elif 330 <= weighted_average <= 350:
                return -0.05
            elif weighted_average >= 350:
                return -0.0
def xDeg(gyro_angle, deg):
        pass