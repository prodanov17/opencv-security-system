import cv2 as cv
import time
import threading
import datetime
from detection.hog_detection import HogDetection
from detection.ml_detection import MLDetection
from detection.mog_detection import MogDetection
from storage.local_storage import LocalStorage

STOP_RECORDING_AFTER = {
        'ml': 50,
        'hog': 1000,
        'mog': 1000,
        }


class Camera:

    def __init__(
            self,
            name,
            id,
            model=None,
            detection_method=MLDetection(),
            capture=0,
            armed=False,
            storage_method=LocalStorage()
    ):
        self.cap_source = capture if capture != '0' else 0
        self.name = name
        self.id = id
        self.cap = cv.VideoCapture(self.cap_source)
        self.out = None
        self.armed = armed
        self.model = model
        self.camera_thread = None
        self.storage = storage_method
        self.detection = detection_method
        self.lock = threading.Lock()

    def arm(self, detection_method=MLDetection()):
        with self.lock:
            if not self.armed and not self.camera_thread:
                self.detection = detection_method
                self.camera_thread = threading.Thread(target=self.run)
                self.armed = True
                self.camera_thread.start()

            if self.model is not None:
                self.model.arm(detection_method.get_short_name())
            print("Camera armed")

    def disarm(self):
        with self.lock:
            self.armed = False

            if self.camera_thread and self.camera_thread.is_alive():
                self.camera_thread = None

            if self.model is not None:
                self.model.disarm()

            print("Camera disarmed")

    def run(self):
        person_detected = False
        non_detected_counter = 0
        current_recording_name = None

        self.cap = cv.VideoCapture(self.cap_source)

        while self.armed:
            check, frame = self.cap.read()

            if not check:
                break

            frame = cv.resize(frame, (640, 480))
            frame, person_detected = self.detection.detect(frame)

            if person_detected:
                non_detected_counter = 0  # reset the counter
                if self.out is None:  # if VideoWriter isn't initialized, initialize it
                    now = datetime.datetime.now()
                    formatted_now = now.strftime("%d-%m-%y-%H-%M-%S")
                    print("Person motion detected at", formatted_now)
                    current_recording_name = f'{formatted_now}.mp4'
                    fourcc = cv.VideoWriter_fourcc(*'mp4v')  # or use 'XVID'
                    self.out = cv.VideoWriter(
                        current_recording_name,
                        fourcc,
                        20.0,
                        (frame.shape[1], frame.shape[0])
                    )

                # Write the frame into the file 'output.mp4'
                self.out.write(frame)

            # If no person is detected, stop recording after 50 frames
            else:
                non_detected_counter += 1  # increment the counter
                if non_detected_counter >= STOP_RECORDING_AFTER[self.detection.get_short_name()]:
                    if self.out is not None:  # if VideoWriter is initialized, release it
                        self.out.release()
                        self.out = None  # set it back to None
                        self.storage.handle_detection(current_recording_name, self.id)
                        current_recording_name = None

        if self.out is not None:  # if VideoWriter is initialized, release it
            self.out.release()
            self.out = None  # set it back to None
            self.storage.handle_detection(current_recording_name, self.id)
            current_recording_name = None

        self.cap.release()

    def gen_frames(self):
        capture = cv.VideoCapture(self.cap_source)

        if self.detection == 'ml':
            self.detection = MLDetection()
        elif self.detection == 'hog':
            self.detection = HogDetection()
        elif self.detection == 'mog':
            self.detection = MogDetection()

        while True:
            try:
                success, frame = capture.read()
                if not success:
                    break

                frame = cv.resize(frame, (640, 480))
                if not self.armed:
                    frame, _ = self.detection.detect(frame)

                ret, buffer = cv.imencode('.jpg', frame)
                if not ret:
                    print("Failed to encode frame.")
                    continue

                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            except Exception as e:
                print(f"Error in gen_frames: {e}")
                time.sleep(1)  # Brief sleep before attempting recovery
                continue

        capture.release()

    def __del__(self):
        with self.lock:
            if self.cap is not None:
                self.cap.release()
            if self.out is not None:
                self.out.release()
