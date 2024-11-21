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

cv2.namedWindow("right_main", cv2.WINDOW_NORMAL)

#lists to hold the clicked points for calibration
src_points = []
dst_points = []

# Global flags to manage calibration stages
collecting_src_points = True
calibration_complete = False

# Mouse callback function to record points
def record_point(event, x, y, flags, params):
    global src_points, dst_points, collecting_src_points, calibration_complete, frame
    if event == cv2.EVENT_LBUTTONDOWN:
        # Collect points based on current phase
        if collecting_src_points and len(src_points) < 4:
            src_points.append((x, y))
        elif not collecting_src_points and len(dst_points) < 4:
            dst_points.append((x, y))

        # Transition to collecting destination points after 9 source points are collected
        if len(src_points) == 4 and collecting_src_points:
            collecting_src_points = False
            print("Switch to collecting destination points on the screen")

        # Complete calibration after collecting all points
        if len(dst_points) == 4:
            calibration_complete = True
            print("Calibration complete. Warping the image...")

#set mouse callback 
cv2.setMouseCallback("right", record_point)

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

    #lets make it all black
    frame_left[:] = 0

    # Display the selected points as they are clicked
    for point in src_points:
        cv2.circle(frame_right, point, 5, (0, 255, 0), -1)  # Green for source points
    for point in dst_points:
        cv2.circle(frame_right, point, 5, (255, 0, 0), -1)  # Blue for destination points

    # Display calibration status and point count
    if collecting_src_points:
        status_text = f"Calibration: Selecting Source Points ({len(src_points)}/9)"
    elif not calibration_complete:
        status_text = f"Calibration: Selecting Destination Points ({len(dst_points)}/9)"
    else:
        status_text = "Calibration Complete. Displaying Warped Image."

    cv2.putText(frame_right, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    if not calibration_complete:
        # Show the frame with points as they are clicked
        cv2.imshow("right", frame_right)
        cv2.imshow("right_main", frame_right)
    else:
        # Calculate homography after collecting 9 points each for source and destination
        src_pts_np = np.float32(src_points)
        dst_pts_np = np.float32(dst_points)
        h, status = cv2.findHomography(src_pts_np, dst_pts_np)

        # Warp the image using the homography matrix
        warped_frame = cv2.warpPerspective(frame_right, h, (frame_right.shape[1], frame_right.shape[0]))

        # Display the warped image to match the destination points
        cv2.imshow("right", warped_frame)
        cv2.imshow("right_main", warped_frame)
        

    # Display control info
    if collecting_src_points:
        print("Click on 9 points on the original frame.")
    elif not calibration_complete:
        print("Click on 9 points on the screen.")

    cv2.moveWindow("right", window_x, window_y)
    cv2.resizeWindow("right", int(monitor_width / 2), monitor_height)

    cv2.moveWindow("right_main", 0, 0)
    cv2.resizeWindow("right_main", int(monitor_width / 2), monitor_height)

    cv2.imshow("left", frame_left)
    cv2.moveWindow("left", int(window_x + monitor_width/2), window_y)
    cv2.resizeWindow("left", int(monitor_width / 2), monitor_height)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if calibration_complete:
            print("Source Points:", src_points)
            print("Destination Points:", dst_points)
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
