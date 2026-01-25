# Security

## Security Scanning

This project uses automated security scanning tools:

- **gosec**: Static analysis for Go security issues
- **govulncheck**: Vulnerability scanning for Go dependencies and standard library

Run security scans with:
```bash
make security
```

## Known Issues

### Standard Library Vulnerabilities

The `govulncheck` tool may report vulnerabilities in the Go standard library. These are **not vulnerabilities in this codebase** but rather in the Go runtime version being used.

Most reported vulnerabilities are:
- In `crypto/x509`, `crypto/tls`, and related packages
- Triggered by indirect calls through `signal.Notify` (used for graceful shutdown)
- Fixed in Go 1.24.11 or later

### Resolution

To resolve standard library vulnerabilities:
1. Update to Go 1.24.11 or later (see `go.mod`)
2. Run `go mod tidy` to update dependencies
3. Re-run `make security` to verify

## Security Best Practices

This project follows security best practices:

- ✅ Input validation (digits, file paths)
- ✅ Path sanitization to prevent directory traversal
- ✅ Bounds checking for array/string operations
- ✅ Error handling with proper error wrapping
- ✅ No hardcoded secrets or credentials
- ✅ Secure file permissions (0644 for files, 0755 for directories)

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:
1. Do not open a public issue
2. Contact the maintainer directly
3. Provide detailed information about the vulnerability
