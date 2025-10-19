# Home Lab Infrastructure Requirements (v0.6 Draft)

These requirements capture the streamlined home-lab deployment plan that prioritizes simplicity while preserving the role separation and automation discipline discussed in the feasibility review.

## 5.F.1 Infrastructure & Access

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-001 | Docker baseline | Each Linux node MUST run Docker Engine with Docker Compose; the designated system-manager node also runs the Docker Swarm manager when clustering is required. | Must | Ensures a consistent runtime without introducing Kubernetes complexity. |
| HLI-002 | Addressability | FritzBox DHCP reservations (or static IPs) MUST exist for every managed node so inventories stay stable. | Must | Simplifies Ansible inventory management and service routing. |
| HLI-003 | Remote access | Linux nodes MUST expose SSH with key-based authentication; Windows hosts MUST document WinRM or manual procedures. | Must | Keeps remote administration predictable without password-based access. |

## 5.F.2 Automation & Configuration Management

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-010 | Idempotent playbooks | Ansible playbooks MUST provision OS baselines, Docker, secrets, and service stacks per role idempotently. | Must | Avoids configuration drift while keeping tooling lightweight. |
| HLI-011 | Manual or light CI runs | Configuration changes SHOULD be executed via manual `ansible-playbook` runs or a simple CI trigger—GitOps controllers are NOT required. | Should | Balances automation with operational simplicity. |
| HLI-012 | Inventory source of truth | The system-manager host MUST maintain the canonical inventory including node roles, IPs, and hardware capabilities. | Must | Enables deterministic placement for Swarm/Compose deployments. |

## 5.F.3 Role Assignments & Workload Placement

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-020 | Always-on responsibilities | The Raspberry Pi and always-on mini-PC MUST host remote orchestration endpoints, the hot cache, downloader queue, and light automation jobs. | Must | Keeps critical coordination services available 24/7. |
| HLI-021 | Storage guardianship | Bulk storage, backup, and repository services MUST reside on the NAS/file server, with repository data backed up independently of general shares. | Must | Prevents storage contention and preserves recoverability. |
| HLI-022 | AI workload placement | GPU-heavy AI inference MUST execute on the desktop-class machine (Windows or Linux). CPU-only inference MAY run on the mini-PC when resources allow. | Must | Ensures workloads land on compatible hardware while permitting lightweight fallbacks. |

## 5.F.4 Networking & Service Discovery

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-030 | Built-in discovery | Docker network aliases and FritzBox DNS MUST cover inter-service name resolution; no external service discovery layer is introduced. | Must | Leverages existing tooling to avoid operational overhead. |
| HLI-031 | Practical segmentation | The FritzBox perimeter firewall and per-host firewalls SHOULD enforce access to sensitive services (storage, backup). VLANs MAY be added later without redesign. | Should | Keeps security manageable in a home-lab LAN. |

## 5.F.5 Data & Storage Practices

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-040 | Hot cache policy | The hot cache MUST use a single-tier design with documented TTL/invalidation strategy and persistence or warm-up scripts as needed. | Must | Avoids multi-tier complexity while ensuring predictable behavior. |
| HLI-041 | Backup cadence | Backup workflows (e.g., Restic/Borg) MUST run on schedule from the backup node to bulk storage and SHOULD produce periodic off-device copies. | Must/Should | Off-device copies can be USB or cloud sync. |
| HLI-042 | Data sync documentation | Synchronization between cache, repositories, and automation artifacts MUST be documented so operators know frequency and conflict resolution steps. | Must | Prevents stale or inconsistent data during recovery. |

## 5.F.6 Monitoring & Logging

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-050 | Lightweight telemetry | A minimal monitoring stack (e.g., Netdata or Prometheus + node_exporter) SHOULD track CPU, memory, disk, and key service availability. | Should | Prioritizes actionable health checks over enterprise observability. |
| HLI-051 | Log retention | At minimum, Ansible run logs, Docker logs, and critical service logs MUST be retained with rotation policies; centralized aggregation is OPTIONAL. | Must | Supports troubleshooting without deploying heavy logging platforms. |

## 5.F.7 Operations & Maintenance

| ID | Title | Requirement | Priority | Notes |
| --- | --- | --- | --- | --- |
| HLI-060 | Regular updates | Weekly or monthly Ansible runs MUST apply OS/package updates, starting with non-critical nodes before core services. | Must | Reduces risk while keeping systems patched. |
| HLI-061 | Recovery playbooks | Disaster recovery documentation MUST outline restoration steps for the Swarm manager, storage services, and AI hosts. | Must | Ensures the operator can rebuild critical roles quickly. |
| HLI-062 | Wake-on-LAN readiness | Wake-on-LAN procedures SHOULD be documented for nodes that can power down, ensuring orchestrated startups when workloads require them. | Should | Keeps high-power hosts offline by default without sacrificing availability. |

