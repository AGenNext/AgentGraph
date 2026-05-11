"""
Linux Kernel Primitives Mapping

Maps all Agent Platform concepts to Linux Kernel primitives:
- Agent = Process
- Task = Thread/Task
- Memory = VM
- Organization = Cgroup/Namespace
- Skills = Syscalls
- Events = Kernel Events
- etc.

Reference:
- Linux Kernel: https://www.kernel.org/doc/html/latest/
- Proc FS: https://www.kernel.org/doc/Documentation/filesystems/proc.txt
- Cgroups: https://www.kernel.org/doc/Documentation/admin-guide/cgroup-v2.rst
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# =============================================================================
# AGENT PLATFORM → LINUX KERNEL MAPPING
# =============================================================================

"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  AGENT PLATFORM            →         LINUX KERNEL                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  SoftwareApplication (Agent)  →     Process (task_struct)                │
│  Action (Task)              →     Thread (kthread)                        │
│  Memory                     →     Virtual Memory (vm_area_struct)        │
│  Organization               →     Cgroup / Namespace                      │
│  Person (User)              →     User (struct cred)                     │
│  Skills (Capabilities)      →     Syscalls                               │
│  Events                     →     Kernel Events (tracepoints)            │
│  Credentials                →     Keys / Certificates (keyctl)             │
│  Location                   →     Net Device / Mount                     │
│  Subscription               →     Resource Limit (ulimit)                 │
│  Cost Tracking              →     CPU/Memory Accounting (cgroup stats)     │
│  Knowledge Graph            →     Page Cache / Radix Tree                  │
│  Queue                      →     Workqueue                               │
│  Schedule                   →     Scheduler (CFS)                         │
│  Communication              →     IPC / Net / Signals                      │
└─────────────────────────────────────────────────────────────────────────────┘
"""


# =============================================================================
# ENUMERATIONS - Kernel Primitives
# =============================================================================

class KernelPrimitive(Enum):
    """Linux kernel primitive types"""
    # Process
    PROCESS = "task_struct"
    THREAD = "thread_info"
    PROCESS_GROUP = "process_group"
    
    # Memory
    VIRTUAL_MEMORY = "vm_area_struct"
    PAGE = "page"
    MEMORY_CGROUP = "memory cgroup"
    
    # Scheduling
    SCHEDULER = "scheduler"
    SCHED_CLASS = "sched_class"
    PRIORITY = "priority"
    
    # Namespaces
    NAMESPACE = "namespace"
    PID_NAMESPACE = "pid_namespace"
    USER_NAMESPACE = "user_namespace"
    NET_NAMESPACE = "net_namespace"
    MOUNT_NAMESPACE = "mount_namespace"
    
    # Cgroups
    CGROUP = "cgroup"
    CGROUP_V2 = "cgroup v2"
    RESOURCE_CONTROLLER = "resource controller"
    
    # IPC
    SHARED_MEMORY = "shared memory"
    SEMAPHORE = "semaphore"
    MESSAGE_QUEUE = "message queue"
    SOCKET = "socket"
    
    # Files
    FILE_DESCRIPTOR = "file descriptor"
    INODE = "inode"
    DENTRY = "dentry"
    
    # Security
    CREDENTIALS = "cred"
    CAPABILITIES = "capabilities"
    SELINUX = "SELinux"
    APPARMOR = "AppArmor"
    
    # Syscalls
    SYSCALL = "syscall"
    SYSTEM_CALL = "system_call"
    
    # Events
    KERNEL_EVENT = "kernel_event"
    TRACEPOINT = "tracepoint"
    INTERRUPT = "interrupt"
    
    # Network
    NETWORK_DEVICE = "net_device"
    NETWORK_NAMESPACE = "net_namespace"
    ROUTE = "route"
    FIREWALL = "firewall"


# =============================================================================
# AGENT = PROCESS
# =============================================================================

