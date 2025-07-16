# Cloud-Based Linux Server Performance Monitor

**Course:** COP3604 – System Administration Using Unix  
**Student:** Hunter Mathews  
**Instructor:** Professor Navarro  
**Project Type:** Solo

## Overview

This project is a custom monitoring solution for a remote Linux server hosted on Google Cloud. It simulates server load using `stress-ng`, collects key system metrics with a custom Python agent, and sends them through a named pipe. A GUI dashboard will eventually display the data in real-time and alert users if performance thresholds are crossed.

## What’s Working So Far

- Cloud VM set up and running Ubuntu 22.04 on Google Cloud
- `stress-ng` load simulation targeting:
  - CPU
  - Memory
  - Disk
  - I/O
  - Matrix operations
- `agent.py` collects:
  - CPU usage
  - RAM usage
  - Disk usage
  - Network usage
  - Load average
- Agent writes output to `/tmp/sysmetrics.pipe` (named pipe)
- Agent runs as a systemd service under a dedicated user (`auser`)
- Agent restarts automatically on failure
- Project organized with Git and pushed to GitHub

## Still in Progress

- Cron job to restart the agent if it fails
- GUI dashboard (Tkinter or Plotly) to visualize real-time data
- Historical tracking and basic alert system (color or popup)
- Multi-server dashboard support
- Threshold settings UI
- API/IP restriction via firewall or VPC config

## Project Folder Structure

cloud-linux-monitor/
  agent/
    agent.py
    agent.service
  stress/
    stress.sh
  dashboard/
    dashboard.py
  README.md

## How to Use It

Start the monitoring agent:  
  sudo systemctl start agent.service

Check if it’s running:  
  sudo systemctl status agent.service

View real-time system metrics:  
  cat /tmp/sysmetrics.pipe

## Notes

Development is ongoing. The project currently meets several of the main requirements, with additional dashboard and automation features being built ahead of the in-class review.
