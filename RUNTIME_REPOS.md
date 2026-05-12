# Programming Runtime Repositories

## Top Runtime Repositories by Language (GitHub Topics)

Reference: https://github.com/topics/runtime

| # | Language | Repositories | Schema.org Type |
|---|---------|-----------|---------------|
| 1 | TypeScript | 218 | SoftwareApplication |
| 2 | Rust | 178 | SoftwareApplication |
| 3 | C++ | 161 | SoftwareApplication |
| 4 | JavaScript | 148 | SoftwareApplication |
| 5 | C# | 139 | SoftwareApplication |
| 6 | Go | 118 | SoftwareApplication |
| 7 | Python | 113 | SoftwareApplication |
| 8 | C | 107 | SoftwareApplication |
| 9 | Java | 104 | SoftwareApplication |
| 10 | Objective-C | 78 | SoftwareApplication |

**Total: 1,755 repositories**

## Popular Runtime Libraries

### JavaScript/TypeScript
- Node.js runtime
- Bun runtime
- Deno runtime
- QuickJS
- Hermes (Meta)

### Rust
- Tokio async runtime
- wasmtime (WebAssembly)
- wasmer (WebAssembly)

### Go
- golang runtime
- gVisor (container runtime)

### Python
- PyPy
- CPython
- MicroPython

### Java/JVM
- HotSpot (OpenJDK)
- GraalVM
- OpenJ9

### .NET/C#
- .NET runtime
- Mono
- CoreCLR

### C/C++
- glibc
- musl
- LLVM runtime

### WebAssembly Runtimes
- wasmtime
- wasmer
- WAVM
- Ethonnet WASM

## Runtime Types

| Runtime | Language | Type | Use Case |
|---------|--------|------|---------|
| **Node.js** | JavaScript | RuntimePlatform | Server JS |
| **Bun** | JavaScript | RuntimePlatform | All-in-one |
| **Deno** | JavaScript | RuntimePlatform | Secure JS |
| **Hermes** | JavaScript | RuntimePlatform | React Native |
| **PyPy** | Python | RuntimePlatform | Fast Python |
| **GraalVM** | Multi | RuntimePlatform | Polyglot |
| **wasmtime** | WASM | RuntimePlatform | WebAssembly |
| **wasmer** | WASM | RuntimePlatform | WebAssembly |

## Schema.org Mapping

```python
@dataclass
class Runtime:
    name: str = ""           # SoftwareApplication.name
    version: str = ""         # SoftwareApplication.version
    language: str = ""        # ProgrammingLanguage
    
    # Runtime-specific
    type: str = ""           # Interpreted, Compiled, VM
    garbage_collected: bool = False
    async_support: bool = False
    
    # Schema.org
    additional_type: str = "RuntimePlatform"
    application_category: str = ""  # DeveloperApplication
```

## Implementation

```python
runtime_categories = {
    "javascript_runtime": [
        {"name": "Node.js", "stars": 99000, "language": "JavaScript"},
        {"name": "Bun", "stars": 95000, "language": "JavaScript"},
        {"name": "Deno", "stars": 93000, "language": "TypeScript"},
    ],
    "python_runtime": [
        {"name": "CPython", "stars": 5000, "language": "Python"},
        {"name": "PyPy", "stars": 0, "language": "Python"},
    ],
    "wasm_runtime": [
        {"name": "wasmtime", "stars": 20000, "language": "Rust"},
        {"name": "wasmer", "stars": 18000, "language": "Rust"},
    ],
    "jvm_runtime": [
        {"name": "OpenJDK", "stars": 2000, "language": "Java"},
        {"name": "GraalVM", "stars": 19000, "language": "Java"},
    ],
}

def get_runtime_features(runtime_name: str) -> dict:
    features = {
        "Node.js": {"async": True, "GC": True, "WASM": True},
        "Bun": {"async": True, "GC": True, "WASM": False},
        "Deno": {"async": True, "GC": True, "WASM": True},
        "wasmtime": {"async": False, "GC": False, "WASM": True},
    }
    return features.get(runtime_name, {})
```

Reference: https://github.com/topics/runtime