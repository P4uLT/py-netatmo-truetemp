## [0.2.1](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/compare/v0.2.0...v0.2.1) (2026-01-13)

### Bug Fixes

* **ci:** use git config for release author ([#46](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/46)) ([325ac66](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/325ac6672b7e57665882df588c94516371ef4b31))

## [0.2.0](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/compare/v0.1.0...v0.2.0) (2026-01-13)

### Features

* add automated release workflow with commitizen and taskfile ([#16](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/16)) ([daad5a4](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/daad5a4f0bd0efefa4441c5461cb6a5079f1a52d))
* add gpg signing to release workflow ([#22](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/22)) ([0faa134](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/0faa1346243bd29ac8ea2e81e98f776e155cfc52))
* **ci:** add github app authentication for verified commits ([#21](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/21)) ([22e149f](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/22e149fcaa823a3dfa1113f6b7d1fe1d4414ac67))
* implement dynamic versioning with hatch-vcs ([#34](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/34)) ([ec7f932](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/ec7f932a5c30c2c1ce72dbfa76fa63b69d7b8c8a))
* use verified-git-commit plugin ([#30](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/30)) ([da44520](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/da445200a63c4c92546c89199c5c80e7f4cc0924))

### Bug Fixes

* **ci:** convert changelog to commitizen format ([#19](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/19)) ([0a85e77](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/0a85e776c81986975b4dbcc8af54cb766b33fa1a))
* **ci:** fetch tags explicitly in release workflow ([#18](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/18)) ([8c63868](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/8c638684272bddb8571e4c98a6fc34c8230589ee))
* **ci:** remove changelog_increment_filename parameter ([#20](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/20)) ([43cf7d9](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/43cf7d949ebc0a9f7443a4a5645b30c95be33931))
* **ci:** remove duplicate tag creation ([#27](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/27)) ([ed3db2e](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/ed3db2e280bebd102cf10f44136d6cda00164b6b))
* **ci:** set github app as commit author ([#28](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/28)) ([af195fc](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/af195fc31fa255a4fd3b338274a26bddf3287750))
* **ci:** use auto-commit for verified commits ([#26](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/26)) ([2e93f70](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/2e93f70ef63a78764accdafef4a58cf7bcd24ab7))
* **ci:** use github api for verified commits ([#29](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/29)) ([bc566b3](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/bc566b3d8ad83f76d09c1855dbe3840a54a52612))
* exclude _version.py from ruff format ([#43](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/43)) ([1c7ae3f](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/1c7ae3f22a1b970559fb61846c36d9bb9a761c8e))
* remove verified-git-commit plugin and restore github api approach ([#32](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/32)) ([cfbd268](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/cfbd268209f75e7d093715b13b30b4fb304a2c26))

### Reverts

* restore github api commit approach ([#31](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/issues/31)) ([b2a727c](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/commit/b2a727c7f800d30c04fe2484b69a007846e603b5))

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
