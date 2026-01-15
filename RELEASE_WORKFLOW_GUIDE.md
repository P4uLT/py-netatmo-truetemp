# Release Workflow Guide

This project uses **semantic-release** for fully automated releases. All versioning, changelog generation, and publishing happens automatically in CI when you push to the main branch.

## Quick Start

### Automated Releases (Only Method)

```bash
# 1. Make changes with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"

# 2. Push to main - automatic release happens
git push origin main

# GitHub Actions automatically:
# - Analyzes conventional commits
# - Determines version bump (major/minor/patch)
# - Updates version in pyproject.toml and __init__.py
# - Generates and updates CHANGELOG.md
# - Creates git tag with verified signature
# - Creates GitHub Release
# - Publishes to PyPI
```

That's it! No manual steps required.

## How It Works

### The Release Pipeline

The `.github/workflows/release.yml` workflow runs on every push to main:

1. **Commit Analysis**: Scans commits since last release using conventional commits format
2. **Version Calculation**: Determines next version based on commit types:
   - `feat:` → minor bump (0.1.0 → 0.2.0)
   - `fix:`, `perf:`, `revert:` → patch bump (0.1.0 → 0.1.1)
   - `feat!:` or `BREAKING CHANGE:` → major bump (0.1.0 → 1.0.0)
   - `docs:`, `refactor:`, `style:`, `test:`, `chore:`, `ci:` → no release
3. **Version Update**: Updates version in:
   - `pyproject.toml` (project.version)
   - `src/py_netatmo_truetemp/__init__.py` (__version__)
4. **Changelog Generation**: Automatically generates changelog from commits
5. **Git Tag Creation**: Creates signed tag using GitHub App
6. **GitHub Release**: Publishes release with changelog notes
7. **PyPI Publishing**: Triggered automatically by tag creation

### Smart Release Logic

- **Skip CI Commits**: Release commits contain `[skip ci]` to prevent infinite loops
- **No Unnecessary Releases**: If no `feat:` or `fix:` commits exist, no release is created
- **Verified Commits**: Uses GitHub App token for signed, verified commits
- **Automatic Labeling**: Adds `release` label during process, `released` label when complete

## Conventional Commits

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification (enforced by pre-commit hooks).

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types and Version Impact

| Type | Description | Version Bump | Shows in Changelog |
|------|-------------|--------------|-------------------|
| `feat:` | New feature | Minor | ✅ Features |
| `fix:` | Bug fix | Patch | ✅ Bug Fixes |
| `perf:` | Performance improvement | Patch | ✅ Performance |
| `revert:` | Revert previous commit | Patch | ✅ Reverts |
| `docs:` | Documentation only | None* | ✅ Documentation |
| `refactor:` | Code refactoring | None | ❌ Hidden |
| `style:` | Code style/formatting | None | ❌ Hidden |
| `test:` | Tests only | None | ❌ Hidden |
| `chore:` | Maintenance tasks | None | ❌ Hidden |
| `ci:` | CI/CD changes | None | ❌ Hidden |

*`docs:` with scope `README` triggers patch bump

### Breaking Changes

Use `!` after the type or add `BREAKING CHANGE:` footer for major version bumps:

```bash
# Method 1: Exclamation mark
git commit -m "feat!: redesign API interface"

# Method 2: Footer
git commit -m "feat: add new authentication

BREAKING CHANGE: NetatmoAPI constructor signature changed"
```

### Examples

```bash
# Feature (minor bump: 0.1.0 → 0.2.0)
git commit -m "feat: add temperature scheduling support"

# Bug fix (patch bump: 0.1.0 → 0.1.1)
git commit -m "fix: handle authentication timeout errors"

# Performance improvement (patch bump)
git commit -m "perf: optimize API request caching"

# Breaking change (major bump: 0.1.0 → 1.0.0)
git commit -m "feat!: redesign thermostat service API"

# With scope
git commit -m "feat(api): add room listing endpoint"

# Documentation (no release, unless README scope)
git commit -m "docs: update installation instructions"
git commit -m "docs(README): fix installation command"  # triggers patch

# No release
git commit -m "refactor: simplify authentication logic"
git commit -m "test: add unit tests for thermostat service"
git commit -m "chore: update dependencies"
```

## Checking Your Commits

Before pushing, verify your commits will trigger a release:

```bash
# View recent commits
git log --oneline -10

# View commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Check if commits follow conventional format
git log --oneline -10 | grep -E "^[a-f0-9]+ (feat|fix|perf|revert|docs|refactor|style|test|chore|ci)"
```

Use the pre-commit hooks to catch format errors early:

```bash
# Install hooks
uv run pre-commit install

# Test manually
uv run pre-commit run --all-files
```

## Monitoring Releases

### Watch the Workflow

