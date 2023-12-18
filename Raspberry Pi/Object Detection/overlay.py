from picamera2 import Picamera2
import numpy as np
picam2 = Picamera2()

picam2.configure(picam2.create_preview_configuration(main={"size": (4096, 2303)}))
picam2.start(show_preview=True)
#set the y,x bounding
overlay = np.zeros((300, 400, 4), dtype=np.uint8)
# overlay[y1;y2, x1:x2] = Color(RGB, opacity)
overlay[275:284, 45:145] = (0, 255, 0, 64) # greenish
overlay[260:282, 174:182] = (255, 0, 0, 64) # reddish
overlay[270:279, 213:312] = (0, 0, 255, 64) # blueish
overlay[195:197, 167:169] = (0, 0, 0, 1000) # blackish
picam2.set_overlay(overlay)