from dynamixel_sdk import *  # Import Dynamixel SDK

# Control Table Addresses
ADDR_TORQUE_ENABLE = 64       # Torque enable
ADDR_GOAL_POSITION = 116      # Goal position
ADDR_PRESENT_POSITION = 132   # Present position

# Protocol version
PROTOCOL_VERSION = 2.0        # Protocol version

# Default settings
DXL_ID = 1                    # Dynamixel ID
BAUDRATE = 57600              # Baudrate
DEVICENAME = '/dev/tty.usbserial-FT94VX0G'   # Adjust to your USB port

TORQUE_ENABLE = 1             # Enable torque
TORQUE_DISABLE = 0            # Disable torque

# Initialize PortHandler and PacketHandler
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

# Enable torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("Torque enabled")

# Function to set servo position
def set_position(position):
    if 0 <= position <= 4095:  # Ensure position is within valid range
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
        else:
            print(f"Position set to {position}")
    else:
        print("Invalid position. Must be in range 0-4095.")

# Continuous loop to set positions
try:
    while True:
        # Prompt user for position
        user_input = input("Enter position (0-4095) or type 'exit' to quit: ").strip()
        
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        
        # Validate input and set position
        if user_input.isdigit():
            position = int(user_input)
            set_position(position)
        else:
            print("Invalid input. Please enter a number between 0 and 4095 or 'exit'.")
except KeyboardInterrupt:
    print("\nExiting loop...")

# Disable torque and close port
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
portHandler.closePort()
print("Torque disabled and port closed")
