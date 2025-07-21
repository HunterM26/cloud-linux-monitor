# Cloud-Based Linux Server Performance Remote Dashboard

## Overview

This project is a full-stack cloud-based system performance monitoring tool. It uses a lightweight custom agent on a remote Linux server to collect live metrics and display them in a dynamic web dashboard built with Dash and Plotly. The system supports real-time monitoring, stress testing, adjustable thresholds, and visual alerts.

## Features

- Live Monitoring Dashboard: Displays CPU, memory, disk, network, and load usage in real-time.
- Dynamic Threshold Sliders: Users can set metric thresholds directly from the dashboard interface.
- Visual Alerts: Red dashed threshold lines and visual indicators when thresholds are exceeded.
- All-Metrics View or Individual View: Choose to monitor all metrics or just one from a dropdown.
- Stress Generator: Systemd service with `stress-ng` simulates system load (CPU, disk, memory).
- Custom Agent: Python script writes metrics to a named pipe for secure transfer.
- Secure SSH Tunnel: Port forwarding for local access to remote dashboard.
- Firewall Support: Configurable to allow only necessary ports.
- Fully Hosted on Google Cloud VM: Built and deployed on a Debian-based Google Cloud instance.

## Project Structure

    cloud-linux-monitor/
    ├── agent/
    │ └── agent.py # Python script to read system metrics and write to named pipe
    ├── dashboard/
    │ └── dashboard.py # Dash/Plotly web interface for real-time monitoring
    ├── stress/
    │ ├── stress.sh # Bash script for stress testing CPU, memory, and disk
    │ └── stress.service # systemd service file for stress.sh
    ├── setup/
    │ └── firewall.sh # (Optional) UFW setup script
    ├── .gitignore
    └── README.md

## Setup Instructions

### 1. SSH & Firewall

- Generate your SSH key and copy it to the VM:
  
      '''bash
      ssh-keygen -t ed25519 -C "gcp-ssh"
      ssh-copy-id -i ~/.ssh/your_key.pub humerthingy@<EXTERNAL_IP>
      
-Create a secure tunnel to access the dashboard:

    bash
    Copy code
    ssh -i ~/.ssh/your_key -L 8050:localhost:8050 humerthingy@<EXTERNAL_IP>
    (Optional) Enable UFW:

    bash
    Copy code
    sudo ufw allow OpenSSH
    sudo ufw allow 8050
    sudo ufw enable
    
###2. Install Requirements

    bash
    Copy code
    sudo apt update
    sudo apt install python3 python3-pip stress-ng
    pip3 install dash plotly psutil
    
###3. Start the Agent

-Run the Python agent to continuously write metrics:

    bash
    Copy code
    python3 agent/agent.py
    4. Run the Dashboard
    In a separate terminal:

    bash
    Copy code
    python3 dashboard/dashboard.py
    Then open http://localhost:8050 in your browser.

###5. Use the Stress Generator

-Enable the systemd service to simulate stress:

    bash
    Copy code
    sudo cp stress/stress.service /etc/systemd/system/
    sudo systemctl daemon-reexec
    sudo systemctl daemon-reload
    sudo systemctl enable stress.service
    sudo systemctl start stress.service
    To check status:
    
    bash
    Copy code
    sudo systemctl status stress.service
    
###Notes
   
    The agent and dashboard communicate via a named pipe: /tmp/sysmetrics.pipe
    
    Threshold sliders let you fine-tune alert levels in real-time
    
    All changes are live; no need to restart dashboard after modifying sliders