After pushing to main:

1. Go to **Actions** tab in GitHub
2. Click on the **Release** workflow run
3. Monitor the steps in real-time

Direct link: `https://github.com/py-netatmo-unofficial/py-netatmo-truetemp/actions`

### Verify Release Success

Check these indicators:

1. **New Git Tag**: `git fetch --tags && git tag -l`
2. **GitHub Release**: Go to Releases page
3. **Updated Files**: Check `CHANGELOG.md`, `pyproject.toml`, `__init__.py`
4. **PyPI**: Visit https://pypi.org/project/py-netatmo-truetemp/

## Troubleshooting

### No Release Created

**Symptom**: Workflow runs but no release is created

**Causes**:
- No `feat:` or `fix:` commits since last release
- Only non-release commits (`docs:`, `refactor:`, `chore:`, etc.)
- Commits don't follow conventional format

**Solution**:
```bash
# Check commit history
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Verify conventional commit format
# Each commit should start with: feat:, fix:, etc.
```

### Workflow Fails

**Symptom**: Red X on workflow run

**Causes**:
- Syntax error in `.releaserc.json`
- Missing GitHub App credentials
- Permission issues

**Solution**:
1. Click on failed workflow run to see error
2. Check workflow logs for specific error message
3. Verify GitHub App token is configured (Settings → Secrets)

### Version Files Out of Sync

**Symptom**: Version differs between `pyproject.toml` and `__init__.py`

**Cause**: Manual edits or workflow failure

**Solution**: Let semantic-release fix it on next release. Never edit version manually.

### Pre-commit Hook Rejects Commit

**Symptom**: `commit-msg` hook fails

**Cause**: Commit message doesn't follow conventional format

**Solution**:
```bash
# Bad
git commit -m "added new feature"
git commit -m "bug fix"

# Good
git commit -m "feat: add temperature scheduling"
git commit -m "fix: resolve authentication timeout"
```

### Need to Skip CI

**Symptom**: Want to push without triggering release

**Solution**: Add `[skip ci]` to commit message:
```bash
git commit -m "docs: update README [skip ci]"
```

Note: Only use for documentation or non-code changes. Semantic-release already handles this for release commits.

### PR Cannot Merge - CI Status Check Blocking

**Symptom**: "Merging is blocked - Required status check 'ci-success' is pending/failing"

**Cause**: CI hasn't completed or has failed. GitHub ruleset requires all CI checks to pass before merge.

**Solution**:
1. Click "Details" next to the failed check in your PR
2. Review error logs to identify the issue
3. Fix issues locally:
   - **Linting errors**: `uv run ruff check --fix src/ tests/`
   - **Type errors**: `uv run mypy src/py_netatmo_truetemp/` and fix reported issues
   - **Test failures**: `uv run pytest tests/ -v` and fix failing tests
   - **Format issues**: `uv run ruff format src/ tests/`
4. Commit fixes and push to your PR branch
5. CI will automatically re-run
6. Merge button unlocks when all checks pass

**Prevention**: Run all checks locally before pushing:
```bash
uv run pre-commit run --all-files
uv run pytest tests/ -v
```

### PyPI Publish Failed

**Symptom**: Release workflow completes but PyPI publish workflow fails

**Cause**: Version already exists on PyPI, or OIDC token issue

**Solution**:
1. Check if version already exists:
   ```bash
   pip index versions py-netatmo-truetemp
   ```
2. If version exists: semantic-release prevented duplicate (expected behavior)
3. If OIDC issue:
   - Verify PyPI trusted publisher settings at https://pypi.org/manage/project/py-netatmo-truetemp/settings/publishing/
   - Ensure GitHub Actions workflow name matches trusted publisher configuration
   - Check workflow has `id-token: write` permission

**Recovery**: Re-run the failed workflow manually (workflows are idempotent)

### Commit Not Signed

**Symptom**: "Required signatures not satisfied" - PR merge blocked

**Cause**: Commit lacks GPG/SSH signature. GitHub ruleset requires all commits to be signed.

**Solution**:
```bash
# Option 1: Configure GPG signing
git config --global commit.gpgsign true
git config --global user.signingkey YOUR_GPG_KEY_ID

# Option 2: Configure SSH signing (simpler)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Amend last commit with signature
git commit --amend --no-edit -S
git push --force-with-lease

# Or create new commit
git commit --allow-empty -m "chore: trigger CI with signed commit" -S
git push
```

**Add signing key to GitHub**:
- Settings → SSH and GPG keys → New GPG key (or New SSH key with type: Signing Key)

### Release Created But No PyPI Package

**Symptom**: GitHub Release exists, but package not on PyPI

**Cause**: PyPI publish workflow didn't trigger or failed

