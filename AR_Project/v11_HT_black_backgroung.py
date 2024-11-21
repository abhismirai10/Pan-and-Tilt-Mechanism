import cv2
import mediapipe as mp
import numpy as np

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

        # Create a black screen
        black_screen = np.zeros(frame.shape, dtype=np.uint8)

        # Flip the image horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        # Draw only hand landmarks and connections on black screen
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw connections between landmarks
                mp_drawing.draw_landmarks(
                    black_screen, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=0),
                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                )

                # Access landmark coordinates (e.g., tip of the index finger)
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = frame.shape
                cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                # Draw a circle at the index finger tip
                cv2.circle(black_screen, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        # Display the output
        cv2.imshow("Hand Tracking", black_screen)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