@dataclass
class AgentProcess:
    """
    Agent mapped to Linux Process
    
    Agent → Process
    - name → comm (command name)
    - pid → pid
    - status → state
    - memory → vm
    - skills → capabilities
    """
    # Process identity (Schema.org: SoftwareApplication)
    agent_id: str
    name: str
    description: Optional[str] = None
    
    # Kernel mapping
    pid: Optional[int] = None  # Process ID
    ppid: Optional[int] = None  # Parent PID
    uid: Optional[int] = None  # User ID
    gid: Optional[int] = None  # Group ID
    
    # State
    state: str = "RUNNING"  # R/S/D/Z/T/W
    priority: int = 0  # Nice value
    num_threads: int = 1
    
    # Resources
    cpu_percent: float = 0.0
    memory_mb: int = 0
    uptime_seconds: int = 0
    
    # Skills mapped to capabilities
    capabilities: List[str] = field(default_factory=list)  # CAP_SYS_ADMIN, etc.
    syscalls: List[str] = field(default_factory=list)  # read, write, execve, etc.
    
    # Cgroup
    cgroup_path: Optional[str] = None
    cgroup_id: Optional[int] = None
    
    # Namespace
    pid_ns: Optional[int] = None
    user_ns: Optional[int] = None
    net_ns: Optional[int] = None
    
    # Security context
    selinux_context: Optional[str] = None
    apparmor_profile: Optional[str] = None
    
    def to_proc(self) -> Dict[str, Any]:
        """Export as /proc/[pid]/status format"""
        return {
            "Name": self.name,
            "Pid": self.pid,
            "PPid": self.ppid,
            "Uid": self.uid,
            "Gid": self.gid,
            "State": self.state,
            "Threads": self.num_threads,
            "Cpus_allowed": "ffff",
            "voluntary_ctxt_switches": 0,
            "nonvoluntary_ctxt_switches": 0
        }


# =============================================================================
# TASK = THREAD
# =============================================================================

@dataclass
class AgentTask:
    """
    Task mapped to Linux Thread
    
    Action (Task) → Thread
    - task_id → tid
    - status → task_state
    - priority → sched_priority
    - result → exit_code
    """
    # Task identity (Schema.org: Action)
    task_id: str
    action_type: str  # SearchAction, CreateAction, etc.
    name: str
    
    # Thread identity
    tid: Optional[int] = None  # Thread ID
    pid: Optional[int] = None  # Process ID (leader)
    
    # State
    state: str = "RUNNING"  # R/S/D/Z/T/t/w/x/k/p
    exit_state: int = 0
    
    # Scheduling
    priority: int = 0  # static_prio
    nice_value: int = 0
    sched_policy: str = "SCHED_NORMAL"  # SCHED_*
    vruntime: int = 0  # CFS virtual runtime
    
    # Timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: int = 0
    
    # Resources
    cpu: int = 0  # CPU core
    cpu_time_ms: int = 0
    memory_kb: int = 0
    
    # Execution
    result: Optional[Any] = None
    error: Optional[str] = None
    exit_code: int = 0
    
    # Stack
    stack_base: Optional[int] = None
    stack_size: int = 0
    
    # Syscall tracking
    last_syscall: Optional[str] = None
    syscall_count: int = 0
    
    def to_sched(self) -> Dict[str, Any]:
        """Export as /proc/[tid]/sched format"""
        return {
            "task": self.name,
            "pid": self.tid,
            "nr_switches": 0,
            "nr_voluntary_switches": 0,
            "nr_involuntary_switches": 0,
            "se.exec_start": self.start_time.isoformat() if self.start_time else 0,
            "se.vruntime": self.vruntime,
            "se.sum_exec_runtime": self.cpu_time_ms,
            "nr_migrations": 0,
            "nr_pagefaults": 0
        }


# =============================================================================
# ORGANIZATION = CGROUP/NAMESPACE
# =============================================================================

