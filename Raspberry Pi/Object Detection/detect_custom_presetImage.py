import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
#from picamera2 import Picamera2, Preview
import serial
ser = serial.Serial('/dev/ttyS0', 115200, timeout=3)
print(ser.name)

imageFile = 'PresentationInput.jpg'

model_asset_path='12-14hotModel.tflite'

#picam2 = Picamera2()
#preview_config = picam2.create_preview_configuration(main={"size": (4608, 2592)}, lores={"size": (512, 350)})
#picam2.configure(preview_config)

#picam2.start_preview(Preview.QTGL)

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 5
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red

spot0 = (1430, 1180)
spot1 = (1650, 1180)
spot2 = (1870, 1200)
spot3 = (2070, 1200)
spot4 = (2260, 1200)
spot5 = (2450, 1220)
spot6 = (2630, 1220)
spot7 = (2820, 1230)
spot8 = (1220, 1500)
spot9 = (1620, 1500)
spot10 = (2530, 1500)
spot11 = (2950, 1500)
spot12 = (1140, 1670)
spot13 = (1550, 1670)
spot14 = (2606, 1680)
spot15 = (3030, 1672)
spot16 = (985, 1860)
spot17 = (1500, 1870)
spot18 = (2660, 1870)
spot19 = (3130, 1900)
spot20 = (800, 2235)
spot21 = (1365, 2225)
spot22 = (2700, 2200)
spot23 = (3215, 2170)
# spot0 = (1630, 1500)
# 
# spot0 = (830, 2230)
# spot1 = (960, 1880)
# spot2 = (1130, 1690)
# spot3 = (1230, 1510)
# 
# spot5 = (1540, 1690)
# spot6 = (1500, 1900)
# spot7 = (1350, 2240)
# spot8 = (2660, 2210)
# spot9 = (2640, 1900)
# spot10 = (2600, 1680)
# spot11 = (2540, 1500)
# spot12 = (2920, 1510)
# spot13 = (2990, 1680)
# spot14 = (3080, 1910)
# spot15 = (3210, 2210)
# spot16 = (2830, 1200)
# spot17 = (2636, 1200)
# spot18 = (2450, 1200)
# spot19 = (2258, 1200)
# spot20 = (2074, 1200)
# spot21 = (1874, 1200)
# spot22 = (1664, 1200)
# spot23 = (1445, 1200)


    
stallLoc = [spot0, spot1,spot2, spot3, spot4, spot5, spot6, spot7, spot8, spot9, spot10, spot11, spot12, spot13, spot14, spot15, spot16, spot17, spot18, spot19, spot20, spot21, spot22, spot23]

# Count how many stalls then round range to next 16th divisible value
# Because we need enough values to fill bytes
stallOcc = [0 for i in range(24)]


#x, y = parkingStallList[0]
#print(x)
#print(y)
def drawSpots(image):
    radius = 30
    color = (0,0,255)
    thickness = -1
    cv2.circle(image, spot0, radius, color, thickness)
    cv2.circle(image, spot1, radius, color, thickness)
    cv2.circle(image, spot2, radius, color, thickness)
    cv2.circle(image, spot3, radius, color, thickness)
    cv2.circle(image, spot4, radius, color, thickness)
    cv2.circle(image, spot5, radius, color, thickness)
    cv2.circle(image, spot6, radius, color, thickness)
    cv2.circle(image, spot7, radius, color, thickness)
    cv2.circle(image, spot8, radius, color, thickness)
    cv2.circle(image, spot9, radius, color, thickness)
    cv2.circle(image, spot10, radius, color, thickness)
    cv2.circle(image, spot11, radius, color, thickness)
    cv2.circle(image, spot12, radius, color, thickness)
    cv2.circle(image, spot13, radius, color, thickness)
    cv2.circle(image, spot14, radius, color, thickness)
    cv2.circle(image, spot15, radius, color, thickness)
    cv2.circle(image, spot16, radius, color, thickness)
    cv2.circle(image, spot17, radius, color, thickness)
    cv2.circle(image, spot18, radius, color, thickness)
    cv2.circle(image, spot19, radius, color, thickness)
    cv2.circle(image, spot20, radius, color, thickness)
    cv2.circle(image, spot21, radius, color, thickness)
    cv2.circle(image, spot22, radius, color, thickness)
    cv2.circle(image, spot23, radius, color, thickness)
    
def visualize(
    image,
    detection_result
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)
    #print("the start point is {}".format(start_point) + "the end point is {}".format(end_point))
    
    # Check if parking spot points are inside a bound box
    index = 0
    for spot in stallLoc:
        x, y = spot
        if x > start_point[0] and x < end_point[0] and y > start_point[1] and y < end_point[1]:
            stallOcc[index] = 1
        else:
            if stallOcc[index] != 1:
                stallOcc[index] = 0
        index += 1
    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    #print(probability)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

  print("sending data")
  for x in range(0, 24, 8):
      # Convert binary values to "hex" values
      value = (stallOcc[x] * 128) + (stallOcc[x+1] * 64) + (stallOcc[x+2] * 32) + (stallOcc[x+3] * 16) + (stallOcc[x+4] * 8) + (stallOcc[x+5] * 4) + (stallOcc[x+6] * 2) + (stallOcc[x+7] * 1)
      
      sender = str(value)
      ser.write(sender.encode('utf-8'))
      print(sender.encode('utf-8'))
      ser.write(b',')
      print(',')

  ser.write(b';')
  print(';')
  print(stallOcc)
  return image

# STEP 1: Setup Camera
#picam2.start()
#time.sleep(2)



# STEP 2: Create an ObjectDetector object.
base_options = python.BaseOptions(model_asset_path)
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.3)
detector = vision.ObjectDetector.create_from_options(options)

while 1:
    stallOcc = [0 for i in range(24)]
    # Take Photo
    #picam2.capture_file("input.jpg")
    IMAGE_FILE = imageFile
    time.sleep(2)
    #img = cv2.imread(IMAGE_FILE)
    #viewer = cv2.resize(img, (1500, 1000))
    #cv2.imshow('input', viewer)
    #cv2.waitKey(0)

    # STEP 3: Load the input image.
    image = mp.Image.create_from_file(IMAGE_FILE)

    # STEP 4: Detect objects in the input image.
    detection_result = detector.detect(image)

    # STEP 5: Process the detection result. In this case, visualize it.
    image_copy = np.copy(image.numpy_view())
    annotated_image = visualize(image_copy, detection_result)
    rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('output.jpg', rgb_annotated_image)
    drawSpots(rgb_annotated_image)
    smaller = cv2.resize(rgb_annotated_image, (1920, 1000))
    cv2.imshow('output', smaller)
    cv2.waitKey(30000)
    cv2.destroyAllWindows()
    
picam2.close()

