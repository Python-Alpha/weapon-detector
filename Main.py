import threading
from Detection import capture_detected
from EmailSending import send_mail
from HumanDetection import age_detection
from VideoRecorder import VideoRecorder

# Initialize video recorder
video_recorder = VideoRecorder()

# Create threads for capturing the image, age detection, email sending, and video recording
capture_thread = threading.Thread(target=capture_detected, args=(video_recorder,))
age_thread = threading.Thread(target=age_detection)
send_thread = threading.Thread(target=send_mail)
record_thread = threading.Thread(target=video_recorder.start_recording)

# Start the threads
capture_thread.start()
age_thread.start()
send_thread.start()
record_thread.start()

# Wait for threads to complete
capture_thread.join()
age_thread.join()
send_thread.join()
record_thread.join()