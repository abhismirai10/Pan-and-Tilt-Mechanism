import cv2
import os
import time

# Set the number of persons (change as needed)
num_persons = 1  # You can change this value to the desired number of persons

# Number of images to capture per person
images_per_person = 5

# Delay between captures (in seconds)
delay_between_captures = 3  # 3 seconds

# Directory to store the images
train_dir = 'train_dir'

# Create the main directory if it doesn't exist
if not os.path.exists(train_dir):
    os.makedirs(train_dir)

# Initialize the video capture
cap = cv2.VideoCapture(0)

for person_num in range(1, num_persons + 1):
    person_name = f'person_{person_num}'
    person_dir = os.path.join(train_dir, person_name)
    
    # Create a directory for the person if it doesn't exist
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)
    
    print(f"\nCapturing images for {person_name}. Please look at the camera.")
    images_captured = 0

    while images_captured < images_per_person:
        # Start the countdown
        for countdown in range(delay_between_captures, 0, -1):
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image. Retrying...")
                continue
            
            # Display countdown on the frame
            display_text = f"Capturing {person_name}_face-{images_captured + 1}.jpg in {countdown}s"
            cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2, cv2.LINE_AA)
            
            cv2.imshow("Image Capture", frame)
            key = cv2.waitKey(1000)  # Wait for 1 second
            if key & 0xFF == ord('q'):
                print("Capture interrupted by user.")
                cap.release()
                cv2.destroyAllWindows()
                exit()
        
        # Capture the image after the countdown
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image. Retrying...")
            continue

        # Display a marker indicating that the image is being taken
        display_text = f"Capturing {person_name}_face-{images_captured + 1}.jpg"
        cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Image Capture", frame)
        cv2.waitKey(500)  # Brief pause to show the capture marker

        # Save the image
        image_name = f'{person_name}_face-{images_captured + 1}.jpg'
        image_path = os.path.join(person_dir, image_name)
        cv2.imwrite(image_path, frame)
        
        images_captured += 1
        print(f"Captured {image_name}")

    print(f"\nFinished capturing images for {person_name}.")

print("\nImage capture completed.")
print(f"Images are saved in the '{train_dir}' directory.")

# Release resources
cap.release()
cv2.destroyAllWindows()
