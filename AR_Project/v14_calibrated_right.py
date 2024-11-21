import cv2
import numpy as np

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

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and resize the frame
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (monitor_height, monitor_width // 2))

    # Rotate the frame for "right" and "left" displays
    frame_right = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_left = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame_left[:] = 0  # Black screen for "left" window

    # Apply the homography to warp the frame
    warped_frame = cv2.warpPerspective(frame_right, h, (frame_right.shape[1], frame_right.shape[0]))

    # Display the warped frame
    cv2.imshow("right", warped_frame)
    cv2.imshow("right_main", warped_frame)
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

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
