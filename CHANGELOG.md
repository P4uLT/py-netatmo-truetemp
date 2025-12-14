# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with core library structure
- TrueTemperature API support for programmatic room temperature control
- Thread-safe authentication with session locking
- JSON-based cookie storage with secure file permissions (0o600)
- Smart temperature updates with 0.1°C tolerance
- Auto-retry mechanism for 403 authentication errors
- Comprehensive type hints with TypedDict definitions
- SOLID architecture with dependency injection
- Multi-platform cookie storage (Linux, macOS, Windows)
- Full test suite with pytest
- CI/CD pipeline with GitHub Actions
- Security scanning with bandit
- Type checking with mypy
- Linting with ruff and pre-commit hooks
- CLI example application with Rich UI
- Core API client functionality
- Home and thermostat service layers
- Authentication manager with cookie caching
- Input validation and error handling
- Comprehensive documentation (README, CLAUDE.md, CONTRIBUTING.md)
- Open-source community files (LICENSE, CODE_OF_CONDUCT, SECURITY)
- GitHub issue and PR templates
- Automated dependency updates with Dependabot
- Type distribution marker (py.typed)

### Security
- Secure cookie storage with proper file permissions
- HTTPS-only communication
- No unsafe pickle serialization
- Environment variable credential management
