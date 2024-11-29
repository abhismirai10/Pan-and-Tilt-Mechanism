import cv2
import time
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11n.pt")

# Specify the target class ID for "cell phone"
TARGET_CLASS_ID = 67

# Open the video file or camera feed
cap = cv2.VideoCapture(0)

# Initialize variables for tracking
tracker = None
is_tracking = False
frame_counter = 0
REINIT_DETECTION_FRAME_INTERVAL = 30  # Run YOLO every 30 frames to refresh tracking

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame_counter += 1

        if not is_tracking or frame_counter % REINIT_DETECTION_FRAME_INTERVAL == 0:
            # Run YOLO inference periodically or if not tracking
            results = model(frame)

            # Get detections for the first result (frame)
            detections = results[0].boxes

            for box in detections:
                class_id = int(box.cls[0])  # Get the class ID

                # Check if the detected class matches the target class ID
                if class_id == TARGET_CLASS_ID:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Initialize a tracker with the detected bounding box
                    tracker = cv2.TrackerCSRT_create()  # Use CSRT tracker for better accuracy
                    tracker.init(frame, (x1, y1, x2 - x1, y2 - y1))
                    is_tracking = True
                    break  # Only initialize one tracker
        else:
            # Update tracker
            tracking_success, bbox = tracker.update(frame)

            if tracking_success:
                # Extract the updated bounding box
                x, y, w, h = map(int, bbox)
                center_x, center_y = x + w // 2, y + h // 2  # Calculate the center point

                # Draw tracking bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue box

                # Draw the center point
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot for center

                # Add label
                cv2.putText(
                    frame,
                    "Tracking cell phone",
                    (x, y - 10),  # Position above the box
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,  # Font scale
                    (255, 0, 0),  # Font color (Blue)
                    2,  # Thickness
                    cv2.LINE_AA,
                )
            else:
                # If tracking fails, reset
                is_tracking = False

        # Display the frame
        cv2.imshow("YOLO Tracking - Cell Phone", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
