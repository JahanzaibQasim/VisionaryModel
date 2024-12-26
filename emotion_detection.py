import cv2
from fer import FER
import numpy as np
import os

# Disable oneDNN to avoid floating-point errors
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize FER model (using MTCNN for face detection)
emotion_detector = FER(mtcnn=True)

print("Press 'q' to quit")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Ensure frame is a NumPy array (avoid dtype error)
    frame = np.array(frame, dtype=np.uint8)

    # Detect emotions
    result = emotion_detector.detect_emotions(frame)

    # Draw bounding boxes and emotions
    if result:
        for face in result:
            (x, y, w, h) = face["box"]
            emotion = max(face["emotions"], key=face["emotions"].get)
            confidence = face["emotions"][emotion]

            # Draw the bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Put emotion label
            cv2.putText(frame, f"{emotion}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No Face Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Emotion Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
