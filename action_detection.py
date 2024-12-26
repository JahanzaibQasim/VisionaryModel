import cv2
import mediapipe as mp
import numpy as np

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize hand model
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Action detection logic
def detect_action(landmarks):
    if landmarks.pose_landmarks:
        pose = landmarks.pose_landmarks.landmark
        left_hip = pose[mp_holistic.PoseLandmark.LEFT_HIP]
        left_knee = pose[mp_holistic.PoseLandmark.LEFT_KNEE]
        left_ankle = pose[mp_holistic.PoseLandmark.LEFT_ANKLE]

        # Calculate knee angle
        def calculate_angle(a, b, c):
            a = np.array([a.x, a.y])
            b = np.array([b.x, b.y])
            c = np.array([c.x, c.y])
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            return np.abs(radians * 180.0 / np.pi)

        knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        if knee_angle > 160:
            return "Standing"
        elif knee_angle < 90:
            return "Sitting"
        if pose[mp_holistic.PoseLandmark.NOSE].y > left_hip.y:
            return "Falling"
        
    return "No Action"

# Hand gesture recognition (V-sign, thumbs up/down)
def detect_hand_gesture(hand_landmarks):
    if not hand_landmarks:
        return "No Gesture"

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    # V-Sign Detection (Distance between index and middle finger)
    v_distance = np.linalg.norm(np.array([index_tip.x, index_tip.y]) - np.array([middle_tip.x, middle_tip.y]))
    if v_distance > 0.05 and pinky_tip.y > ring_tip.y:
        return "V-Sign"
    
    # Thumbs Up or Down (Thumb tip relative to index tip)
    if thumb_tip.y < index_tip.y and abs(thumb_tip.x - index_tip.x) < 0.05:
        return "Thumbs Up"
    elif thumb_tip.y > index_tip.y and abs(thumb_tip.x - index_tip.x) < 0.05:
        return "Thumbs Down"

    return "Open Palm"

# Start webcam
cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb_frame)
        hand_results = hands.process(rgb_frame)

        # Draw pose landmarks
        mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # Detect pose-based action
        action = detect_action(results)

        # Detect hand gestures
        gesture = "No Gesture"
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = detect_hand_gesture(hand_landmarks)
        
        # Display detected actions and gestures
        cv2.putText(frame, f"Action: {action}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Show frame
        cv2.imshow('Action & Gesture Detection', frame)

        # Press 'q' to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
