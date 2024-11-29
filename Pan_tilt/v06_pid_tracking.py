import cv2
import time
from ultralytics import YOLO
from dynamixel_sdk import *  # Import Dynamixel SDK

# Load the YOLO model
model = YOLO("yolo11m.pt")

# Specify the target class ID for 67 "cell phone", 46 banana, 47 apple 
TARGET_CLASS_ID = 46

# Open the video file or camera feed
cap = cv2.VideoCapture(0)

# Dynamixel Configuration
ADDR_TORQUE_ENABLE = 64       # Torque enable
ADDR_GOAL_POSITION = 116      # Goal position
ADDR_PRESENT_POSITION = 132   # Present position
PROTOCOL_VERSION = 2.0        # Protocol version
BAUDRATE = 57600              # Baudrate
DEVICENAME = '/dev/ttyUSB0'   # Adjust to your USB port
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
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(
            f"Communication error for servo {servo_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(
            f"Error for servo {servo_id}: {packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Torque enabled for servo {servo_id}")

# Function to set servo position
def set_position(servo_id, position):
    position = max(SERVO_MIN, min(SERVO_MAX, position))  # Clamp position within valid range
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, servo_id, ADDR_GOAL_POSITION, position)
    if dxl_comm_result != COMM_SUCCESS:
        print(
            f"Communication error for servo {servo_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(
            f"Error for servo {servo_id}: {packetHandler.getRxPacketError(dxl_error)}")

# ADDR_MOVING_SPEED = 112  # Replace with your servo's correct address

# def set_speed(servo_id, speed):
#     speed = max(0, min(1023, speed))  # Adjust the range according to your servo model
#     dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
#         portHandler, servo_id, ADDR_MOVING_SPEED, speed)
#     # Error handling as before

# # Set maximum speed for both servos
# set_speed(PAN_ID, 1023)
# set_speed(TILT_ID, 1023)

# PID Controller Class
class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0.0):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Desired value
        self.integral = 0.0
        self.previous_error = 0.0
        self.previous_time = time.time()
        
    def update(self, current_value):
        current_time = time.time()
        dt = current_time - self.previous_time
        if dt <= 0.0:
            dt = 1e-16  # Prevent division by zero
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        self.previous_time = current_time
        return output

# Initialize tracking variables
tracker = None
is_tracking = False
frame_counter = 0
REINIT_DETECTION_FRAME_INTERVAL = 5  # Run YOLO every 10 frames to refresh tracking

# Servo positions
pan_position = CENTER_POSITION
tilt_position = CENTER_POSITION
set_position(PAN_ID, pan_position)
set_position(TILT_ID, tilt_position)

# Initialize PID controllers for pan and tilt
# Adjust the kp, ki, kd values as needed
pan_pid = PIDController(kp=0.11, ki=0.001, kd=0.02)
tilt_pid = PIDController(kp=0.13, ki=0.001, kd=0.02)

# Limit maximum adjustment per frame to prevent abrupt changes
MAX_ADJUSTMENT = 60  # Adjust this value as needed

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
                center_x, center_y = x + w / 2, y + h / 2  # Calculate the center point

                # Draw tracking bounding box
                cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2)  # Blue box

                # Draw the center point
                cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)  # Red dot for center

                # Add label
                cv2.putText(
                    frame,
                    "Tracking cell phone",
                    (int(x), int(y) - 10),  # Position above the box
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,  # Font scale
                    (255, 0, 0),  # Font color (Blue)
                    2,  # Thickness
                    cv2.LINE_AA,
                )

                # Adjust pan and tilt positions based on tracking center
                # Normalize error between -1 and 1
                error_x = (center_x - frame_width / 2) / (frame_width / 2)
                error_y = (center_y - frame_height / 2) / (frame_height / 2)

                # Calculate control signals from PID controllers
                pan_adjustment = pan_pid.update(error_x)
                tilt_adjustment = tilt_pid.update(error_y)

                # Scale the adjustment appropriately and limit it
                pan_adjustment = max(-MAX_ADJUSTMENT, min(MAX_ADJUSTMENT, pan_adjustment * 1000))
                tilt_adjustment = max(-MAX_ADJUSTMENT, min(MAX_ADJUSTMENT, tilt_adjustment * 1000))

                # Update positions
                pan_position += int(pan_adjustment)
                tilt_position += int(tilt_adjustment)

                # Clamp the values within servo limits
                pan_position = max(SERVO_MIN, min(SERVO_MAX, pan_position))
                tilt_position = max(SERVO_MIN, min(SERVO_MAX, tilt_position))

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
    packetHandler.write1ByteTxRx(
        portHandler, servo_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
portHandler.closePort()
print("Torque disabled and port closed")

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
