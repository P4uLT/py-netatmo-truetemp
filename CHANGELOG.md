## Unreleased

### Feat

- add automated release workflow with commitizen and taskfile (#16)

### Fix

- **ci**: fetch tags explicitly in release workflow (#18)

## v0.1.0 (2025-12-18)

### Feat

- **Initial Release**: Python 3.13+ client for Netatmo TrueTemperature API ([#1](https://github.com/P4uLT/py-netatmo-truetemp/pull/1))
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
  - Type distribution marker (py.typed)
- **Codecov Integration**: Test coverage tracking ([#3](https://github.com/P4uLT/py-netatmo-truetemp/pull/3))
- **Automated Dependencies**: Dependabot with uv support ([#4](https://github.com/P4uLT/py-netatmo-truetemp/pull/4))

### Fix

- codecov upload configuration for examples test coverage ([#14](https://github.com/P4uLT/py-netatmo-truetemp/pull/14))
- codecov badge URL to use modern format ([#15](https://github.com/P4uLT/py-netatmo-truetemp/pull/15))

### Chore

- update requests from 2.32.3 to 2.32.5 ([#2](https://github.com/P4uLT/py-netatmo-truetemp/pull/2))
- update platformdirs from 4.5.0 to 4.5.1 ([#11](https://github.com/P4uLT/py-netatmo-truetemp/pull/11))
- update pre-commit from 4.5.0 to 4.5.1 ([#12](https://github.com/P4uLT/py-netatmo-truetemp/pull/12))
- update dev dependencies: pytest, pytest-cov, bandit ([#10](https://github.com/P4uLT/py-netatmo-truetemp/pull/10))
- upgrade actions/setup-python from 5 to 6 ([#5](https://github.com/P4uLT/py-netatmo-truetemp/pull/5))
- upgrade astral-sh/setup-uv from 5 to 7 ([#7](https://github.com/P4uLT/py-netatmo-truetemp/pull/7))
- upgrade actions/upload-artifact from 4 to 6 ([#8](https://github.com/P4uLT/py-netatmo-truetemp/pull/8))
- upgrade actions/checkout from 4 to 6 ([#9](https://github.com/P4uLT/py-netatmo-truetemp/pull/9))
- upgrade codecov/codecov-action from 4 to 5 ([#6](https://github.com/P4uLT/py-netatmo-truetemp/pull/6))

**Security Notes:**
- Secure cookie storage with proper file permissions (0o600)
- HTTPS-only communication with Netatmo API
- No unsafe pickle serialization (uses JSON)
- Environment variable-based credential management
