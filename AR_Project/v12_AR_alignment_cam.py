import cv2
import numpy as np

# Set up webcam or video capture
cap = cv2.VideoCapture(0)

# Handle camera not opening
if not cap.isOpened():
    raise IOError("Cannot open webcam")

#macbook res 1512x982
#display res 2160*1200
monitor_width = 2160
monitor_height = 1200

#mac screen ends
window_x, window_y = 1512, 0

# Set resolution 
# Supported resolutions: 640 x 480, 1280 x 720, 1920 x 1080
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, 30)

# Create windows before moving them
cv2.namedWindow("right", cv2.WINDOW_NORMAL)
cv2.namedWindow("left", cv2.WINDOW_NORMAL)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    #flip the main frame
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (monitor_height, monitor_width//2))

    # Rotate the frame 90 degrees counterclockwise and clockwise
    frame_right = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_left = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Display the combined frame
    cv2.imshow("right", frame_right)
    #cv2.imshow("left", frame_left)

    # Set window position and size
    cv2.moveWindow("right", window_x, window_y)
    cv2.resizeWindow("right", int(monitor_width / 2), monitor_height)

    cv2.moveWindow("left", int(window_x + monitor_width/2), window_y)
    cv2.resizeWindow("left", int(monitor_width / 2), monitor_height)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