**Solution**:
1. Check Actions tab for "Publish to PyPI" workflow
2. Verify workflow was triggered by tag creation
3. If workflow missing: Check `.github/workflows/publish.yml` trigger is `on: push: tags: - 'v*.*.*'`
4. If workflow failed: Check logs for OIDC or build errors
5. Manual publish (emergency only):
   ```bash
   git checkout v0.2.0  # checkout the release tag
   uv build
   uv run twine upload dist/*  # requires PyPI token
   ```

## Emergency Procedures

### Critical Bug in Latest Release

**Don't panic!** Fix forward:

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main

# 2. Fix the bug
# ... make changes ...

# 3. Commit with fix: type
git commit -m "fix: resolve critical authentication bug"

# 4. Push - automatic patch release
git push origin main

# Result: 0.2.0 → 0.2.1 (automatic)
```

### Accidentally Pushed Breaking Change

If you pushed a commit with `feat!:` or `BREAKING CHANGE:` by mistake:

**Option 1: Accept it** (Recommended)
- Let the major version bump happen
- Document in release notes
- If not actually breaking, clarify in GitHub Release description

**Option 2: Revert** (Before release runs)
```bash
git revert HEAD
git push origin main
# Semantic-release won't create release (revert commits trigger patch, but cancel out the breaking change)
```

**Option 3: Manual intervention** (After release already created)
- Cannot undo - versions are permanent
- Fix forward with new release
- Update GitHub Release notes to clarify

### Workflow Permanently Broken

If semantic-release workflow is completely broken:

1. **Check workflow file**: `.github/workflows/release.yml`
2. **Verify secrets**: GitHub App credentials in Settings → Secrets
3. **Test locally** (requires Node.js):
   ```bash
   npm install -g semantic-release @semantic-release/changelog @semantic-release/git @semantic-release/exec conventional-changelog-conventionalcommits
   semantic-release --dry-run
   ```
4. **Manual release** (last resort):
   ```bash
   # Manually update version
   # Edit pyproject.toml and __init__.py

   # Update changelog
   # Edit CHANGELOG.md

   # Create tag
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0

   # Create GitHub Release manually
   gh release create v0.2.0 --notes "Release notes here"
   ```

## Configuration

### semantic-release Configuration

The `.releaserc.json` file controls release behavior:

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/exec",
    "@semantic-release/git",
    "@semantic-release/github"
  ]
}
```

**Key settings**:
- `branches`: Only `main` triggers releases
- `releaseRules`: Defines which commit types trigger releases
- `changelogTitle`: Sets changelog header format
- `message`: Template for release commit message

### GitHub Workflow Configuration

The `.github/workflows/release.yml` requires:

**Secrets**:
- `APP_ID`: GitHub App ID (for verified commits)
- `APP_PRIVATE_KEY`: GitHub App private key

**Permissions**:
- `contents: write` - Create commits, tags, releases
- `id-token: write` - PyPI trusted publishing

### Pre-commit Hooks

The `.pre-commit-config.yaml` enforces commit message format:

```yaml
- repo: https://github.com/compwa/commitizen-pre-commit
  hooks:
    - id: commitizen
      stages: [commit-msg]
```

Install hooks:
```bash
uv run pre-commit install --hook-type commit-msg
```

## Best Practices

1. **Trust the Automation**: Don't manually edit version numbers or CHANGELOG.md
2. **Write Good Commit Messages**: Clear, descriptive, following conventional format
3. **Use Scopes**: Add scope for better organization: `feat(api):`, `fix(auth):`
4. **Group Related Changes**: Squash related commits before merging
5. **Test Before Pushing**: Run tests locally before pushing to main
6. **Monitor Releases**: Check Actions tab after pushing
7. **Fix Forward**: Never revert releases - fix bugs with new releases
8. **Document Breaking Changes**: Explain impact in commit body

## FAQ

**Q: Can I release manually?**
A: No. Semantic-release handles all releases automatically. This ensures consistency and verified commits.

**Q: Can I choose the version number?**
A: No. Version is determined automatically by commit types. Use correct commit types (`feat:`, `fix:`, etc.) to control version bumps.

**Q: What if I need to test releases?**
A: Use a separate branch or fork. The main branch is for production releases only.

**Q: Can I skip a release?**
A: Yes, by only pushing non-release commits (`refactor:`, `docs:`, `test:`, `chore:`).

**Q: How do I make a hotfix?**
A: Push a `fix:` commit to main. It will automatically create a patch release.

**Q: Can I release from a feature branch?**
A: No. Only commits on `main` trigger releases. Merge your feature branch to main first.

**Q: What if the workflow fails?**
A: Fix the underlying issue (usually permissions or configuration) and push a new commit. The workflow will retry.

## References

- [Semantic Release Documentation](https://semantic-release.gitbook.io/)
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
