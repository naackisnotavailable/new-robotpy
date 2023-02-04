from keras.models import load_model
#from PIL import Image, ImageOps #Install pillow instead of PIL
import numpy as np
import cv2
#import time

video = cv2.VideoCapture(0)
print(type(video))
print(video)
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model('test\keras_model.h5', compile=False)
# Load the labels

class_names = open('test\labels.txt', 'r').readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
#image = Image.open('<IMAGE_PATH>').convert('RGB')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)


data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
timer = []
dims = (224, 224)
checkOpen = video.isOpened()
print("Opened?:" + str(checkOpen))

_, _ = video.read()

while True:
    _, frame = video.read() #takes a full second ????????
    frame = cv2.resize(frame, dims)
    # Load the labels
    class_names = open('test\labels.txt', 'r').readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = frame

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    #image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    #turn the image into a numpy array
    image_array = np.asarray(frame)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    index = np.argmax(prediction)
    prediction1 = np.delete(prediction[0], index)
    index2 = np.argmax(prediction1)

    class_name = class_names[index]
    confidence_score = prediction[0][index]

    class_name2 = class_names[index2]
    confidence_score2 = prediction1[index2]
    print('Class:', class_name, end='')

    weighted_average1 = int(class_name) * confidence_score
    weighted_average2 = int(class_name2) * confidence_score2
    weighted_average = (weighted_average1 + weighted_average2) / 2
    print('wavg: ' + str(weighted_average))

    print('Confidence score:', confidence_score)
    print('class2: ' + class_name2)
    print('conf2: ' + str(confidence_score2))

    
        



    cv2.imshow("Capturing", frame)
    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
            break
    
video.release()
cv2.destroyAllWindows()


