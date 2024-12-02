#!/bin/bash

# Run scripts sequentially
echo "Starting imu.sh..."
gnome-terminal -- bash -c "./imu.sh; exec bash"
sleep 5

echo "Starting lidar.sh..."
gnome-terminal -- bash -c "./lidar.sh; exec bash"
sleep 5

echo "Starting tortle.sh..."
gnome-terminal -- bash -c "./tortle.sh; exec bash"
sleep 5

echo "Starting ekf.sh...."
gnome-terminal -- bash -c "./ekf.sh; exec bash"
sleep 5

echo "Starting async.sh...."
gnome-terminal -- bash -c "./async.sh; exec bash"
sleep 5

echo "Starting rviz.sh...."
gnome-terminal -- bash -c "./rviz.sh; exec bash"