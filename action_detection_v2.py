from flask import Flask, Response, render_template
import cv2
import mediapipe as mp
import numpy as np
import threading
import time

app = Flask(__name__)

# Initialize Mediapipe models
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Global variables
cap = cv2.VideoCapture(0)
lock = threading.Lock()
model_loaded = False

# Load Mediapipe models (simulate loading time)
def load_model():
    global model_loaded
    time.sleep(10)  # Simulate 10-second loading
    model_loaded = True
    print("Model Loaded")

threading.Thread(target=load_model).start()

# Action detection logic
def detect_action(landmarks):
    if landmarks.pose_landmarks:
        pose = landmarks.pose_landmarks.landmark
        left_hip = pose[mp_holistic.PoseLandmark.LEFT_HIP]
        left_knee = pose[mp_holistic.PoseLandmark.LEFT_KNEE]
        left_ankle = pose[mp_holistic.PoseLandmark.LEFT_ANKLE]
        nose = pose[mp_holistic.PoseLandmark.NOSE]
        right_foot = pose[mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
        left_foot = pose[mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]

        def calculate_angle(a, b, c):
            a = np.array([a.x, a.y])
            b = np.array([b.x, b.y])
            c = np.array([c.x, c.y])
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            return np.abs(radians * 180.0 / np.pi)

        knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        # Detect Standing or Sitting
        if knee_angle > 160:
            return "Standing"
        elif knee_angle < 90:
            return "Sitting"

        # Detect Falling
        if nose.y > left_hip.y:
            return "Falling"

        # Detect Jumping (feet off the ground)
        if right_foot.y < left_hip.y and left_foot.y < left_hip.y:
            return "Jumping"

        # Detect Running (arm-leg coordination)
        if left_knee.y < left_hip.y and nose.y < left_hip.y:
            return "Running"

        # Detect Dancing (Wide stances or rhythmic movement)
        if abs(left_hip.x - left_foot.x) > 0.1 and abs(left_hip.y - left_knee.y) > 0.1:
            return "Dancing"

    return "No Action"

# Detect Hand Gestures
def detect_hand_gesture(hand_landmarks):
    if not hand_landmarks:
        return "No Gesture"

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    v_distance = np.linalg.norm(np.array([index_tip.x, index_tip.y]) - np.array([middle_tip.x, middle_tip.y]))
    if v_distance > 0.05 and pinky_tip.y > ring_tip.y:
        return "V-Sign"
    
    if thumb_tip.y < index_tip.y and abs(thumb_tip.x - index_tip.x) < 0.05:
        return "Thumbs Up"
    elif thumb_tip.y > index_tip.y and abs(thumb_tip.x - index_tip.x) < 0.05:
        return "Thumbs Down"

    return "Open Palm"

# Video Frame Generator
def generate_frames():
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            with lock:
                ret, frame = cap.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(rgb_frame)
                hand_results = mp_hands.Hands().process(rgb_frame)

                mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

                action = detect_action(results)

                gesture = "No Gesture"
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        gesture = detect_hand_gesture(hand_landmarks)

                cv2.putText(frame, f"Action: {action}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Gesture: {gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('action_detection.html')

@app.route('/video_feed')
def video_feed():
    if not model_loaded:
        return render_template('od_loading.html')
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    if not cap.isOpened():
        print("Failed to open webcam. Exiting...")
    else:
        app.run(host='0.0.0.0', port=5002, debug=False)
