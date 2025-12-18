# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-12-14

### Added
- Initial Python 3.13+ client for Netatmo TrueTemperature API ([#1](https://github.com/P4uLT/py-netatmo-truetemp/pull/1))
- SOLID architecture with clean separation of concerns (Facade → Service → Infrastructure layers)
- Thread-safe authentication manager with session locking and cookie caching
- JSON-based cookie storage with secure file permissions (0o600) for Linux, macOS, and Windows
- Smart temperature updates with 0.1°C tolerance to skip redundant API calls
- Auto-retry mechanism for 403 authentication errors with automatic token refresh
- Comprehensive type hints with TypedDict definitions for all API responses
- Room management: list and lookup rooms by name (case-insensitive) or ID
- Full test suite with pytest and multi-platform CI (Linux, macOS, Windows)
- Security scanning with bandit and type checking with mypy
- Code quality enforcement with ruff linter and formatter
- Pre-commit hooks for automated code quality checks
- CLI example application with Rich UI for terminal formatting
- Comprehensive documentation (README, CLAUDE.md, CONTRIBUTING.md)
- Open-source community files (LICENSE, CODE_OF_CONDUCT, SECURITY)
- GitHub issue and pull request templates
- Codecov integration for test coverage tracking ([#3](https://github.com/P4uLT/py-netatmo-truetemp/pull/3))
- Automated dependency updates with Dependabot and uv support ([#4](https://github.com/P4uLT/py-netatmo-truetemp/pull/4))
- Type distribution marker (py.typed)

### Fixed
- Codecov upload configuration for examples test coverage ([#14](https://github.com/P4uLT/py-netatmo-truetemp/pull/14))
- Codecov badge URL to use modern format ([#15](https://github.com/P4uLT/py-netatmo-truetemp/pull/15))

### Changed
- Updated requests from 2.32.3 to 2.32.5 ([#2](https://github.com/P4uLT/py-netatmo-truetemp/pull/2))
- Updated platformdirs from 4.5.0 to 4.5.1 ([#11](https://github.com/P4uLT/py-netatmo-truetemp/pull/11))
- Updated pre-commit from 4.5.0 to 4.5.1 ([#12](https://github.com/P4uLT/py-netatmo-truetemp/pull/12))
- Updated dev dependencies: pytest, pytest-cov, bandit ([#10](https://github.com/P4uLT/py-netatmo-truetemp/pull/10))
- Upgraded GitHub Actions: actions/setup-python from 5 to 6 ([#5](https://github.com/P4uLT/py-netatmo-truetemp/pull/5))
- Upgraded GitHub Actions: astral-sh/setup-uv from 5 to 7 ([#7](https://github.com/P4uLT/py-netatmo-truetemp/pull/7))
- Upgraded GitHub Actions: actions/upload-artifact from 4 to 6 ([#8](https://github.com/P4uLT/py-netatmo-truetemp/pull/8))
- Upgraded GitHub Actions: actions/checkout from 4 to 6 ([#9](https://github.com/P4uLT/py-netatmo-truetemp/pull/9))
- Upgraded GitHub Actions: codecov/codecov-action from 4 to 5 ([#6](https://github.com/P4uLT/py-netatmo-truetemp/pull/6))

### Security
- Secure cookie storage with proper file permissions (0o600)
- HTTPS-only communication with Netatmo API
- No unsafe pickle serialization (uses JSON)
- Environment variable-based credential management
