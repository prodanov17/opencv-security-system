from detection.detection import Detection
import cv2 as cv
import numpy as np

class MLDetection(Detection):
    def __init__(self):
        self.net = cv.dnn.readNetFromCaffe('models/config.txt', 'models/mobilenet_iter_73000.caffemodel')

    def detect(self, frame):
        blob = cv.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        person_detected = False

        for i in range(detections.shape[2]):
            # Extract the confidence
            confidence = detections[0, 0, i, 2]

            # Get the label for the class number and set its color
            idx = int(detections[0, 0, i, 1])

            # Check if the detection is of a person and its confidence is greater than the minimum confidence
            if idx == 15 and confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")
                cv.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                person_detected = True

        return frame, person_detected

    def get_short_name(self):
        return "ml"

