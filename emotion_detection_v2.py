import cv2
from deepface import DeepFace
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        # Analyze emotions, age, gender
        result = DeepFace.analyze(rgb_frame, actions=['emotion', 'age', 'gender'], enforce_detection=False)

        # Process each detected face
        for face in result:
            x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
            emotion = face['dominant_emotion']
            age = face['age']
            gender = face['dominant_gender']

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display emotion, age, gender
            cv2.putText(frame, f"{emotion} ({gender}, {age})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    except Exception as e:
        cv2.putText(frame, "No Face Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Emotion Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
