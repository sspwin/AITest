# Proxmox Cluster Inventory Script

This script fetches the inventory (nodes, VMs, and LXC containers) from a Proxmox cluster using the Proxmox API.

## Prerequisites

- Python 3.x
- `proxmoxer` and `requests` libraries

## Setup

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set the following environment variables with your Proxmox cluster details:

   - `PROXMOX_HOST`: The hostname or IP address of your Proxmox server.
   - `PROXMOX_USER`: Your Proxmox username (e.g., `root@pam`).
   - `PROXMOX_PASSWORD`: Your Proxmox password.
   - `PROXMOX_VERIFY_SSL`: (Optional) Set to `True` to enable SSL verification. Defaults to `False`.

   Example:
   ```bash
   export PROXMOX_HOST="192.168.1.10"
   export PROXMOX_USER="root@pam"
   export PROXMOX_PASSWORD="yourpassword"
   export PROXMOX_VERIFY_SSL="False"
   ```

## Usage

Run the script using Python:

```bash
python3 proxmox_inventory.py
```

The script will connect to the cluster and print a summary of all nodes, virtual machines, and containers found.
