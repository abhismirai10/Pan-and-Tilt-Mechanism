import cv2

#display res 2160*1200
monitor_width = 2160
monitor_height = 1200

# Set window position and size
window_x, window_y = 1512, 0

# Path to the image
image_path_right = "AR_Project_2/right.png"
image_path_left = "AR_Project_2/left.png"

# Read the image
image_right = cv2.imread(image_path_right)
image_right = cv2.resize(image_right, (monitor_height, monitor_width//2))
image_right = cv2.rotate(image_right, cv2.ROTATE_90_COUNTERCLOCKWISE)

image_left = cv2.imread(image_path_left)
image_left = cv2.resize(image_left, (monitor_height, monitor_width//2))
image_left = cv2.rotate(image_left, cv2.ROTATE_90_CLOCKWISE)

# Create a window and display the image
cv2.namedWindow("right", cv2.WINDOW_NORMAL)
cv2.imshow("right", image_right)

cv2.moveWindow("right", window_x, window_y)
cv2.resizeWindow("right", int(monitor_width / 2), monitor_height)

cv2.namedWindow("left", cv2.WINDOW_NORMAL)
cv2.imshow("left", image_left)

cv2.moveWindow("left", int(window_x + monitor_width/2), window_y)
cv2.resizeWindow("left", int(monitor_width / 2), monitor_height)

# Wait until a key is pressed, then close the window
print("Press any key to exit...")
cv2.waitKey(0)
cv2.destroyAllWindows()
