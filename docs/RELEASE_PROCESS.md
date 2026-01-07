# Release Process

This document explains how to release new versions of the Stock Exchange Tracker.

## Release Workflows

You have two options for publishing updates:

### Option 1: Automated Publishing (Recommended)

Automated via GitHub Actions when you create a release.

### Option 2: Manual Publishing

Publish manually from your local machine.

---

## Option 1: Automated Publishing (Recommended)

### One-Time Setup

#### 1. Create PyPI API Token

1. Log in to [PyPI](https://pypi.org/)
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. **Scope**: Choose "Entire account" (or specific to `stock-exchange-tracker` after first publish)
5. Copy the token (starts with `pypi-`)

#### 2. Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. **Name**: `PYPI_API_TOKEN`
5. **Value**: Paste the token from PyPI
6. Click "Add secret"

#### 3. (Optional) Set up Test PyPI

For testing releases:

1. Create account on [Test PyPI](https://test.pypi.org/)
2. Generate API token
3. Add to GitHub Secrets as `TEST_PYPI_API_TOKEN`

### Release Process

Once set up, releasing is simple:

```bash
# 1. Update version in setup.cfg
# Change: version = 0.2.0
# To:     version = 0.3.0

# 2. Update CHANGELOG.md
# Add new section for v0.3.0 with changes

# 3. Commit and push to main
git add setup.cfg CHANGELOG.md
git commit -m "chore: Bump version to 0.3.0"
git push origin main

# 4. Create a GitHub Release
# Go to: https://github.com/lawaloy/stock-exchange-tracker/releases/new
# - Tag: v0.3.0
# - Title: v0.3.0 - Your Release Name
# - Description: Copy from CHANGELOG.md
# - Click "Publish release"

# 5. Done! GitHub Actions will:
#    ✅ Run tests
#    ✅ Build package
#    ✅ Publish to PyPI automatically
```

### Manual Trigger (Test Publishing)

You can also trigger publishing manually:

1. Go to Actions → "Publish to PyPI"
2. Click "Run workflow"
3. Choose environment:
   - `testpypi` - Test your package first
   - `pypi` - Publish to production

### Monitoring

Watch the GitHub Actions run:

1. Go to the "Actions" tab
2. Click on the latest "Publish to PyPI" workflow
3. Monitor progress:
   - ✅ Test: Runs pytest
   - ✅ Build: Creates distribution files
   - ✅ Publish: Uploads to PyPI

If any step fails, the workflow stops (package won't be published).

---

## Option 2: Manual Publishing

If you prefer manual control:

### Prerequisites

```bash
pip install build twine
```

### Release Steps

```bash
# 1. Ensure you're on main and up to date
git checkout main
git pull origin main

# 2. Update version in setup.cfg
# Change version = 0.2.0 to version = 0.3.0

# 3. Update CHANGELOG.md
# Add new version section with changes

# 4. Commit version bump
git add setup.cfg CHANGELOG.md
git commit -m "chore: Bump version to 0.3.0"
git push origin main

# 5. Create and push tag
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0

# 6. Clean previous builds
rm -rf dist/ build/ *.egg-info

# 7. Run tests
pytest tests/ -v

# 8. Build package
python -m build

# 9. Check the build
twine check dist/*

# 10. Upload to Test PyPI (optional but recommended)
python -m twine upload --repository testpypi dist/*

# 11. Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ stock-exchange-tracker

# 12. If all good, upload to PyPI
python -m twine upload dist/*

# 13. Create GitHub Release
# Go to: https://github.com/lawaloy/stock-exchange-tracker/releases/new
# - Select tag: v0.3.0
# - Add release notes from CHANGELOG.md
# - Publish
```

---

## Semantic Versioning

Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **PATCH** (0.2.0 → 0.2.1): Bug fixes, no new features
- **MINOR** (0.2.0 → 0.3.0): New features, backward compatible
- **MAJOR** (0.2.0 → 1.0.0): Breaking changes

### Examples

```text
0.2.1 - Fix projection calculation bug
0.3.0 - Add new technical indicators
1.0.0 - Stable API, change CLI interface
```

---

## Pre-release Versions

For beta testing:

```text
0.3.0b1 - Beta 1
0.3.0rc1 - Release candidate 1
```

Update `setup.cfg`:

```ini
version = 0.3.0b1
```

Users install with:

```bash
pip install --pre stock-exchange-tracker
```

---

## Hotfix Process

For urgent fixes to production:

```bash
# 1. Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-bug

# 2. Fix the bug
# ... make changes ...

# 3. Update version (patch bump)
# 0.2.0 → 0.2.1

# 4. Update CHANGELOG.md

# 5. Commit and push
git add .
git commit -m "fix: Critical bug description"
git push origin hotfix/critical-bug

# 6. Create PR and merge to main

# 7. Create release v0.2.1
# (Automated workflow will publish)
```

---

## Checklist for Each Release

Before creating a release:

- [ ] All tests pass locally: `pytest tests/ -v`
- [ ] Markdown files are clean: `python scripts/check_markdown.py`
- [ ] Version updated in `setup.cfg`
- [ ] `CHANGELOG.md` updated with changes
- [ ] Changes merged to `main` branch
- [ ] Git tag created: `git tag -a v0.X.0 -m "..."`
- [ ] Tag pushed: `git push origin v0.X.0`
- [ ] GitHub Release created with notes
- [ ] (Automated) Wait for GitHub Actions to complete
- [ ] (Manual) Package built and uploaded to PyPI
- [ ] Verify installation: `pip install --upgrade stock-exchange-tracker`
- [ ] Test CLI: `stock-tracker --version`

---

## Troubleshooting

### "Version already exists on PyPI"

You cannot replace a published version. You must:

1. Increment version number
2. Publish new version

### "Tests failed in CI"

Fix tests before publishing:

1. Run tests locally: `pytest tests/ -v`
2. Fix failing tests
3. Push fixes
4. Re-run release process

### "Upload failed - authentication error"

For automated publishing:

1. Check `PYPI_API_TOKEN` is set in GitHub Secrets
2. Verify token hasn't expired
3. Ensure token has correct permissions

For manual publishing:

1. Check `~/.pypirc` configuration
2. Verify credentials
3. Generate new API token if needed

### "Package import error after installation"

1. Check `MANIFEST.in` includes all necessary files
2. Verify `setup.cfg` package configuration
3. Test locally: `pip install -e .`

---

## Rollback

If you publish a broken version:

### Option 1: Yank the Release

"Yanking" marks the version as broken (doesn't delete it):

1. Go to PyPI project page
2. Manage → Releases
3. Click "Yank" on the broken version
4. Users won't install it by default

### Option 2: Publish a Fixed Version

Immediately publish a patch:

```bash
# If 0.3.0 is broken
# Publish 0.3.1 with fix

# Update version to 0.3.1
python -m build
python -m twine upload dist/*
```

---

## Best Practices

1. **Always test on TestPyPI first** (for manual releases)
2. **Write good release notes** - users read them!
3. **Keep CHANGELOG.md up to date** - before each release
4. **Use semantic versioning** - helps users understand impact
5. **Tag releases in Git** - creates clear history
6. **Automate when possible** - reduces human error
7. **Test installation** - before announcing release
8. **Announce releases** - README, discussions, social media

---

## Release Cadence

Suggested schedule:

- **Patch releases**: As needed (bug fixes)
- **Minor releases**: Monthly or when features are ready
- **Major releases**: Quarterly or for significant changes

---

## Questions?

- Check [PUBLISHING.md](../PUBLISHING.md) for detailed PyPI setup
- Review [CHANGELOG.md](../CHANGELOG.md) for version history
- See [GitHub Actions docs](https://docs.github.com/en/actions) for workflow help
