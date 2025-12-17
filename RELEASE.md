# Release Process

This document outlines the **automated release process** for py-netatmo-truetemp using **Commitizen** and **PyPI Trusted Publishing**.

## Overview

Releases are semi-automated:
1. **Manual trigger**: Run `cz bump --changelog` when ready to release
2. **Automatic publishing**: GitHub Actions publishes to PyPI when you push the git tag
3. **Changelog generation**: Commitizen automatically updates CHANGELOG.md from conventional commits

## Prerequisites

Before your first release:

1. ✅ All CI checks pass
2. ✅ Test coverage > 90%
3. ✅ All documentation is up to date
4. ✅ Conventional commits enforced via pre-commit hook
5. ✅ PyPI Trusted Publishing configured (see First-Time Setup below)

## Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes (use `feat!:` or `BREAKING CHANGE:` in commits)
- **MINOR** version (0.X.0): New functionality, backwards-compatible (use `feat:` commits)
- **PATCH** version (0.0.X): Bug fixes, backwards-compatible (use `fix:` commits)

For pre-1.0.0 releases:
- 0.1.0 -> 0.2.0: Minor breaking changes are acceptable
- 0.1.0 -> 0.1.1: Bug fixes and minor features

## Quick Release (Automated Workflow)

### 1. Pre-Release Validation

```bash
# Ensure clean working directory
git status

# Update from main
git checkout main
git pull

# Run full test suite
uv run pytest tests/ -v --cov=src/py_netatmo_truetemp --cov-report=term-missing

# Run all quality checks
uv run ruff format --check src/ tests/
uv run ruff check src/ tests/
uv run mypy src/py_netatmo_truetemp/
uv run bandit -r src/py_netatmo_truetemp/ -ll
```

### 2. Bump Version and Generate Changelog

Commitizen handles version bumping and changelog updates automatically:

```bash
# Automatic bump (analyzes commits, determines version)
cz bump --changelog

# Or specify increment manually
cz bump --changelog --increment PATCH   # 0.1.0 -> 0.1.1
cz bump --changelog --increment MINOR   # 0.1.0 -> 0.2.0
cz bump --changelog --increment MAJOR   # 0.1.0 -> 1.0.0

# Dry run (see what would change)
cz bump --changelog --dry-run
```

**What `cz bump` does:**
- Analyzes commit messages since last release
- Determines version increment based on conventional commits
- Updates `pyproject.toml` version
- Updates `src/py_netatmo_truetemp/__init__.py __version__`
- Generates changelog entry in `CHANGELOG.md`
- Creates git commit: `chore: bump version to X.Y.Z`
- Creates git tag: `vX.Y.Z`

### 3. Push to Trigger Automated Release

```bash
# Review changes before pushing
git show HEAD
cat CHANGELOG.md

# Push commit and tag (triggers GitHub Actions)
git push && git push --tags

# Monitor GitHub Actions
# Go to: https://github.com/P4uLT/py-netatmo-truetemp/actions
```

**What happens automatically:**
1. GitHub Actions workflow (`publish.yml`) triggers on tag push
2. Builds package with `uv build`
3. Validates with `twine check`
4. Publishes to PyPI via Trusted Publishing (no tokens needed!)

### 4. Create GitHub Release

```bash
# Go to releases page
open https://github.com/P4uLT/py-netatmo-truetemp/releases/new

# Or use GitHub CLI
gh release create v0.2.0 \
  --title "v0.2.0" \
  --notes "$(git tag -l --format='%(contents)' v0.2.0)" \
  --verify-tag
```

**Manual steps:**
- Select the new tag
- Copy changelog entry for release notes
- Publish release

### 5. Verify Release

```bash
# Wait 1-2 minutes for PyPI to index

# Test installation
uv venv verify-release
uv pip install --python verify-release py-netatmo-truetemp

# Verify version
uv run --python verify-release python -c "import py_netatmo_truetemp; print(py_netatmo_truetemp.__version__)"

# Clean up
rm -rf verify-release
```

That's it! Three simple steps:
1. `cz bump --changelog`
2. `git push && git push --tags`
3. Create GitHub Release (optional but recommended)

## First-Time Setup

### Step 1: Manual First Release to Create PyPI Project

**Why:** PyPI Trusted Publishing requires the project to exist first. The first release must be manual.

```bash
# Build package
uv build

# Option A: Test on TestPyPI first (recommended)
uv run twine upload --repository testpypi dist/*

# Verify TestPyPI installation
uv venv test-install
uv pip install --python test-install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    py-netatmo-truetemp
rm -rf test-install

# Option B: Upload directly to production PyPI
uv run twine upload dist/*
```

**Configure credentials in `~/.pypirc`:**
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your PyPI API token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...  # Your Test PyPI token
```

**Get API tokens:**
- PyPI: https://pypi.org/manage/account/token/
- Test PyPI: https://test.pypi.org/manage/account/token/

### Step 2: Configure PyPI Trusted Publishing

After the first manual release:

1. Go to PyPI project settings:
   - https://pypi.org/manage/project/py-netatmo-truetemp/settings/publishing/

2. Add trusted publisher:
   - **PyPI project name**: `py-netatmo-truetemp`
   - **Owner**: `P4uLT`
   - **Repository name**: `py-netatmo-truetemp`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `release`

3. Save changes

### Step 3: Create GitHub Environment

1. Go to repository settings:
   - https://github.com/P4uLT/py-netatmo-truetemp/settings/environments

2. Create environment named `release`
   - Optional: Add protection rules (require reviews)
   - Optional: Add deployment branches (only `main`)

### Step 4: Test Automated Release

```bash
# Create a test feature commit
git commit --allow-empty -m "feat: test automated release"
git push

# Trigger release
cz bump --changelog
git push && git push --tags

# Watch GitHub Actions
gh run watch
```

## Commit Message Guidelines

Commitizen enforces conventional commits via pre-commit hook. Format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types that affect versioning:**
- `feat:` → MINOR version bump (new feature)
- `fix:` → PATCH version bump (bug fix)
- `feat!:` or `BREAKING CHANGE:` → MAJOR version bump

**Other types (no version bump):**
- `chore:` → Maintenance tasks
- `docs:` → Documentation changes
- `test:` → Test additions/changes
- `refactor:` → Code restructuring
- `style:` → Formatting changes
- `ci:` → CI/CD changes
- `perf:` → Performance improvements

**Examples:**
```bash
# Minor version bump
git commit -m "feat: add camera service for security camera integration"

# Patch version bump
git commit -m "fix: resolve authentication retry loop"

# Major version bump (breaking change)
git commit -m "feat!: remove deprecated cookie_store parameter"

# With scope
git commit -m "feat(auth): add support for OAuth2 authentication"

# With body and footer
git commit -m "feat: add room scheduling

Allows users to schedule temperature changes for specific times.

Closes #42"
```

**Interactive commit helper:**
```bash
# Use Commitizen CLI for guided commit messages
cz commit
```

## Advanced: Manual Version Override

If you need to set a specific version (e.g., for major milestones):

```bash
# Set exact version
cz bump --changelog --version 1.0.0

# Pre-release versions
cz bump --changelog --version 1.0.0-beta.1
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
