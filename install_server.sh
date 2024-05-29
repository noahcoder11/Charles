#!/bin/bash
#If needed, stop and unload the current charles service
systemctl stop charles_monitor.service || true
systemctl disable charles_monitor.service || true

#Create the main service file
\cp -rf ./charles_monitor.service /lib/systemd/system/charles_monitor.service

#Enable the service
systemctl enable charles_monitor.service
systemctl start charles_monitor.service

echo "The Charles Monitor service is enabled and started."
exit 0