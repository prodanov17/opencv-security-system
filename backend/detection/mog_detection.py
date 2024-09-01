import cv2
import numpy as np
from detection.detection import Detection


class MogDetection(Detection):
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=True)
        self.motion_threshold = 10000

    def detect(self, frame):
        person_detected = False
        # Apply background subtractor to get the foreground mask
        fgmask = self.fgbg.apply(frame)

        # Apply a binary threshold to the foreground mask
        _, thresh = cv2.threshold(fgmask, 244, 255, cv2.THRESH_BINARY)

        # Count non-zero (white) pixels
        motion_pixels = np.count_nonzero(thresh)

        # Check if motion is detected
        if motion_pixels > self.motion_threshold:
            person_detected = True

            # Find contours from the binary image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw rectangles around detected contours
            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Minimum contour area to consider
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw rectangle in green

        return frame, person_detected

    def get_short_name(self):
        return "mog"

