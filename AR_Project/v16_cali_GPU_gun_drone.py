import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Set up webcam or video capture
cap = cv2.VideoCapture(0)

# Handle camera not opening
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Monitor and resolution setup
monitor_width = 2160
monitor_height = 1200
window_x, window_y = 1512, 0

# Set resolution
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, 30)

# Create windows
cv2.namedWindow("right", cv2.WINDOW_NORMAL)
cv2.namedWindow("left", cv2.WINDOW_NORMAL)
cv2.namedWindow("right_main", cv2.WINDOW_NORMAL)

# Predefined calibration points
src_points = [(520, 591), (564, 812), (766, 622), (816, 821)]
dst_points = [(441, 459), (485, 742), (666, 468), (703, 703)]

# Convert points to NumPy format
src_pts_np = np.float32(src_points)
dst_pts_np = np.float32(dst_points)

# Compute the homography matrix
h, status = cv2.findHomography(src_pts_np, dst_pts_np)

# Load the YOLO model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO("best.pt").to(device)

# Class names mapping
class_names = model.names

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_black = np.zeros(frame.shape, dtype=np.uint8)
    
    #uncomment both line for rgb visulation
    frame_black = frame

    # Run YOLO object detection
    results = model.track(frame, conf=0.3, iou=0.5, persist=True, show=False, device=device)

    # Access detection results
    detections = results[0].boxes if len(results) > 0 else None

    if detections is not None and len(detections) > 0:
        boxes = detections.xyxy.cpu().numpy()  # Bounding boxes
        confs = detections.conf.cpu().numpy()  # Confidence scores
        class_ids = detections.cls.cpu().numpy().astype(int)  # Class IDs

        # Plot the tracks
        for box, conf, class_id in zip(boxes, confs, class_ids):
            x1, y1, x2, y2 = map(int, box)

            # Get the class name and confidence score
            class_name = class_names[class_id]
            conf_score = conf

            # Decide color based on class name
            if class_name == 'gun':
                color = (255, 255, 255)  # Default to white
                
            elif class_name == 'drone':
                color = (255, 255, 0)  # Blue in BGR
            else:
                color = (0, 0, 255)  # Red in BGR
                
            # Draw rectangle
            cv2.rectangle(frame_black, (x1, y1), (x2, y2), color, 3)

            # Prepare label with class name and confidence
            label = f"{class_name}: {conf_score:.2f}"

            # Put text above the rectangle
            cv2.putText(frame_black, label, (x1, max(0, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    frame_black = cv2.flip(frame_black, 1)
    frame = cv2.resize(frame_black, (monitor_height, monitor_width // 2))

    # Rotate the frame for "right" and "left" displays
    frame_right = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_left = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame_left[:] = 0  # Black screen for "left" window

    # Apply the homography to warp the right frame
    warped_frame_right = cv2.warpPerspective(frame_right, h, (frame_right.shape[1], frame_right.shape[0]))

    # Display the frames
    cv2.imshow("right", warped_frame_right)
    cv2.imshow("right_main", warped_frame_right)
    cv2.imshow("left", frame_left)

    # Move and resize windows
    cv2.moveWindow("right", window_x, window_y)
    cv2.resizeWindow("right", int(monitor_width / 2), monitor_height)

    cv2.moveWindow("right_main", 0, 0)
    cv2.resizeWindow("right_main", int(monitor_width / 2), monitor_height)

    cv2.moveWindow("left", int(window_x + monitor_width / 2), window_y)
    cv2.resizeWindow("left", int(monitor_width / 2), monitor_height)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
