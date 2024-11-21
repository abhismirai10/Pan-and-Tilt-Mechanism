import cv2
import numpy as np
import face_recognition as fr

# Load the known face and encode it
known_image = fr.load_image_file('AR_Project/Face_Recognition/known_faces/person_1/person_1_face-5.jpg')
known_face_encoding = fr.face_encodings(known_image)[0]

# Open the webcam
cap = cv2.VideoCapture(0)

# Handle camera not opening
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Display resolution
monitor_width = 2160
monitor_height = 1200

# Create windows before moving them
cv2.namedWindow("rightside", cv2.WINDOW_NORMAL)
cv2.namedWindow("leftside", cv2.WINDOW_NORMAL)

# Loop through the video frames
while True:
    # Read a frame from the video
    success, frame = cap.read()
    if not success:
        break

    # Create a black screen matching the frame size
    black_screen = np.zeros_like(frame)

    # Convert frame to RGB for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces and get their encodings
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the face with the known face
        matches = fr.compare_faces([known_face_encoding], face_encoding)

        if matches[0]:
            # Match found, draw rectangle and label
            x1, y1, x2, y2 = left, top, right, bottom
            color = (255, 255, 255)  # White color
            cv2.rectangle(black_screen, (x1, y1), (x2, y2), color, 3)

            # Prepare label
            label = "person id 10, NASA employee, Jaycon.INC"

            # Put text above the rectangle
            cv2.putText(
                black_screen,
                label,
                (x1, max(0, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2,
            )

    # Flip the image horizontally
    black_screen = cv2.flip(black_screen, 1)

    # Rotate the screens
    rotated_left = cv2.rotate(black_screen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated_right = cv2.rotate(black_screen, cv2.ROTATE_90_CLOCKWISE)

    # Resize the rotated frames
    resized_left = cv2.resize(rotated_left, (monitor_width // 2, monitor_height))
    resized_right = cv2.resize(rotated_right, (monitor_width // 2, monitor_height))

    # Display the frames
    cv2.imshow("rightside", resized_left)
    cv2.imshow("leftside", resized_right)

    # Set window position and size
    window_x, window_y = 1512, 0
    cv2.moveWindow("rightside", window_x, window_y)
    cv2.resizeWindow("rightside", monitor_width // 2, monitor_height)

    cv2.moveWindow("leftside", window_x + monitor_width // 2, window_y)
    cv2.resizeWindow("leftside", monitor_width // 2, monitor_height)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display windows
cap.release()
cv2.destroyAllWindows()
