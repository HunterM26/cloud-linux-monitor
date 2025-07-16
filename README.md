# Cloud-Based Linux Server Performance Monitor

**Course**: COP3604 – System Administration Using Unix  
**Student**: Hunter Mathews  
**Instructor**: Professor Navarro  
**Project Type**: Solo

---

## Overview

This project is a custom-built monitoring system for a remote Linux server hosted on Google Cloud. It uses `stress-ng` to simulate system load and a Python-based agent to collect performance metrics. These metrics are passed through a named pipe and will be visualized using a real-time web-based GUI (Plotly Dash). Alerts will notify the user when performance crosses user-defined thresholds.

---

## What’s Working So Far

- Google Cloud VM running Ubuntu 22.04
- Simulated load using `stress-ng`, targeting:
  - CPU
  - Memory
  - Disk
  - I/O
  - Matrix operations
- `agent.py` script collects:
  - CPU usage
  - RAM usage
  - Disk usage
  - Network usage
  - Load average
- Agent writes formatted output to `/tmp/sysmetrics.pipe` (named pipe)
- Agent runs as a `systemd` service under a dedicated user (`auser`)
- Agent auto-restarts on failure via `systemd`
- `stress.sh` script runs automated `stress-ng` tests in a loop
- `stress.sh` is configured as a `systemd` service
- Git repo initialized and actively used for version control

---

## Still in Progress

- Cron job to ensure agent restarts if it fails unexpectedly
- Web-based dashboard using Plotly Dash for live data visualization
- Historical metric tracking
- Threshold alert system (color changes or popups)
- Ability to select and monitor multiple servers
- Adjustable threshold settings through the dashboard
- Restrict dashboard access by IP using firewall/VPC rules

---

## Project Folder Structure

-cloud-linux-monitor/
  -agent/
    -agent.py
    -agent.service
  -stress/
    -stress.sh
  -dashboard/
    -dashboard.py
  -README.md
  
---

## How to Use It

### Start the monitoring agent:
sudo systemctl start agent.service

### Check that agent is running
sudo systemctl status agent.service

### View live system metrics from pipe
cat /tmp/sysmetrics.pipe

### Start stress generator 
sudo systemctl start stress.service

### Check if stress script is running
sudo systemctl status stress.service

### Run dashboard


---

## Notes
7/16/2025 
    The backend is complete and working, working on web-based GUI for monitoring functionalilty (currently have the code working, working on web-based format)
