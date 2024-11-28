from dynamixel_sdk import *
# Control Table Addresses
ADDR_TORQUE_ENABLE = 64       # Torque enable
ADDR_GOAL_POSITION = 116      # Goal position
ADDR_PRESENT_POSITION = 132   # Present position

# Protocol version
PROTOCOL_VERSION = 2.0        # Use 2.0 for Dynamixel X series

# Default settings
DXL_ID = 1                    # ID of your Dynamixel
BAUDRATE = 57600              # Baudrate (use the correct value for your setup)
DEVICENAME = '/dev/ttyUSB0'   # Port (adjust to your setup)

TORQUE_ENABLE = 1             # Enable torque
TORQUE_DISABLE = 0            # Disable torque
DXL_MIN_POSITION = 0          # Minimum position (0 for some servos)
DXL_MAX_POSITION = 4095       # Maximum position (for 360-degree servos)

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Port opened successfully")
else:
    print("Failed to open port")
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Baudrate set successfully")
else:
    print("Failed to set baudrate")
    quit()

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("Torque enabled")

goal_position = 0  # Midpoint position for some servos

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print(f"Moved to position: {goal_position}")

present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print(f"Present Position: {present_position}")

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Communication error: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error occurred: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("Torque disabled")

portHandler.closePort()
