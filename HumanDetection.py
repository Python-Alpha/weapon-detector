# Age and Gender Detection
import threading

import cv2
from deepface import DeepFace

from EmailSending import send_event

age_detect = threading.Event()

def age_detection():
    while True:
        age_detect.wait()
        age_detect.clear()

        # add image for analysis
        img1 = cv2.imread("cell phone.png")

        # Get results
        result = DeepFace.analyze(img1, actions=['age'])
        age = int(result[0]['age'])

        if age >= 15:
            send_event.set()
