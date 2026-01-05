# Proxmox 3-Tier Architecture

This document outlines a typical Proxmox 3-tier architecture, consisting of hosts, networking, and storage. This architecture is designed for high availability, scalability, and performance.

## Architecture Diagram

```mermaid
graph TD
    subgraph "Tier 1: Virtualization (Guests)"
        VM1[VM 1]
        VM2[VM 2]
        CT1[Container 1]
    end

    subgraph "Tier 2: Host Layer (Proxmox Cluster)"
        PVE1[Proxmox VE Node 1]
        PVE2[Proxmox VE Node 2]
        PVE3[Proxmox VE Node 3]
    end

    subgraph "Tier 3: Networking Layer"
        subgraph "PVE1 Networking"
            Bond1[Bond0 (LACP)]
        end
        subgraph "PVE2 Networking"
            Bond2[Bond0 (LACP)]
        end
        subgraph "PVE3 Networking"
            Bond3[Bond0 (LACP)]
        end

        Switch1[Switch 1]
        Switch2[Switch 2]

        Bond1 -- VLANs --> Switch1
        Bond1 -- VLANs --> Switch2
        Bond2 -- VLANs --> Switch1
        Bond2 -- VLANs --> Switch2
        Bond3 -- VLANs --> Switch1
        Bond3 -- VLANs --> Switch2
    end

    subgraph "Tier 3: Storage Layer (Ceph Cluster)"
        subgraph "PVE1 Storage"
            OSD1[OSD]
            OSD2[OSD]
        end
        subgraph "PVE2 Storage"
            OSD3[OSD]
            OSD4[OSD]
        end
        subgraph "PVE3 Storage"
            OSD5[OSD]
            OSD6[OSD]
        end
        CephPool[Ceph Storage Pool]
        OSD1 --> CephPool
        OSD2 --> CephPool
        OSD3 --> CephPool
        OSD4 --> CephPool
        OSD5 --> CephPool
        OSD6 --> CephPool
    end

    VM1 --> PVE1
    VM2 --> PVE2
    CT1 --> PVE3

    PVE1 -- Access --> CephPool
    PVE2 -- Access --> CephPool
    PVE3 -- Access --> CephPool
```

## Explanation of Tiers

### Tier 1: Virtualization (Guests)

This tier consists of the virtual machines (VMs) and containers (CTs) that run on the Proxmox cluster. These are the workloads that your applications and services run on.

### Tier 2: Host Layer (Proxmox Cluster)

This tier is the core of the Proxmox environment. It consists of multiple Proxmox VE nodes that are clustered together. The cluster provides high availability, allowing VMs and containers to be automatically migrated to other nodes if a host fails.

### Tier 3: Networking and Storage

This tier provides the underlying infrastructure for the Proxmox cluster.

*   **Networking:** The networking layer is designed for redundancy and performance. Each Proxmox node has a bonded network interface (LACP) that is connected to two separate switches. This provides both link aggregation for increased bandwidth and failover if a switch or network card fails. VLANs are used to segment traffic for management, VM traffic, and storage.
*   **Storage:** The storage layer is provided by a distributed Ceph cluster. Ceph is a software-defined storage solution that runs on the Proxmox nodes themselves, using the local disks of each node. The OSDs (Object Storage Daemons) on each node work together to create a single, resilient storage pool. This provides high availability and scalability for your VM and container storage.
