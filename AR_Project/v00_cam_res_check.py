import cv2

# Open the webcam
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Error: Cannot access the webcam.")
    exit()

# Function to check available resolutions
def list_resolutions(webcam):
    resolutions = [
        (160, 120), (320, 240), (640, 480), (800, 600), (1024, 768),
        (1280, 720), (1920, 1080)
    ]
    supported_resolutions = []

    for width, height in resolutions:
        webcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        actual_width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if int(actual_width) == width and int(actual_height) == height:
            supported_resolutions.append((width, height))

    return supported_resolutions

# List and display available resolutions
print("Checking supported resolutions...")
supported = list_resolutions(webcam)
print("Supported Resolutions:")
for res in supported:
    print(f"{res[0]}x{res[1]}")

# Set your desired resolution
desired_width = 1280
desired_height = 720
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
webcam.set(cv2.CAP_PROP_FPS, 30)

# Confirm settings
actual_width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Webcam set to resolution: {int(actual_width)}x{int(actual_height)}")

# Release the webcam
webcam.release()
