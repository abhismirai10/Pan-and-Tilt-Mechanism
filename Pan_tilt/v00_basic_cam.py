import cv2

# Open the webcam
webcam = cv2.VideoCapture(0)

# Check if webcam is opened correctly
if not webcam.isOpened():
    raise IOError("Cannot open webcam")

# Set the webcam resolution
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
webcam.set(cv2.CAP_PROP_FPS, 30)

# Setup font for text in video
font = cv2.FONT_HERSHEY_SIMPLEX

# Main loop to read and process frames
while True:
    ret, frame = webcam.read()

    # If the frame was not read correctly, then we break the loop
    if not ret:
        break

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy all windows
webcam.release()
cv2.destroyAllWindows()
