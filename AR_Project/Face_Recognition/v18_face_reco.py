import cv2
import numpy as np
import face_recognition as fr
from screeninfo import get_monitors

# Source and destination points from previous calibration
src_points = np.float32([(47, 351), (64, 494), (92, 611), (207, 325), (246, 451), (262, 571), (374, 320), (401, 433), (422, 543)])
dst_points = np.float32([(220, 296), (218, 430), (237, 580), (390, 287), (393, 416), (399, 545), (554, 289), (561, 396), (571, 512)])

# Compute the homography matrix
h, _ = cv2.findHomography(src_points, dst_points)

# Set up webcam or video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# # Find resolution of the monitor
# monitor = get_monitors()[0]
# monitor_width = monitor.width
# monitor_height = monitor.height

monitor_width = 2160
monitor_height = 1200

# Create windows before moving them
cv2.namedWindow("rightside", cv2.WINDOW_NORMAL)
cv2.namedWindow("leftside", cv2.WINDOW_NORMAL)

# Setup font for text
font = cv2.FONT_HERSHEY_SIMPLEX

# Load and encode known faces (you should replace the paths with actual images you have)
def load_and_encode_face(image_path):
    image = fr.load_image_file(image_path)
    face_locations = fr.face_locations(image)
    face_encoding = fr.face_encodings(image, face_locations)[0]
    return face_encoding

known_faces = {
    "Abhi": load_and_encode_face('AR_Project/Face_Recognition/photos/abhi.jpg'),
    "Derek": load_and_encode_face('AR_Project/Face_Recognition/photos/derek.jpg'),
    "Jay": load_and_encode_face('AR_Project/Face_Recognition/photos/jay.jpg'),
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and prepare the frame for face recognition
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Find all face locations and face encodings in the current frame
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    # Prepare black frames for displaying face bounding boxes
    black_frame = np.zeros(frame.shape, dtype=np.uint8)

    # Process each face in the frame
    for face_location, face_encoding in zip(face_locations, face_encodings):
        top, right, bottom, left = face_location
        # Draw bounding box around the face on the black frame
        cv2.rectangle(black_frame, (left, top), (right, bottom), (255, 255, 255), 3)

        # Default face name to "Unknown"
        face_name = "Unknown Person"

        # Check for matches with known faces
        for known_name, known_encoding in known_faces.items():
            match = fr.compare_faces([known_encoding], face_encoding, tolerance=0.50)
            if match[0]:
                face_name = known_name
                break

        # Display face name and message on black frame
        if face_name == "Abhi":
            cv2.putText(black_frame, "Hey Abhi, what's up!", (50, 500), font, 1, (255, 0, 0), 2)
        elif face_name == "Derek":
            cv2.putText(black_frame, "Derek COO Jaycon Systems", (50, 50), font, 1, (0, 255, 0), 2)
        elif face_name == "Jay":
            cv2.putText(black_frame, "Jay CEO Jaycon Systems", (50, 50), font, 1, (0, 0, 255), 2)
        else:
            cv2.putText(black_frame, face_name, (50, 50), font, 1, (255, 255, 255), 2)

    # Rotate frames
    frame_right = cv2.rotate(black_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_left = cv2.rotate(black_frame, cv2.ROTATE_90_CLOCKWISE)

    # Resize for the monitor's dimensions
    frame_right = cv2.resize(frame_right, (monitor_width // 2, monitor_height))
    frame_left = cv2.resize(frame_left, (monitor_width // 2, monitor_height))

    # Apply the homography warp to the right and left frames
    warped_frame_right = cv2.warpPerspective(frame_right, h, (frame_right.shape[1], frame_right.shape[0]))
    warped_frame_left = cv2.warpPerspective(frame_left, h, (frame_left.shape[1], frame_left.shape[0]))

    # Display the frames
    cv2.imshow("rightside", warped_frame_right)
    cv2.imshow("leftside", warped_frame_left)

    # Set window position and size
    window_x, window_y = 1512, 0
    cv2.moveWindow("rightside", window_x, window_y)
    cv2.resizeWindow("rightside", int(monitor_width / 2), monitor_height)

    cv2.moveWindow("leftside", int(window_x + monitor_width/2), window_y)
    cv2.resizeWindow("leftside", int(monitor_width / 2), monitor_height)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
