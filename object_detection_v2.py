from flask import Flask, Response, render_template
import cv2
import torch
import threading
import time

app = Flask(__name__)

# Global variables for video capture and loading state
cap = cv2.VideoCapture(0)
lock = threading.Lock()
model_loaded = False

# Load YOLOv5 model globally (with delay for loading animation)
def load_model():
    global model_loaded, model
    time.sleep(10)  # Simulate loading time
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model_loaded = True
    print("Model Loaded")

threading.Thread(target=load_model).start()  # Load model in a separate thread


# Video Frame Generator
def generate_frames():
    while True:
        with lock:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame with YOLO
            results = model(frame)
            frame = results.render()[0]
            
            # Encode and yield frame
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Flask Routes
@app.route('/')
def index():
    return render_template('object_detection.html')


@app.route('/video_feed')
def video_feed():
    if not model_loaded:
        # Show loading animation if model isn't ready
        return render_template('od_loading.html')
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    if not cap.isOpened():
        print("Failed to open webcam. Exiting...")
    else:
        app.run(host='0.0.0.0', port=5001, debug=False)
