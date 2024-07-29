import cv2 as cv
import threading
import datetime
from detection.ml_detection import MLDetection
from storage.local_storage import LocalStorage

class Camera:

    def __init__(self, capture=0, storage_method=LocalStorage()):
        self.cap_source = capture
        self.cap = cv.VideoCapture(self.cap_source)
        self.out = None
        self.armed = False
        self.camera_thread = None
        self.storage = storage_method


    def arm(self, detection_method=MLDetection()):
        if not self.armed and not self.camera_thread:
            self.detection = detection_method
            self.camera_thread = threading.Thread(target=self.run)
            self.armed = True
            self.camera_thread.start()

        print("Camera armed")

    def disarm(self):
        self.armed = False
        self.camera_thread = None

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
                    self.out = cv.VideoWriter(current_recording_name, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

                # Write the frame into the file 'output.mp4'
                self.out.write(frame)

            # If no person is detected, stop recording after 50 frames
            else:
                non_detected_counter += 1  # increment the counter
                if non_detected_counter >= 50:  # if 50 frames have passed without a detection
                    if self.out is not None:  # if VideoWriter is initialized, release it
                        self.out.release()
                        self.out = None  # set it back to None
                        self.storage.handle_detection(current_recording_name)
                        current_recording_name = None

        if self.out is not None:  # if VideoWriter is initialized, release it
            self.out.release()
            self.out = None  # set it back to None
            self.storage.handle_detection(current_recording_name)
            current_recording_name = None



    def gen_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                self.cap = cv.VideoCapture(0)
                continue
            else:
                ret, buffer = cv.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def __del__(self):
        self.cap.release()
        if self.out is not None:
            self.out.release()
        cv.destroyAllWindows()
