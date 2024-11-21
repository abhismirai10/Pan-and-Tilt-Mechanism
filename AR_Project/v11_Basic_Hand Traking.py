import cv2
import mediapipe as mp

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Set up webcam
cap = cv2.VideoCapture(0)

# Use MediaPipe Hands
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        # Draw the hand annotations on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Access landmark coordinates (e.g., tip of the index finger)
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = frame.shape
                cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                # Draw a circle at the index finger tip
                cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        # Display the output
        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
