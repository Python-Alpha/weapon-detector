import threading
import cv2
from deepface import DeepFace
from EmailSending import send_event, set_detection_info

age_detect = threading.Event()

def age_detection():
    while True:
        age_detect.wait()
        age_detect.clear()

        try:
            # Read image for analysis
            img = cv2.imread("cell phone.png")
            if img is None:
                print("Error: Could not read image for age detection")
                continue

            # Get age, gender, and expression detection results
            result = DeepFace.analyze(img, actions=['age', 'gender', 'emotion'])
            age = int(result[0]['age'])
            gender = result[0]['dominant_gender']
            expression = result[0]['dominant_emotion']

            print(f"Detected person - Age: {age}, Gender: {gender}, Expression: {expression}")

            if age >= 15:
                print("Triggering email notification with detection details.")
                set_detection_info(age, gender, expression)
                send_event.set()
            else:
                print(f"Detected person age: {age}. No email notification triggered.")
        except Exception as e:
            print(f"Detection failed. Error: {str(e)}")