@dataclass
class OrganizationCgroup:
    """
    Organization mapped to Cgroup/Namespace
    
    Organization → Cgroup + Namespace
    - org_id → cgroup path
    - departments → sub-cgroups
    - members → tasks in cgroup
    - limits → resource limits
    """
    # Organization identity (Schema.org: Organization)
    org_id: str
    name: str
    description: Optional[str] = None
    
    # Cgroup
    cgroup_path: str  # /sys/fs/cgroup/...
    cgroup_id: Optional[int] = None
    
    # Resource limits
    cpu_shares: int = 1024  # weight
    cpu_quota_us: int = -1  # period
    memory_limit_mb: int = -1
    memory_swap_limit_mb: int = -1
    io_weight: int = 100
    io_latency_ns: int = 0
    
    # PIDs
    max_pids: int = -1  # unlimited
    
    # Tasks
    task_count: int = 0
    
    # Namespace (optional)
    namespace_id: Optional[int] = None
    
    # Sub-groups
    sub_cgroups: List[str] = field(default_factory=list)
    
    # Hierarchy
    parent_cgroup: Optional[str] = None
    level: int = 0
    
    def to_cgroup(self) -> Dict[str, Any]:
        """Export cgroup settings"""
        return {
            "path": self.cgroup_path,
            "cpu.weight": self.cpu_shares,
            "cpu.max": f"{self.cpu_quota_us}/100000" if self.cpu_quota_us > 0 else "max",
            "memory.max": f"{self.memory_limit_mb}M" if self.memory_limit_mb > 0 else "max",
            "io.weight": self.io_weight,
            "pids.max": str(self.max_pids) if self.max_pids > 0 else "max"
        }


# =============================================================================
# PERSON = USER
# =============================================================================

@dataclass
class PersonUser:
    """
    Person mapped to Linux User
    
    Person → User + Credentials
    - person_id → uid
    - role → gid (group)
    - account_status → password status
    """
    # Person identity (Schema.org: Person)
    person_id: str
    name: str
    email: Optional[str] = None
    
    # User mapping
    uid: Optional[int] = None  # User ID
    gid: Optional[int] = None  # Primary Group ID
    gids: List[int] = field(default_factory=list)  # Supplementary groups
    
    # Home
    home_directory: Optional[str] = None
    shell: Optional[str] = None
    
    # Account
    username: Optional[str] = None
    password_hash: Optional[str] = None
    account_status: str = "active"  # active/locked/expired
    
    # Role (mapped to groups)
    role: Optional[str] = None
    department: Optional[str] = None
    
    # Capabilities (Skills mapped to capabilities)
    permitted_capabilities: List[str] = field(default_factory=list)  # CAP_*
    effective_capabilities: List[str] = field(default_factory=list)
    
    # Security context
    selinux_user: Optional[str] = None
    apparmor_profile: Optional[str] = None
    
    # Limits
    max_processes: int = 0
    max_files: int = 0
    
    def to_passwd(self) -> Dict[str, Any]:
        """Export as /etc/passwd format"""
        return {
            "username": self.username or self.name.lower(),
            "uid": self.uid,
            "gid": self.gid,
            "info": self.name,
            "home": self.home_directory or f"/home/{self.name.lower()}",
            "shell": self.shell or "/bin/bash"
        }
    
    def to_capabilities(self) -> Dict[str, Any]:
        """Export capabilities"""
        return {
            "permitted": self.permitted_capabilities,
            "effective": self.effective_capabilities
        }


# =============================================================================
# SKILLS = SYSCALLS
# =============================================================================

@dataclass
class SkillSyscall:
    """
    Skills mapped to Linux Syscalls
    
    Skill → Syscall
    - skill_name → syscall name
    - description → syscall description
    """
    # Skill identity
    skill_id: str
    skill_name: str
    description: Optional[str] = None
    
    # Syscall mapping
    syscall_number: Optional[int] = None
    syscall_name: Optional[str] = None
    
    # Categories
    category: str = "system"  # system, process, memory, file, network, ipc
    
    # Properties
    requires_capability: Optional[str] = None  # CAP_*
    is_privileged: bool = False
    
    # Resource impact
    blocking: bool = False
    idempotent: bool = True
    
    # Mapping to skill categories
    skill_to_syscall = {
        # Data operations
        "data_read": "read",
        "data_write": "write",
        "data_query": "select",  # pseudo
        "data_analysis": "process_vm_readv",  # pseudo
        
        # File operations
        "file_read": "read",
        "file_write": "write",
        "file_delete": "unlink",
        
        # Code execution
        "code_execute": "execve",
        "shell_command": "execve",
        
        # Network
        "web_search": "socket",  # pseudo
        "http_request": "connect",
        "api_call": "sendto/recvfrom",
        
        # Communication
        "send_email": "sendmail",  # pseudo
        "send_message": "sendmsg",
        
        # Process
        "create_process": "fork",
        "terminate_process": "kill",
        "wait": "wait4",
        
        # Memory
        "allocate_memory": "mmap",
        "free_memory": "munmap",
        
        # Security
        "change_owner": "chown",
        "set_permission": "chmod",
        "get_credential": "getuid"
    }
    
    def get_syscall(self) -> str:
        """Get mapped syscall"""
        return self.skill_to_syscall.get(self.skill_name, "unknown")
    
    def requires_root(self) -> bool:
        """Check if requires root"""
        privileged_syscalls = [
            "mount", "umount", "reboot", "init_module",
            "delete_module", "quotactl", "settimeofday"
        ]
        return self.syscall_name in privileged_syscalls


