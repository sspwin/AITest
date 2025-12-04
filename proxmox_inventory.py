from proxmoxer import ProxmoxAPI

# Proxmox server details (replace with your actual details)
proxmox_host = "proxmox_host"
proxmox_user = "user@pam"
proxmox_password = "password"

def get_proxmox_inventory():
    """
    Connects to the Proxmox cluster and fetches the complete inventory.
    """
    try:
        # Establish connection to Proxmox API
        proxmox = ProxmoxAPI(
            proxmox_host,
            user=proxmox_user,
            password=proxmox_password,
            verify_ssl=False  # Set to True if you have a valid SSL certificate
        )

        print("Successfully connected to Proxmox cluster.")
        print("-" * 50)

        # Get all nodes in the cluster
        nodes = proxmox.nodes.get()
        print(f"Found {len(nodes)} nodes in the cluster.")
        print("-" * 50)

        # Iterate through each node
        for node in nodes:
            node_name = node["node"]
            print(f"Node: {node_name}")
            print("-" * 30)

            # Get all QEMU (KVM) virtual machines on the node
            qemu_vms = proxmox.nodes(node_name).qemu.get()
            print(f"  QEMU VMs ({len(qemu_vms)}):")
            if qemu_vms:
                for vm in qemu_vms:
                    print(f"    - VMID: {vm['vmid']}, Name: {vm['name']}, Status: {vm['status']}")
            else:
                print("    - No QEMU VMs found.")

            print("-" * 30)

            # Get all LXC containers on the node
            lxc_containers = proxmox.nodes(node_name).lxc.get()
            print(f"  LXC Containers ({len(lxc_containers)}):")
            if lxc_containers:
                for container in lxc_containers:
                    print(f"    - VMID: {container['vmid']}, Name: {container['name']}, Status: {container['status']}")
            else:
                print("    - No LXC containers found.")

            print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_proxmox_inventory()
