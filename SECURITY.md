# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please send an email to security@agenext.io instead of using the public GitHub issue tracker.

## Supported Versions

| Version | Supported |
| --- | --- |
| latest | ✅ |

## Security Checks Enabled

- ✅ Dependency Review Action
- ✅ CodeQL Static Analysis  
- ✅ Secret Scanning
- ✅ Docker Scan (Trivy)
- ✅ Dependency Vulnerability Alerts

## Security Best Practices

- All API keys use environment variables (never hardcoded)
- Docker runs as non-root user
- Minimal base image (python:3.11-slim)
- No secrets in logs