# Release Workflow Guide

This project uses automated releases with commitizen for semantic versioning and conventional commits.

## Quick Start

### Automatic Releases (Recommended)

```bash
# 1. Make changes with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"

# 2. Push to main - automatic release happens
git push origin main

# GitHub Actions automatically:
# - Bumps version based on commits
# - Updates CHANGELOG.md
# - Creates git tag
# - Creates GitHub Release
# - Publishes to PyPI
```

### Manual Local Releases

```bash
# Preview what would happen
task release:dry-run
task git:unreleased

# Create release locally
task release:bump          # Auto-detect version
task release:major         # Force major bump (0.1.0 → 1.0.0)
task release:minor         # Force minor bump (0.1.0 → 0.2.0)
task release:patch         # Force patch bump (0.1.0 → 0.1.1)

# Review and push
task git:log
task changelog:latest
task release:push          # Triggers GitHub Actions
```

## Taskfile Commands

Run `task --list` to see all available commands, or `task help:guide` for detailed help.

### Release Commands

- `task release:bump` - Create release with auto version detection
- `task release:major` - Force major version bump
- `task release:minor` - Force minor version bump
- `task release:patch` - Force patch version bump
- `task release:dry-run` - Preview what would be released
- `task release:check` - Check if release is needed
- `task release:push` - Push release to GitHub (triggers automation)

### Version Commands

- `task version:current` - Show current version
- `task version:history` - Show release history
- `task version:latest` - Show latest release tag
- `task version:next` - Predict next version
- `task version:sync-check` - Verify version files are in sync

### Changelog Commands

- `task changelog:show` - Display full changelog
- `task changelog:preview` - Preview next changelog
- `task changelog:latest` - Show latest release notes
- `task changelog:unreleased` - Show unreleased changes

### Git Commands

- `task git:log` - Show recent commits
- `task git:since-release` - Show commits since last release
- `task git:unreleased` - Show unreleased changes grouped by type
- `task git:status` - Show git status
- `task git:tags` - List all tags

### Help Commands

- `task help:guide` - Show complete workflow guide
- `task help:release` - Show release workflow
- `task help:commits` - Show conventional commit format guide

## Conventional Commits

This project requires conventional commit format (enforced by pre-commit hooks):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat:` | New feature | Minor (0.1.0 → 0.2.0) |
| `fix:` | Bug fix | Patch (0.1.0 → 0.1.1) |
| `feat!:` | Breaking change | Major (0.1.0 → 1.0.0) |
| `docs:` | Documentation | None |
| `style:` | Code style | None |
| `refactor:` | Code refactoring | None |
| `perf:` | Performance | None |
| `test:` | Tests | None |
| `chore:` | Maintenance | None |
| `ci:` | CI/CD changes | None |

### Examples

```bash
# Feature (minor bump)
git commit -m "feat: add temperature scheduling"

# Bug fix (patch bump)
git commit -m "fix: handle auth timeout errors"

# Breaking change (major bump)
git commit -m "feat!: redesign API interface"

# With scope
git commit -m "feat(api): add new endpoint"

# With body and footer
git commit -m "feat: add user authentication

Add OAuth2 support for user authentication

BREAKING CHANGE: NetatmoAPI constructor now requires home_id"
```

## How It Works

### Automatic Workflow

The `.github/workflows/release.yml` workflow:

1. **Triggers** on push to main branch
2. **Uses** commitizen-action to:
   - Analyze conventional commits
   - Bump version in `pyproject.toml` and `__init__.py`
   - Update `CHANGELOG.md`
   - Create git tag
   - Push changes back to main
3. **Creates** GitHub Release with changelog
4. **Triggers** publish workflow (on tag push) to publish to PyPI

### Infinite Loop Prevention

The workflow won't trigger on its own bump commits:
```yaml
if: "!startsWith(github.event.head_commit.message, 'bump:')"
```

### Smart Skipping

If there are no `feat:` or `fix:` commits since the last release, no release is created.

## Troubleshooting

### No Release Created

**Cause**: No conventional commits since last release

**Fix**: Ensure commits follow conventional format (`feat:`, `fix:`, etc.)

### Version Not Bumping

**Debug locally**:
```bash
task release:dry-run
task git:unreleased
```

### Permission Denied

**Cause**: GITHUB_TOKEN doesn't have write permissions

**Fix**: Go to Settings → Actions → General → Set "Workflow permissions" to "Read and write permissions"

### Version Files Out of Sync

**Check**:
```bash
task version:sync-check
```

**Fix**: Commitizen should keep them in sync automatically. If not, check `pyproject.toml` configuration.

## Emergency Manual Release

If the automated workflow fails:

```bash
# 1. Create release locally
task release:bump

# 2. Review changes
task git:log
task changelog:latest

# 3. Push manually
git push origin main
git push origin --tags

# 4. Create GitHub Release manually if needed
gh release create v0.2.0 --notes "$(task changelog:latest)"
```

## Configuration Files

### pyproject.toml

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
version_files = [
    "pyproject.toml:project.version",
    "pyproject.toml:tool.commitizen.version",
    "src/py_netatmo_truetemp/__init__.py:__version__",
]
tag_format = "v$version"
update_changelog_on_bump = true
changelog_file = "CHANGELOG.md"
```

### Taskfile.yml

Modular task structure:
- `tasks/release/` - Release operations
- `tasks/version/` - Version utilities
- `tasks/changelog/` - Changelog operations
- `tasks/git/` - Git utilities
- `tasks/help/` - Help and documentation

## Best Practices

1. **Use conventional commits** - Enforced by pre-commit hooks
2. **Let automation handle releases** - Push to main and let GitHub Actions do the work
3. **Use Taskfile for local testing** - Preview releases before pushing
4. **Fix forward, don't rollback** - Releases are permanent
5. **Review changes before pushing** - Use `task git:unreleased` and `task release:dry-run`

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Commitizen Documentation](https://commitizen-tools.github.io/commitizen/)
- [Taskfile Documentation](https://taskfile.dev/)
