import numpy as np
import cv2

def on_trackbar_change(val):
    pass

def initialize_trackbars(window_name):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 400, 200)
    cv2.createTrackbar('Hue Low', window_name, 82, 179, on_trackbar_change)
    cv2.createTrackbar('Hue High', window_name, 125, 179, on_trackbar_change)
    cv2.createTrackbar('Sat Low', window_name, 128, 255, on_trackbar_change)
    cv2.createTrackbar('Sat High', window_name, 243, 255, on_trackbar_change)
    cv2.createTrackbar('Val Low', window_name, 154, 255, on_trackbar_change)
    cv2.createTrackbar('Val High', window_name, 251, 255, on_trackbar_change)

def get_trackbar_values(window_name):
    hue_low = cv2.getTrackbarPos('Hue Low', window_name)
    hue_high = cv2.getTrackbarPos('Hue High', window_name)
    sat_low = cv2.getTrackbarPos('Sat Low', window_name)
    sat_high = cv2.getTrackbarPos('Sat High', window_name)
    val_low = cv2.getTrackbarPos('Val Low', window_name)
    val_high = cv2.getTrackbarPos('Val High', window_name)
    return hue_low, hue_high, sat_low, sat_high, val_low, val_high

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Set the webcam resolution (match working script)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Initialize trackbars
    trackbar_window = 'Trackbars'
    initialize_trackbars(trackbar_window)

    print("Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue_low, hue_high, sat_low, sat_high, val_low, val_high = get_trackbar_values(trackbar_window)

        lower_bound = np.array([hue_low, sat_low, val_low])
        upper_bound = np.array([hue_high, sat_high, val_high])
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 50:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                center_x, center_y = x + w // 2, y + h // 2
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        cv2.imshow('Original Frame', frame)
        cv2.imshow('Mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
