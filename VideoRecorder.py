import cv2
import threading
import time
from datetime import datetime

class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.out = None
        self.record_event = threading.Event()
        self.frame = None
        self.lock = threading.Lock()

    def start_recording_event(self):
        self.record_event.set()

    def stop_recording(self):
        self.recording = False
        self.record_event.clear()
        if self.out is not None:
            self.out.release()

    def write_frame(self, frame):
        with self.lock:
            self.frame = frame.copy() if frame is not None else None

    def start_recording(self):
        while True:
            self.record_event.wait()
            self.record_event.clear()

            # Initialize video writer
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"weapon_detection_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))
            self.recording = True

            # Record for 10 seconds
            start_time = time.time()
            while time.time() - start_time < 10 and self.recording:
                with self.lock:
                    if self.frame is not None:
                        # Resize frame to match output dimensions
                        frame_resized = cv2.resize(self.frame, (640, 480))
                        self.out.write(frame_resized)
                time.sleep(0.05)  # Control frame rate

            # Release video writer
            self.recording = False
            if self.out is not None:
                self.out.release()
                print(f"Video saved as {output_filename}")