# =============================================================================
# MEMORY = VIRTUAL MEMORY
# =============================================================================

@dataclass
class AgentMemory:
    """
    Memory mapped to Virtual Memory Areas
    
    Memory → vm_area_struct
    - memory_id → vma
    - content → file/pages
    - access_count → page_faults
    """
    # Memory identity
    memory_id: str
    agent_id: str
    
    # VM mapping
    vma_start: Optional[int] = None
    vma_end: Optional[int] = None
    vma_flags: str = "rw-"  # r/w/x/p/s/h
    
    # Type
    memory_type: str = "anonymous"  # anonymous, file, shared
    backing_file: Optional[str] = None
    
    # Usage
    size_kb: int = 0
    resident_pages: int = 0
    swapped_pages: int = 0
    
    # Access
    access_count: int = 0
    last_access: Optional[datetime] = None
    
    # Protection
    read: bool = True
    write: bool = True
    execute: bool = False
    shared: bool = False
    
    # Performance
    page_faults: int = 0
    cache_hits: int = 0
    
    def to_maps(self) -> Dict[str, Any]:
        """Export as /proc/[pid]/maps format"""
        return {
            "start": hex(self.vma_start) if self.vma_start else "0",
            "end": hex(self.vma_end) if self.vma_end else "0",
            "perms": self.vma_flags,
            "offset": "0",
            "dev": "00:00",
            "inode": "0",
            "pathname": self.backing_file or ""
        }


# =============================================================================
# EVENTS = KERNEL EVENTS
# =============================================================================

@dataclass
class AgentEvent:
    """
    Events mapped to Kernel Events
    
    Event → tracepoint/kprobe/irq
    - event_id → event ID
    - type → tracepoint category
    - timestamp → ktime
    """
    # Event identity (Schema.org: Event)
    event_id: str
    event_type: str
    
    # Kernel event mapping
    tracepoint: Optional[str] = None  # syscalls:sys_enter_*
    interrupt: Optional[int] = None  # IRQ number
    exception: Optional[str] = None  # #DE, #PF, etc.
    
    # Timing
    timestamp_ns: int = 0  # ktime_get_ns()
    cpu: int = 0
    
    # Data
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Source
    process_id: Optional[int] = None
    thread_id: Optional[int] = None
    
    # Categories
    event_category: str = "system"  # syscall, irq, exception, timer, net
    
    # Event types
    EVENT_TYPES = {
        "TaskCreated": "sched:sched_process_fork",
        "TaskStarted": "sched:sched_process_exec",
        "TaskCompleted": "sched:sched_process_exit",
        "TaskFailed": "exceptions:general_protection_fault",
        "AgentRegistered": "syscalls:sys_enter_prctl",
        "SystemStartup": "init:init_post"
    }
    
    def get_tracepoint(self) -> str:
        """Get mapped tracepoint"""
        return self.EVENT_TYPES.get(self.event_type, "unknown:tracepoint")


# =============================================================================
# CREDENTIALS = KEYS
# =============================================================================

@dataclass
class CredentialKey:
    """
    Credentials mapped to Linux Keys
    
    Credential → key (keyctl)
    - credential_id → serial
    - key_type → type (keyring, user, asymmetric)
    """
    # Credential identity (Schema.org: PropertyValue)
    credential_id: str
    credential_type: str  # api_key, oauth, jwt, certificate
    
    # Key mapping
    key_serial: Optional[int] = None
    key_type: str = "user"  # user, keyring, asymmetric
    key_description: Optional[str] = None
    
    # Permissions
    uid: Optional[int] = None  # Owner
    gid: Optional[int] = None  # Group
    permissions: str = "--w--w----"  # owner/group/other
    
    # Expiry
    expiry: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    
    # Status
    revoked: bool = False
    
    # Key types
    KEY_TYPES = {
        "api_key": "user",
        "oauth": "user",
        "jwt": "user",
        "certificate": "asymmetric",
        "ssh_key": "asymmetric"
    }
    
    def get_key_type(self) -> str:
        """Get mapped key type"""
        return self.KEY_TYPES.get(self.credential_type, "user")


