
# Sysmon
Sysmon is a lightweight, interactive system monitor for Linux written in Python.  
It provides real-time information about CPU, memory, disk, network, and processes — similar to `htop`, but simplified and customizable.

---

## Features
- Live dashboard with system information (OS, kernel, machine type)
- CPU usage per core
- Memory usage (total, used, percentage)
- Disk usage
- Network traffic (sent/received)
- Process monitoring with scrollable list
- Interactive controls:
  - ↑ / ↓ : Scroll through processes
  - q : Quit
  - c : Sort by CPU usage
  - m : Sort by Memory usage

---

## Installation

Clone the repository:
```bash
git clone https://github.com/artnuel4u/sysmon.git
cd sysmon
pip install psutil

## Make the script installable


chmod +x sysmon.py
sudo mv sysmon.py /usr/local/bin/sysmon


## Usage

sysmon




