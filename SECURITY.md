# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of py-netatmo-truetemp seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Disclose Publicly

Please do not open a public GitHub issue for security vulnerabilities. Public disclosure before a fix is available could put users at risk.

### 2. Report Privately

Report security vulnerabilities through one of these channels:

- **GitHub Security Advisories** (preferred): Use the [Security tab](https://github.com/P4uLT/py-netatmo-truetemp/security/advisories/new) to create a private security advisory
- **Email**: Send details to the maintainer via GitHub profile contact

### 3. Include Detailed Information

When reporting, please include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** and severity assessment
- **Affected versions** (if known)
- **Possible mitigations** or workarounds
- **Proof of concept** code (if applicable)
- **Your contact information** for follow-up questions

### 4. Response Timeline

- **Initial Response**: Within 48 hours acknowledging receipt
- **Status Update**: Within 7 days with assessment and next steps
- **Fix Timeline**: Depends on severity (critical issues prioritized)
- **Disclosure**: Coordinated disclosure after fix is released

## Security Practices

This project follows security best practices:

### Authentication & Credentials

- **Environment Variables**: Credentials stored in environment variables, not hardcoded
- **Cookie Security**: Session cookies stored with 0o600 permissions (owner-only read/write)
- **No Pickle**: JSON serialization instead of unsafe pickle for cookie storage
- **HTTPS Only**: All API communication over HTTPS

### Code Security

- **Bandit Scanning**: Automated security scanning in CI/CD pipeline
- **Dependency Management**: Regular dependency updates via Renovate
- **Type Safety**: Full type hints to prevent type-related vulnerabilities
- **Input Validation**: All user inputs validated before use
- **Error Handling**: Proper exception handling without exposing sensitive info

### File System Security

Cookie storage locations with secure permissions:
- **Linux**: `~/.cache/netatmo/py-netatmo-truetemp/cookies.json` (0o600)
- **macOS**: `~/Library/Caches/netatmo/py-netatmo-truetemp/cookies.json` (0o600)
- **Windows**: `%LOCALAPPDATA%\netatmo\py-netatmo-truetemp\Cache\cookies.json` (restricted ACLs)

### Supply Chain Security

- **Locked Dependencies**: `uv.lock` ensures reproducible builds
- **Minimal Dependencies**: Only essential packages (requests, platformdirs)
- **Version Pinning**: Exact versions in production
- **Automated Updates**: Renovate for dependency security patches

## Security Considerations for Users

### Best Practices

1. **Protect Credentials**: Never commit `.env` files or hardcode credentials
2. **Secure Cookie Files**: Default locations are protected, but custom paths should use appropriate permissions
3. **Keep Updated**: Always use the latest version for security fixes
4. **Review Logs**: Monitor logs for unusual authentication patterns
5. **Network Security**: Use trusted networks when authenticating

### What We Store

The library stores minimal data:
- **Session Cookies**: Cached in JSON format for authentication
- **No Passwords**: Passwords never stored, only used during authentication
- **No API Keys**: No long-term API credentials stored

### What We Don't Store

- Passwords (used only for initial authentication)
- Personal identification information
- Home layout details
- Historical temperature data

## Known Security Considerations

### Undocumented API Usage

This library uses Netatmo's undocumented TrueTemperature API endpoint:
- **Rate Limiting**: No official rate limits published; use responsibly
- **API Changes**: Undocumented endpoints may change without notice
- **Terms of Service**: Ensure compliance with Netatmo's ToS

### Authentication Method

Cookie-based authentication is used:
- **Session Duration**: Cookies expire based on Netatmo's policy
- **Auto-Retry**: Automatic re-authentication on 403 errors
- **Thread Safety**: Session management is thread-safe with locking

## Security Updates

Security fixes are prioritized and released promptly:

1. **Critical**: Released within 24-48 hours
2. **High**: Released within 1 week
3. **Medium**: Released in next minor version
4. **Low**: Released in regular update cycle

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities. Contributors will be credited in:
- Security advisories (with permission)
- Release notes
- GitHub security acknowledgments

## Additional Resources

- [OWASP Python Security Guide](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Bandit Security Scanner](https://bandit.readthedocs.io/)

## Questions?

For non-security questions, please use:
- GitHub Issues for bug reports
- GitHub Discussions for general questions

Thank you for helping keep py-netatmo-truetemp secure!
