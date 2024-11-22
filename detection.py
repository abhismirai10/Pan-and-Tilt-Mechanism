import cv2
import time
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("best.pt")

# Open the video file or camera feed
# video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture(0)

# Initialize variables for FPS calculation
fps = 0
frame_count = 0
start_time = time.time()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Start timing for FPS calculation
        frame_start_time = time.time()

        # Run YOLO inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Calculate FPS
        frame_end_time = time.time()
        fps = 1 / (frame_end_time - frame_start_time)

        # Display FPS on the frame
        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.2f}",
            (10, 30),  # Position (x=10, y=30)
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Font scale
            (0, 255, 0),  # Font color (Green)
            2,  # Thickness
            cv2.LINE_AA,
        )

        # Display the annotated frame
        cv2.imshow("YOLO Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
