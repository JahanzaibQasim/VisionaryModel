import torch
import cv2

def load_model():
    # Load YOLOv5 model (choose from yolov5s, yolov5m, yolov5l, yolov5x)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Using the smallest YOLOv5 model
    return model

def process_frame(frame, model):
    # Run YOLOv5 detection on the current frame
    results = model(frame)
    
    # Render results on the frame (bounding boxes, labels, and confidence)
    frame = results.render()[0]  # results.render() returns a list of images with annotations
    return frame

def real_time_detection(model):
    # Open webcam (use 0 for default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame from webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        # Process the frame and get the detected objects
        frame_with_results = process_frame(frame, model)

        # Display the resulting frame with detections
        cv2.imshow("YOLOv5 Real-Time Detection", frame_with_results)

        # Exit the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model = load_model()  # Load the model
    real_time_detection(model)  # Start real-time object detection
