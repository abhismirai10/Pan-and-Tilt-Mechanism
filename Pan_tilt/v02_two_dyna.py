from dynamixel_sdk import *  # Import Dynamixel SDK
import time

# Control Table Addresses
ADDR_TORQUE_ENABLE = 64       # Torque enable
ADDR_GOAL_POSITION = 116      # Goal position
ADDR_PRESENT_POSITION = 132   # Present position

# Protocol version
PROTOCOL_VERSION = 2.0        # Protocol version

# Default settings
DXL_IDS = [1, 2]              # Dynamixel IDs for servos
BAUDRATE = 57600              # Baudrate
DEVICENAME = '/dev/ttyUSB1'   # Adjust to your USB port

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

# Enable torque for both servos
for DXL_ID in DXL_IDS:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error enabling torque for ID {DXL_ID}: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Servo error for ID {DXL_ID}: {packetHandler.getRxPacketError(dxl_error)}")
    else:
        print(f"Torque enabled for ID {DXL_ID}")

# Move both servos in a while loop
try:
    while True:
        for goal_position in [0, 4095]:
            for DXL_ID in DXL_IDS:
                # Write goal position for each servo
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
                if dxl_comm_result != COMM_SUCCESS:
                    print(f"Error moving ID {DXL_ID} to position {goal_position}: {packetHandler.getTxRxResult(dxl_comm_result)}")
                elif dxl_error != 0:
                    print(f"Servo error for ID {DXL_ID}: {packetHandler.getRxPacketError(dxl_error)}")
                else:
                    print(f"ID {DXL_ID} moved to position {goal_position}")
            
            # Wait for 2 seconds before switching positions
            time.sleep(2)

except KeyboardInterrupt:
    print("Exiting loop")

# Disable torque and close port
for DXL_ID in DXL_IDS:
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    print(f"Torque disabled for ID {DXL_ID}")

portHandler.closePort()
print("Port closed")
