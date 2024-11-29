import cv2
import time
from ultralytics import YOLO
from dynamixel_sdk import *  # Import Dynamixel SDK

# Load the YOLO model
model = YOLO("yolo11m.pt")

# Specify the target class ID for "cell phone"
TARGET_CLASS_ID = 67

# Open the video file or camera feed
cap = cv2.VideoCapture(0)

# Dynamixel Configuration
ADDR_TORQUE_ENABLE = 64       # Torque enable
ADDR_GOAL_POSITION = 116      # Goal position
ADDR_PRESENT_POSITION = 132   # Present position
PROTOCOL_VERSION = 2.0        # Protocol version
BAUDRATE = 57600              # Baudrate
DEVICENAME = '/dev/tty.usbserial-FT94VX0G'   # Adjust to your USB port
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
PAN_ID = 1                    # Pan servo ID
TILT_ID = 2                   # Tilt servo ID
SERVO_MIN = 0
SERVO_MAX = 4095
CENTER_POSITION = 2048        # Servo center position

# Initialize Dynamixel PortHandler and PacketHandler
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if not portHandler.openPort():
    print("Failed to open the port!")
    quit()

# Set baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to set baudrate!")
    quit()

# Enable torque for both servos
for servo_id in [PAN_ID, TILT_ID]:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Communication error for servo {servo_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error for servo {servo_id}: {packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Torque enabled for servo {servo_id}")

# Function to set servo position
def set_position(servo_id, position):
    position = max(SERVO_MIN, min(SERVO_MAX, position))  # Clamp position within valid range
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, servo_id, ADDR_GOAL_POSITION, position)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Communication error for servo {servo_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error for servo {servo_id}: {packetHandler.getRxPacketError(dxl_error)}")

# Initialize tracking variables
tracker = None
is_tracking = False
frame_counter = 0
REINIT_DETECTION_FRAME_INTERVAL = 30  # Run YOLO every 30 frames to refresh tracking

# Servo positions
pan_position = CENTER_POSITION
tilt_position = CENTER_POSITION
set_position(PAN_ID, pan_position)
set_position(TILT_ID, tilt_position)

# Image dimensions
frame_width, frame_height = 640, 480  # Default values; will update with the first frame

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame_counter += 1
        frame_height, frame_width = frame.shape[:2]

        if not is_tracking or frame_counter % REINIT_DETECTION_FRAME_INTERVAL == 0:
            # Run YOLO inference periodically or if not tracking
            results = model(frame)

            # Get detections for the first result (frame)
            detections = results[0].boxes

            for box in detections:
                class_id = int(box.cls[0])  # Get the class ID

                # Check if the detected class matches the target class ID
                if class_id == TARGET_CLASS_ID:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Initialize a tracker with the detected bounding box
                    tracker = cv2.TrackerCSRT_create()  # Use CSRT tracker for better accuracy
                    tracker.init(frame, (x1, y1, x2 - x1, y2 - y1))
                    is_tracking = True
                    break  # Only initialize one tracker
        else:
            # Update tracker
            tracking_success, bbox = tracker.update(frame)

            if tracking_success:
                # Extract the updated bounding box
                x, y, w, h = map(int, bbox)
                center_x, center_y = x + w // 2, y + h // 2  # Calculate the center point

                # Draw tracking bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue box

                # Draw the center point
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot for center

                # Add label
                cv2.putText(
                    frame,
                    "Tracking cell phone",
                    (x, y - 10),  # Position above the box
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,  # Font scale
                    (255, 0, 0),  # Font color (Blue)
                    2,  # Thickness
                    cv2.LINE_AA,
                )

                # Adjust pan and tilt positions based on tracking center
                error_x = center_x - frame_width // 2
                error_y = center_y - frame_height // 2

                # Print error for debugging
                print(f"Error X: {error_x}, Error Y: {error_y}")

                # Scale errors to adjust servo positions proportionally
                # Scaling factor (0.1) can be adjusted for smoother movement
                pan_position -= int(error_x * 0.5)
                tilt_position -= int(error_y * 0.5)

                # Clamp the values within servo limits
                pan_position = max(SERVO_MIN, min(SERVO_MAX, pan_position))
                tilt_position = max(SERVO_MIN, min(SERVO_MAX, tilt_position))

                # Print new servo positions for debugging
                print(f"Pan Position: {pan_position}, Tilt Position: {tilt_position}")

                # Update servo positions
                set_position(PAN_ID, pan_position)
                set_position(TILT_ID, tilt_position)

            else:
                # If tracking fails, reset
                is_tracking = False

        # Display the frame
        cv2.imshow("YOLO Tracking with Dynamixel Control", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Disable torque and close port
for servo_id in [PAN_ID, TILT_ID]:
    packetHandler.write1ByteTxRx(portHandler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
portHandler.closePort()
print("Torque disabled and port closed")

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
