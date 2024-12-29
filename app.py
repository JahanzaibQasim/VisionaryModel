from flask import Flask, render_template, jsonify, Response
import cv2
from fer import FER

app = Flask(__name__)

# Initialize Emotion Detection Model (or any model you want to connect)
emotion_detector = FER(mtcnn=True)
cap = cv2.VideoCapture(0)  # Webcam feed

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/service-details')
def service_details():
    return render_template('service-details.html')

# Start model when the user clicks the section
@app.route('/start_model', methods=['POST'])
def start_model():
    return jsonify({'message': 'Model started successfully!'})

# Real-time video feed (streams webcam with model running)
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Emotion Detection (replace with your model's logic)
        results = emotion_detector.detect_emotions(frame)
        for face in results:
            (x, y, w, h) = face["box"]
            emotion = max(face["emotions"], key=face["emotions"].get)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to display the live webcam feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
