#!/bin/bash
#If needed, stop and unload the current charles service
systemctl stop charles.service || true
systemctl disable charles.service || true

#Create the main service file
\cp -rf ./charles.service /lib/systemd/system/charles.service

#Install the requirements
pip3 install -r requirements.txt

#Enable the service
systemctl enable charles.service

#Critical environment variable for Charles!
export PA_ALSA_PLUGHW=1

if [ -z "${CHARLES_INPUT_AUDIO_DEVICE}" -o -z "${CHARLES_OUTPUT_AUDIO_DEVICE}" ]; then
    if [ -z "${CHARLES_MONITOR_URL}" ]; then
        echo "The Charles service is enabled; to run setup and start it, you must configure it through the charles_monitor web service."
        echo "To start it, run:"
        echo "systemctl start charles.service"
        exit 1
    else
        echo "The Charles service is enabled; to run setup and start it, go to the charles_monitor web service."
        echo "${CHARLES_MONITOR_URL}"
        exit 1
    fi
else 
    #Start the service
    systemctl start charles.service
    echo "The Charles service is enabled and started."
    exit 0
fi