# =============================================================================
# QUEUE = WORKQUEUE
# =============================================================================

@dataclass
class TaskQueue:
    """
    Task queue mapped to Workqueue
    
    Task Queue → workqueue
    - queue_id → workqueue_struct
    - pending_tasks → pending works
    """
    # Queue identity
    queue_id: str
    queue_name: str
    
    # Workqueue mapping
    wq_name: Optional[str] = None
    
    # State
    pending_count: int = 0
    running_count: int = 0
    
    # Configuration
    max_workers: int = 0
    current_workers: int = 0
    
    # Type
    unbound: bool = False  # unbound vs bound
    ordered: bool = False
    
    # CPU affinity
    cpu: Optional[int] = None  # None = any CPU
    
    # Performance
    total_dispatched: int = 0
    total_completed: int = 0
    
    def to_workqueue(self) -> Dict[str, Any]:
        """Export workqueue info"""
        return {
            "name": self.wq_name or self.queue_name,
            "pending": self.pending_count,
            "active": self.running_count,
            "max_active": self.max_workers,
            "unbound": self.unbound,
            "cpu": self.cpu if self.cpu is not None else "any"
        }


# =============================================================================
# KNOWLEDGE GRAPH = PAGE CACHE
# =============================================================================

@dataclass
class KnowledgePageCache:
    """
    Knowledge graph mapped to Page Cache
    
    Knowledge → Page Cache + Radix Tree
    - knowledge_id → page
    - content → page content
    - search → radix_tree_lookup
    """
    # Knowledge identity
    knowledge_id: str
    content: str
    
    # Page mapping
    page_frame_number: Optional[int] = None
    cache_index: Optional[int] = None
    
    # State
    dirty: bool = False
    referenced: bool = True
    uptodate: bool = True
    
    # Access
    access_count: int = 0
    last_access: Optional[datetime] = None
    last_modify: Optional[datetime] = None
    
    # Mapping
    radix_tree_index: Optional[int] = None
    
    # Size
    size_bytes: int = 0
    
    # Mapping to addresses
    virtual_address: Optional[int] = None
    
    def to_slab(self) -> Dict[str, Any]:
        """Export slab info"""
        return {
            "object_size": self.size_bytes,
            "objects_per_slab": 1,
            "slabs": 1,
            "total_objects": 1,
            "active_objects": self.access_count
        }


# =============================================================================
# LINUX KERNEL AGENT PLATFORM
# =============================================================================

