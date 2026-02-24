import os
from proxmoxer import ProxmoxAPI

# Proxmox server details from environment variables
proxmox_host = os.getenv("PROXMOX_HOST", "proxmox_host")
proxmox_user = os.getenv("PROXMOX_USER", "user@pam")
proxmox_password = os.getenv("PROXMOX_PASSWORD", "password")
proxmox_verify_ssl = os.getenv("PROXMOX_VERIFY_SSL", "False").lower() == "true"

def fetch_inventory():
    """
    Connects to the Proxmox cluster and fetches the complete inventory.
    """
    try:
        # Establish connection to Proxmox API
        proxmox = ProxmoxAPI(
            proxmox_host,
            user=proxmox_user,
            password=proxmox_password,
            verify_ssl=proxmox_verify_ssl
        )

        print(f"Successfully connected to Proxmox cluster at {proxmox_host}.")
        print("-" * 50)

        # Get all nodes in the cluster
        nodes = proxmox.nodes.get()
        print(f"Found {len(nodes)} nodes in the cluster.")
        print("-" * 50)

        # Iterate through each node
        for node in nodes:
            name = node["node"]
            print(f"Node: {name}")
            print("-" * 30)

            # Get all QEMU (KVM) virtual machines on the node
            vms = proxmox.nodes(name).qemu.get()
            print(f"  QEMU VMs ({len(vms)}):")
            for v in vms:
                print(f"    - VMID: {v['vmid']}, Name: {v['name']}, Status: {v['status']}")

            print("-" * 30)

            # Get all LXC containers on the node
            cts = proxmox.nodes(name).lxc.get()
            print(f"  LXC Containers ({len(cts)}):")
            for c in cts:
                print(f"    - VMID: {c['vmid']}, Name: {c['name']}, Status: {c['status']}")

            print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_inventory()
