# CLI Cleanup and Opensource Checklist Update

**Date:** 2026-01-15
**Status:** Approved Design
**Goal:** Remove CLI remnants after CLI moved to dedicated repository, update opensource checklist

## Background

The CLI has been moved to a separate repository (`py-netatmo-truetemp-cli`). The library repository still contains:
- Complete `examples/` folder with CLI application (~500+ lines)
- CLI-specific documentation and references
- Outdated monorepo guide in root `/CLAUDE.md`

This plan transforms the repository from a monorepo structure into a clean library-only repository with external example backlinks.

## Files to Delete

### 1. Root CLAUDE.md
**Path:** `/CLAUDE.md`
**Reason:** Describes outdated monorepo structure that no longer exists
**Action:** Delete entirely (library has its own `py-netatmo-truetemp/CLAUDE.md`)

### 2. Examples Folder
**Path:** `examples/`
**Contents:**
```
examples/
├── cli.py                         # CLI commands (87 lines)
├── helpers.py                     # CLI helpers (174 lines)
├── display.py                     # Rich formatting (55 lines)
├── pyproject.toml                 # CLI dependencies (Typer, Rich)
├── Taskfile.yml                   # Task automation
├── .mise.local.toml               # Environment config
├── CLAUDE.md                      # CLI development guide (256 lines)
├── README.md                      # CLI usage docs
├── tests/                         # CLI tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cli.py
│   └── test_helpers.py
└── .venv/                         # CLI virtual environment
```
**Reason:** CLI now lives in separate repository
**Action:** Delete entire folder recursively

## Documentation Updates

### README.md Changes

**1. Remove Project Structure Section**
**Location:** Lines 197-222
**Current:** Describes library + examples structure
**Action:** Delete entire section

**2. Remove Testing with Examples**
**Location:** Line 235 in Development section
**Current:** "The `examples/` folder contains independent applications for testing library changes. See [`examples/README.md`](examples/README.md) for setup and usage instructions."
**Action:** Delete this subsection

**3. Remove Examples Documentation Links**
**Location:** Lines 271-272 in Documentation section
**Current:**
```markdown
- [examples/README.md](examples/README.md) - CLI setup and usage instructions
- [examples/CLAUDE.md](examples/CLAUDE.md) - CLI development workflow
```
**Action:** Delete these two lines

**4. Add Usage Examples Section**
**Location:** After "Quick Start" section (after line 100)
**Action:** Insert new section:

```markdown
## Usage Examples

### Command-Line Interface

For a complete CLI application built with this library, see:
- **[py-netatmo-truetemp-cli](https://github.com/P4uLT/py-netatmo-truetemp-cli)** - Full-featured CLI with Typer and Rich formatting

The CLI demonstrates:
- Environment-based configuration
- Error handling patterns
- Room lookup by name
- Formatted terminal output

### More Examples

Want to add your project here? Submit a PR or open an issue!
```

### CLAUDE.md Changes

**Location:** `py-netatmo-truetemp/CLAUDE.md`

**1. Remove CLI Examples Section**
**Current:** Lines 40-72 ("CLI Examples" section)
**Action:** Delete entire section

**2. Update Package Structure Section**
**Current:** Lines 196-256 (shows library + examples)
**Action:** Simplify to library-only structure:

```markdown
## Package Structure

This is a Python library package following modern src-layout structure:

```
src/py_netatmo_truetemp/     # Core library (installable package)
   ├── __init__.py            # Package exports
   ├── netatmo_api.py         # Main facade
   ├── cookie_store.py        # Cookie persistence
   ├── auth_manager.py        # Authentication (thread-safe)
   ├── api_client.py          # HTTP client (auto-retry)
   ├── home_service.py        # Home operations
   ├── thermostat_service.py  # Thermostat operations
   ├── types.py               # TypedDict definitions
   ├── validators.py          # Input validation
   ├── exceptions.py          # Custom exceptions
   ├── constants.py           # API endpoints
   └── logger.py              # Logging utilities
```

**Build Configuration**: The `pyproject.toml` includes `[build-system]` configuration using Hatchling, making the library installable via pip.

**Example Applications**: For usage examples, see the [py-netatmo-truetemp-cli](https://github.com/P4uLT/py-netatmo-truetemp-cli) repository.
```
```

**3. Remove See Also Links**
**Current:** Lines 282-289 (references to examples/CLAUDE.md and examples/README.md)
**Action:** Remove these lines from See Also section

## Opensource Checklist Updates

**Location:** `OPENSOURCE_CHECKLIST.md`

### Status Updates (Items Completed)

**Line 66:**
```markdown
- [x] **PyPI account** - Created and available
```

**Line 67:**
~~Delete this line~~ (Test PyPI trial not needed)

**Line 68:**
```markdown
- [x] **PyPI release** - Published and available
```

**Line 164:**
~~Delete this line~~ (Test PyPI upload successful)

**Line 165:**
```markdown
- [x] **PyPI upload** - Completed
```

**Line 192:**
```markdown
- [x] **PyPI listing** - Published and searchable
```

**Line 200:**
```markdown
- [x] **PyPI badges** - Download and version badges in README
```

**Line 208:**
```markdown
- [x] **Release automation** - GitHub Actions publishing enabled
```

### Summary Section Updates

**Line 244:**
```markdown
**Overall Status**: Production ready (published on PyPI)
```

**Line 246:**
```markdown
**Completed**: 44/47 items (93.6%)
```

**Lines 248-254 (Remaining for v0.x.x):**
```markdown
**Remaining**:
- [ ] Enable GitHub Discussions (Q&A and community)
- [ ] Enable branch protection on main (require PR reviews and CI checks)
- [ ] Announce project (Reddit r/Python, Python Weekly)
```

## Implementation Checklist

1. [ ] Delete `/CLAUDE.md`
2. [ ] Delete `examples/` folder recursively
3. [ ] Update `README.md`:
   - [ ] Remove Project Structure section (lines 197-222)
   - [ ] Remove Testing with Examples (line 235)
   - [ ] Remove examples documentation links (lines 271-272)
   - [ ] Add Usage Examples section after Quick Start
4. [ ] Update `py-netatmo-truetemp/CLAUDE.md`:
   - [ ] Remove CLI Examples section
   - [ ] Update Package Structure section
   - [ ] Remove examples/ links from See Also
5. [ ] Update `OPENSOURCE_CHECKLIST.md`:
   - [ ] Mark PyPI items as completed
   - [ ] Remove Test PyPI trial line
   - [ ] Update completion percentage
   - [ ] Update remaining items list
6. [ ] Validate all documentation links work
7. [ ] Commit changes with message: `docs: remove CLI examples after moving to dedicated repository`

## Expected Outcome

**Before:** Monorepo structure with library + CLI examples
**After:** Clean library repository with external example backlinks

**Benefits:**
- Clear separation of concerns (library vs. CLI)
- Simpler repository structure
- No confusion about what belongs where
- External examples via backlinks (extensible)
- Updated checklist reflects production-ready status (93.6% complete)

**No Breaking Changes:** Core library functionality unchanged; only documentation and examples affected.

## Next Steps After Implementation

1. Enable GitHub Discussions for community Q&A
2. Enable branch protection (require PR reviews and CI passing)
3. Announce on Reddit r/Python and Python Weekly
4. Add download badges to README using PyPI stats
