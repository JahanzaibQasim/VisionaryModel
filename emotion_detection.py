from flask import Flask, Response, render_template
import cv2
from deepface import DeepFace
import numpy as np

app = Flask(__name__)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Emotion Detection Logic
def detect_emotion(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    try:
        results = DeepFace.analyze(rgb_frame, actions=['emotion', 'age', 'gender'], enforce_detection=False)

        for face in results:
            x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
            emotion = face['dominant_emotion']
            age = face['age']
            gender = face['dominant_gender']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{emotion} ({gender}, {age})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    except Exception as e:
        cv2.putText(frame, "No Face Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame

# Generate Video Frames
def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = detect_emotion(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Flask Routes
@app.route('/')
def index():
    return render_template('emotion_detection.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=False)
