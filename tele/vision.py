# Import the camera server
from cscore import CameraServer

# Import OpenCV and NumPy
import cv2
import numpy as np

def main(camera):

    # Capture from the first USB Camera on the system

    # Get a CvSink. This will capture images from the camera
    cvSink = CameraServer.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = CameraServer.putVideo("Name", 320, 240)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
    time, img = cvSink.grabFrame(img)
    if time == 0:
        outputStream.notifyError(cvSink.getError())
    print(type(img))
    return img