# Linux Insights for Schema.org

## System Information

| Command | Output | Schema.org |
|---------|--------|------------|
| `uname -a` | Linux kernel info | Place (CivicStructure) |
| `hostname` | Device name | Thing (name) |
| `ls /` | Root filesystem | Place (address) |
| `df -h` | Disk usage | StructuredValue (QuantitativeValue) |
| `free -h` | RAM usage | StructuredValue (QuantitativeValue) |

## Device as Schema.org

| Linux Device | Schema.org Type |
|--------------|---------------|
| Server | Place > CivicStructure |
| Container | VirtualLocation |
| Process | Action |
| User | Person |
| Service | Organization |
| Package | Product |
| File | CreativeWork |
| Network | Intangible > Property |

## Package Management

| Manager | Schema.org Package |
|---------|------------------|
| apt | Debian package |
| yum | RPM package |
| dnf | RPM package |
| pacman | Arch package |
| brew | Homebrew package |
| pip | Python package |
| npm | Node.js package |
| cargo | Rust crate |

## Package → Product Mapping

```python
@dataclass
class Package:
    name: str = ""          # Product.name
    version: str = ""       # Product.model
    architecture: str = ""  # Product.width
    source: str = ""        # Product.manufacturer
    license: str = ""      # CreativeWork.license
```

## Process → Action Mapping

| Process Type | Schema.org Action |
|--------------|-----------------|
| systemd | ActivateAction |
| cron | ScheduleAction |
| cron@ | PlanAction |
| service | Service |
| daemon | Service |

## User as Person

```python
@dataclass
class LinuxUser:
    id: int = 0           # Person.identifier
    name: str = ""        # Person.name
    home: str = ""       # Place.address (path)
    shell: str = ""       # Person.jobTitle
    groups: List[str] = [] # Organization.member
```

## Container as Place

| Container | Schema.org Place |
|-----------|-------------|
| Docker container | VirtualLocation |
| VM | Place |
| Namespace | Place |
| cgroup | Place |

## Network as Intangible

| Network | Schema.org Intangible |
|---------|-------------------|
| IP Address | StructuredValue > PropertyValue |
| Port | PropertyValue |
| Protocol | Intangible > Enumeration |

## File as CreativeWork

```python
@dataclass
class File:
    name: str = ""           # CreativeWork.name
    path: str = ""           # Place.address
    permissions: str = ""    # Intangible > DigitalDocumentPermission
    size: int = 0            # QuantitativeValue
    modified: datetime = None # CreativeWork.dateModified
    owner: str = ""          # Person.author
```

## Filesystem Hierarchy (as Place)

```
/
├── /bin       → Action (binary)
├── /boot      → Action (boot)
├── /dev       → Device
├── /etc       → Configuration
├── /home      → Place > Residence
├── /lib       → Intangible (library)
├── /media    → Place > CivicStructure
├── /mnt       → Place > Accommodation
├── /opt      → Place > TouristDestination
├── /proc     → Place > CivicStructure (virtual)
├── /root     → Place > Residence
├── /run      → Place > CivicStructure
├── /sbin     → Action (system binary)
├── /srv      → Place > Service (data service)
├── /tmp     → Place > Temporary
├── /usr      → Place > User
└── /var     → Place > Variable
```

## Implementation

```python
# Map Linux resources to Schema.org
device = Place(name="server-1", address="/", geo=GeoCoordinates(...))
file = CreativeWork(name="readme.txt", ...)
package = Product(name="python", brand="Python", ...)
user = Person(name="root", jobTitle="Administrator")
service = Service(name="docker", provider=org)
```

Reference: https://schema.org/docs/full.html