import wpilib
import wpilib.drive
import ctre
import rev
from ntcore import _ntcore
import wpilib.interfaces
import time
import navx
from navx import AHRS as ahrs
import tele.functions as functions
import cscore as cam
from cscore import CameraServer
import numpy as np

class Robot(wpilib.TimedRobot):
    def robotInit(self):

        # Capture from the first USB Camera on the system
        camera = CameraServer.startAutomaticCapture()
        camera.setResolution(320, 240)

        # Get a CvSink. This will capture images from the camera
        self.cvSink = CameraServer.getVideo()

        # (optional) Setup a CvSource. This will send images back to the Dashboard
        self.outputStream = CameraServer.putVideo("Name", 320, 240)

        # Allocating new images is very expensive, always try to preallocate
        self.img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    def teleopPeriodic(self):
        self.time, self.img = self.cvSink.grabFrame(self.img)
        if time == 0:
            # Send the output the error.
            self.outputStream.notifyError(self.cvSink.getError())
            # skip the rest of the current iteration

        #
        # Insert your image processing logic here!
        #

        # (optional) send some image back to the dashboard
        self.outputStream.putFrame(self.img)
        
    



if __name__ == "__main__":
    wpilib.run(Robot)