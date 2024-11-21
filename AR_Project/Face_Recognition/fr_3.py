import cv2
import face_recognition as fr
import os
import numpy as np

# Open the webcam
webcam = cv2.VideoCapture(0)

# Check if webcam is opened correctly
if not webcam.isOpened():
    raise IOError("Cannot open webcam")

# Set the webcam resolution to high quality
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
webcam.set(cv2.CAP_PROP_FPS, 30)

# Setup font for text in video
font = cv2.FONT_HERSHEY_SIMPLEX

# Function to load and encode faces
def load_and_encode_faces(person_name, person_folder):
    encodings = []
    images = os.listdir(person_folder)
    for img_name in images:
        image_path = os.path.join(person_folder, img_name)
        # Load the image
        image = fr.load_image_file(image_path)
        if image is None:
            print(f"Cannot open image at {image_path}")
            continue
        # Align the face (optional)
        # image = align_face(image)
        # Detect face locations using the CNN model
        face_locations = fr.face_locations(image, model='cnn')
        if len(face_locations) != 1:
            print(f"Image {image_path} not suitable for training: Found {len(face_locations)} faces.")
            continue
        # Get the face encoding
        face_encoding = fr.face_encodings(image, known_face_locations=face_locations)[0]
        encodings.append(face_encoding)
    return encodings

# Load and encode known faces
known_faces = {}

# Path to the directory containing subdirectories of known faces
known_faces_dir = 'AR_Project/Face_Recognition/known_faces/'

# Loop through each person in the known faces directory
for name in os.listdir(known_faces_dir):
    person_dir = os.path.join(known_faces_dir, name)
    if not os.path.isdir(person_dir):
        continue

    # Load and encode faces for the person
    encodings = load_and_encode_faces(name, person_dir)
    if encodings:
        known_faces[name] = encodings
    else:
        print(f"No valid face encodings found for {name}.")

# Main loop to read and process frames
while True:
    ret, frame = webcam.read()

    # If the frame was not read correctly, then we break the loop
    if not ret:
        print("Failed to read frame from webcam. Exiting...")
        break

    # Convert the image from BGR color to RGB color
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations using the CNN model
    face_locations = fr.face_locations(rgb_frame, model='cnn')
    # Get face encodings for all faces in the frame
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    # Process each face in the frame
    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Initialize variables
        face_name = "Unknown Person"
        lowest_distance = float('inf')
        best_match_name = None

        # Compare face encoding with known faces
        for known_name, known_encodings in known_faces.items():
            distances = fr.face_distance(known_encodings, face_encoding)
            min_distance = np.min(distances)
            if min_distance < lowest_distance:
                lowest_distance = min_distance
                best_match_name = known_name

        # Set a threshold for recognizing a face
        # Lower threshold means stricter matching
        threshold = 0.4
        if lowest_distance < threshold:
            face_name = best_match_name

        # Draw a rectangle around the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the face name and distance
        label = f"{face_name} ({lowest_distance:.2f})"
        cv2.putText(frame, label, (left, top - 10), font, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release the VideoCapture and destroy all windows
webcam.release()
cv2.destroyAllWindows()
