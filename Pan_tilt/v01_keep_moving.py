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
DEVICENAME = '/dev/ttyUSB0'   # Adjust to your USB port

TORQUE_ENABLE = 1             # Enable torque
TORQUE_DISABLE = 0            # Disable torque

# Initialize PortHandler and PacketHandler
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Port opened successfully")
else:
    print("Failed to open port")
    quit()

# Set baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Baudrate set successfully")
else:
    print("Failed to set baudrate")
    quit()

# Enable torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("Torque enabled")

# Move in a while loop
try:
    while True:
        # Move to position 0
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, 0)
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Error moving to position 0: {packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            print(f"Servo error: {packetHandler.getRxPacketError(dxl_error)}")
        else:
            print("Moved to position 0")
        
        # Wait for 2 seconds
        time.sleep(2)

        # Move to position 4095
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, 4095)
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Error moving to position 4095: {packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            print(f"Servo error: {packetHandler.getRxPacketError(dxl_error)}")
        else:
            print("Moved to position 4095")
        
        # Wait for 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting loop")

# Disable torque and close port
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
portHandler.closePort()
print("Torque disabled and port closed")