class KernelAgentPlatform:
    """
    Complete Agent Platform mapped to Linux Kernel
    
    This class demonstrates the mapping between:
    - Agent Platform concepts
    - Linux Kernel primitives
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentProcess] = {}
        self.tasks: Dict[str, AgentTask] = {}
        self.organizations: Dict[str, OrganizationCgroup] = {}
        self.persons: Dict[str, PersonUser] = {}
        self.memories: Dict[str, AgentMemory] = {}
        self.events: Dict[str, AgentEvent] = {}
        self.credentials: Dict[str, CredentialKey] = {}
        self.queues: Dict[str, TaskQueue] = {}
    
    # =================================================================
    # Create mappings
    # =================================================================
    
    def create_agent_process(self, agent_id: str, name: str) -> AgentProcess:
        """Create agent as process"""
        agent = AgentProcess(
            agent_id=agent_id,
            name=name,
            state="RUNNING"
        )
        self.agents[agent_id] = agent
        return agent
    
    def create_task_thread(self, task_id: str, agent_id: str) -> AgentTask:
        """Create task as thread"""
        task = AgentTask(
            task_id=task_id,
            action_type="Action",
            name=f"task-{task_id}",
            pid=self.agents.get(agent_id).pid if agent_id in self.agents else None
        )
        self.tasks[task_id] = task
        return task
    
    def create_org_cgroup(self, org_id: str, name: str) -> OrganizationCgroup:
        """Create organization as cgroup"""
        cgroup = OrganizationCgroup(
            org_id=org_id,
            name=name,
            cgroup_path=f"/sys/fs/cgroup/{name}"
        )
        self.organizations[org_id] = cgroup
        return cgroup
    
    def create_person_user(self, person_id: str, name: str) -> PersonUser:
        """Create person as user"""
        user = PersonUser(
            person_id=person_id,
            name=name,
            username=name.lower()
        )
        self.persons[person_id] = user
        return user
    
    # =================================================================
    # Export
    # =================================================================
    
    def to_proc(self) -> Dict[str, Any]:
        """Export as proc filesystem"""
        return {
            "agents": {aid: a.to_proc() for aid, a in self.agents.items()},
            "tasks": {tid: t.to_sched() for tid, t in self.tasks.items()},
            "cgroups": {oid: o.to_cgroup() for oid, o in self.organizations.items()},
            "users": {pid: p.to_passwd() for pid, p in self.persons.items()}
        }


# =============================================================================
# USAGE
# =============================================================================

def main():
    """Example usage"""
    
    print("=" * 60)
    print("Agent Platform → Linux Kernel Primitives Mapping")
    print("=" * 60)
    
    # Create platform
    platform = KernelAgentPlatform()
    
    # Create agent as process
    print("\n1. Agent = Process")
    agent = platform.create_agent_process("agent-001", "ai-assistant")
    print(f"   Name: {agent.name}")
    print(f"   PID: {agent.pid}")
    print(f"   Capabilities: {agent.capabilities}")
    
    # Create organization as cgroup
    print("\n2. Organization = Cgroup")
    org = platform.create_org_cgroup("org-acme", "acme-corp")
    print(f"   Name: {org.name}")
    print(f"   Cgroup Path: {org.cgroup_path}")
    print(f"   CPU Shares: {org.cpu_shares}")
    
    # Create person as user
    print("\n3. Person = User")
    person = platform.create_person_user("person-john", "John Doe")
    print(f"   Name: {person.name}")
    print(f"   UID: {person.uid}")
    print(f"   Capabilities: {person.permitted_capabilities}")
    
    # Create task as thread
    print("\n4. Task = Thread")
    task = platform.create_task_thread("task-001", "agent-001")
    print(f"   Task ID: {task.task_id}")
    print(f"   TID: {task.tid}")
    print(f"   Priority: {task.priority}")
    
    # Export as proc
    print("\n5. Export as /proc format")
    proc_data = platform.to_proc()
    print(f"   Agents: {len(proc_data['agents'])}")
    print(f"   Tasks: {len(proc_data['tasks'])}")
    print(f"   Cgroups: {len(proc_data['cgroups'])}")


if __name__ == "__main__":
    main()


"""
Linux Kernel Primitives Mapping

Complete mapping table:

┌─────────────────────────┬──────────────────────────────────────────┐
│ Agent Platform          │ Linux Kernel Primitive                   │
├─────────────────────────┼──────────────────────────────────────────┤
│ SoftwareApplication    │ task_struct (Process)                  │
│ Action                 │ kthread (Thread)                        │
│ Organization           │ cgroup + namespace                     │
│ Person                 │ cred + user_struct                      │
│ Skills                 │ syscalls + capabilities                │
│ Memory                 │ vm_area_struct + page                  │
│ Event                  │ tracepoint + kprobe                    │
│ Credential             │ key_struct + keyctl                    │
│ Subscription           │ ulimit + cgroup limits                │
│ Cost Tracking          │ cpuacct + memcg stats                  │
│ Knowledge Graph        │ radix_tree + page_cache               │
│ Task Queue             │ workqueue + kworker                   │
│ Schedule               │ CFS scheduler                          │
│ Location               │ net_device + mount                     │
│ Communication          │ socket + ipc                          │
│ Authentication         │ pam + selinux                         │
│ Industry               │ cgroup controllers                    │
│ Job Role               │ sched_class (RT/Batch/Idle)          │
└─────────────────────────┴──────────────────────────────────────────┘

References:
- https://www.kernel.org/doc/html/latest/
- https://www.kernel.org/doc/Documentation/filesystems/proc.txt
- https://www.kernel.org/doc/admin-guide/cgroup-v2.rst
"""