# Release Process

This document outlines the process for releasing py-netatmo-truetemp to PyPI.

## Prerequisites

Before publishing to PyPI, ensure:

1. All CI checks pass
2. Test coverage > 90%
3. All documentation is up to date
4. CHANGELOG.md has been updated with release notes
5. Version number follows semantic versioning

## Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality (backwards-compatible)
- **PATCH** version (0.0.X): Bug fixes (backwards-compatible)

For pre-1.0.0 releases:
- 0.1.0 -> 0.2.0: Minor breaking changes are acceptable
- 0.1.0 -> 0.1.1: Bug fixes and minor features

## Release Checklist

### 1. Pre-Release Validation

```bash
# Ensure clean working directory
git status

# Update from main
git checkout main
git pull origin main

# Run full test suite
uv run pytest tests/ -v --cov=src/py_netatmo_truetemp --cov-report=term-missing

# Run all quality checks
uv run ruff format --check src/ tests/
uv run ruff check src/ tests/
uv run mypy src/py_netatmo_truetemp/
uv run bandit -r src/py_netatmo_truetemp/ -ll

# Validate package imports
uv run python -c "from py_netatmo_truetemp import NetatmoAPI; print('✓ Imports validated')"
```

### 2. Update Version and Changelog

```bash
# Edit pyproject.toml version (e.g., 0.1.0 -> 0.2.0)
# Update CHANGELOG.md:
# - Move unreleased items to new version section
# - Add release date
# - Update comparison links at bottom
```

Example CHANGELOG.md update:
```markdown
## [0.2.0] - 2024-12-15

### Added
- New camera service for security camera integration
- Support for custom authentication providers

### Changed
- Improved error messages for authentication failures

### Fixed
- Cookie storage race condition on Windows

[0.2.0]: https://github.com/P4uLT/py-netatmo-truetemp/compare/v0.1.0...v0.2.0
```

### 3. Test Build Locally

```bash
# Build the package
uv build

# Inspect the built files
ls -lh dist/

# Check package metadata
uv run twine check dist/*

# Test installation in isolated environment
uv venv test-install-env
uv pip install --python test-install-env dist/*.whl
uv run --python test-install-env python -c "from py_netatmo_truetemp import NetatmoAPI; print('✓ Package installed successfully')"

# Clean up
rm -rf test-install-env
```

### 4. Commit Release Changes

```bash
# Commit version bump and changelog
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"
git push origin main
```

### 5. Test PyPI Release (Recommended First Time)

```bash
# Build clean package
rm -rf dist/
uv build

# Upload to Test PyPI
uv run twine upload --repository testpypi dist/*

# Test installation from Test PyPI
uv venv test-pypi-install
uv pip install --python test-pypi-install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    py-netatmo-truetemp

# Verify it works
uv run --python test-pypi-install python -c "from py_netatmo_truetemp import NetatmoAPI; print('✓ TestPyPI package works')"

# Clean up
rm -rf test-pypi-install
```

**Note**: Test PyPI credentials needed. Configure in `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...  # Your Test PyPI token
```

### 6. Create Git Tag

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push tag to GitHub
git push origin v0.2.0
```

### 7. Create GitHub Release

Go to https://github.com/P4uLT/py-netatmo-truetemp/releases/new

- **Tag**: Select `v0.2.0`
- **Release title**: `v0.2.0`
- **Description**: Copy from CHANGELOG.md for this version
- **Attachments**: Upload `dist/*.whl` and `dist/*.tar.gz`
- Click "Publish release"

### 8. Publish to PyPI

```bash
# Build clean package (if not already done)
rm -rf dist/
uv build

# Upload to PyPI
uv run twine upload dist/*
```

PyPI credentials needed. Configure in `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-...  # Your PyPI token
```

**Or use trusted publishing** (recommended):
1. Configure GitHub Actions workflow (see below)
2. Set up trusted publisher on PyPI
3. Releases publish automatically on tag creation

### 9. Verify PyPI Release

```bash
# Wait a few minutes for PyPI to index

# Install from PyPI
uv venv verify-pypi
uv pip install --python verify-pypi py-netatmo-truetemp

# Test installation
uv run --python verify-pypi python -c "from py_netatmo_truetemp import NetatmoAPI; print('✓ PyPI package works')"

# Clean up
rm -rf verify-pypi
```

### 10. Post-Release

- Update README.md installation instructions (remove "from GitHub" note)
- Announce release (GitHub Discussions, social media, etc.)
- Monitor issues for any release-related problems
- Start new "Unreleased" section in CHANGELOG.md

## Automated Release with GitHub Actions (Future)

Once you're comfortable with the manual process, you can automate with GitHub Actions.

### Setup Trusted Publishing

1. Go to PyPI project settings: https://pypi.org/manage/project/py-netatmo-truetemp/settings/
2. Add a new trusted publisher:
   - **PyPI project name**: `py-netatmo-truetemp`
   - **GitHub repository**: `P4uLT/py-netatmo-truetemp`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

3. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

permissions:
  contents: read
  id-token: write

jobs:
  build:
    name: Build Distribution
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - uses: astral-sh/setup-uv@v5
      - run: uv build
      - uses: actions/upload-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

  publish-to-pypi:
    name: Publish to PyPI
    needs: [build]
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/py-netatmo-truetemp
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: python-package-distributions
          path: dist/
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### Automated Release Process

With GitHub Actions configured:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push to main
4. Create and push git tag: `git tag v0.2.0 && git push origin v0.2.0`
5. Create GitHub release from tag
6. GitHub Actions automatically builds and publishes to PyPI

## Version Management Tools

Consider using a version management tool to automate version bumping:

### Option 1: Manual (current approach)
- Edit `pyproject.toml` version manually
- Full control, simple

### Option 2: hatch version
```bash
# Already using hatchling as build backend
uv run hatch version patch  # 0.1.0 -> 0.1.1
uv run hatch version minor  # 0.1.0 -> 0.2.0
uv run hatch version major  # 0.1.0 -> 1.0.0
```

### Option 3: bump-my-version
```bash
# Install
uv add --dev bump-my-version

# Configure in pyproject.toml
[tool.bumpversion]
current_version = "0.1.0"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
search = "{current_version}"
replace = "{new_version}"
regex = false
ignore_missing_version = false
tag = true
sign_tags = false
tag_name = "v{new_version}"
tag_message = "Bump version: {current_version} → {new_version}"
allow_dirty = false
commit = true
message = "chore: bump version to {new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

# Usage
bump-my-version bump patch  # Updates pyproject.toml, creates commit & tag
```

## Troubleshooting

### Build Fails

```bash
# Clear build artifacts
rm -rf dist/ build/ *.egg-info

# Check for syntax errors
uv run python -m py_compile src/py_netatmo_truetemp/*.py

# Rebuild
uv build
```

### Twine Upload Fails

```bash
# Check credentials
cat ~/.pypirc

# Check package metadata
uv run twine check dist/*

# Try with verbose output
uv run twine upload --verbose dist/*
```

### Version Already Exists on PyPI

Cannot re-upload same version. Options:
1. Delete version from PyPI (if just published)
2. Bump to next patch version (0.1.0 -> 0.1.1)

### Import Fails After Install

```bash
# Check what got installed
uv pip show py-netatmo-truetemp

# Check package contents
unzip -l dist/*.whl

# Verify package structure includes src/py_netatmo_truetemp/
```

## Support

For release process questions:
- Check [Python Packaging Guide](https://packaging.python.org/)
- Review [PyPI Help](https://pypi.org/help/)
- Ask in [GitHub Discussions](https://github.com/P4uLT/py-netatmo-truetemp/discussions)