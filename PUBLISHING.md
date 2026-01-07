# Publishing Guide for Stock Exchange Tracker

This guide walks through publishing the package to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing)
   - [PyPI](https://pypi.org/account/register/) (for production)

2. **Install Publishing Tools**:

```bash
pip install --upgrade build twine
```

1. **Update Your Information**:
   - Edit `setup.cfg` and replace `your.email@example.com` with your actual email
   - Verify all URLs and metadata are correct

## Step 1: Prepare the Package

### 1.1 Version Update

Update version in `setup.cfg` following [Semantic Versioning](https://semver.org/):

- **Patch** (0.2.0 → 0.2.1): Bug fixes
- **Minor** (0.2.0 → 0.3.0): New features (backward compatible)
- **Major** (0.2.0 → 1.0.0): Breaking changes

### 1.2 Update CHANGELOG.md

Document all changes in `CHANGELOG.md`.

### 1.3 Verify Package Contents

Check what will be included:

```bash
python setup.py check
```

## Step 2: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build
```

This creates:

- `dist/stock-exchange-tracker-0.2.0.tar.gz` (source distribution)
- `dist/stock_exchange_tracker-0.2.0-py3-none-any.whl` (wheel)

## Step 3: Test on TestPyPI (Recommended)

### 3.1 Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for your TestPyPI credentials.

### 3.2 Test Installation

```bash
# In a new virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ stock-exchange-tracker

# Test the CLI
stock-tracker --help
stock-tracker run
```

## Step 4: Publish to PyPI (Production)

Once testing is successful:

```bash
python -m twine upload dist/*
```

You'll be prompted for your PyPI credentials.

## Step 5: Verify Installation

```bash
# In a fresh environment
pip install stock-exchange-tracker

# With AI features
pip install stock-exchange-tracker[ai]

# With development tools
pip install stock-exchange-tracker[dev]

# Everything
pip install stock-exchange-tracker[all]
```

## Step 6: Tag the Release

```bash
git tag -a v0.2.0 -m "Release version 0.2.0 - Stock Projections"
git push origin v0.2.0
```

## Step 7: Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select the tag you just created
4. Add release notes from CHANGELOG.md
5. Publish release

## Using API Tokens (Recommended)

For security, use API tokens instead of passwords:

### PyPI Token Setup

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Generate an API token
3. Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

Then upload with:

```bash
python -m twine upload dist/*
```

## Package Naming Considerations

- **PyPI name**: `stock-exchange-tracker` (with hyphens)
- **Import name**: `from src.cli.commands import main`
- **CLI command**: `stock-tracker`

## Important Notes

### What Gets Included

The `MANIFEST.in` file controls what's packaged:

- ✅ Source code (`src/`)
- ✅ Configuration files (`config/`)
- ✅ Documentation (`README.md`, `LICENSE`, `docs/`)
- ✅ Tests (`tests/`)
- ❌ Data files (`data/`)
- ❌ Log files (`logs/`)
- ❌ Environment files (`.env`)

### API Keys

Users will need their own Finnhub API key. Make sure:

- The README clearly explains this requirement
- `.env.example` is provided as a template
- The package gracefully handles missing keys

### Optional Dependencies

OpenAI is now optional:

```bash
# Basic installation (no AI summaries)
pip install stock-exchange-tracker

# With AI summaries
pip install stock-exchange-tracker[ai]
```

## Maintenance

### Updating the Package

1. Make changes
2. Update version in `setup.cfg`
3. Update `CHANGELOG.md`
4. Build: `python -m build`
5. Test on TestPyPI
6. Upload to PyPI
7. Tag the release

### Yanking a Release

If you published a broken version:

```bash
# This doesn't delete but marks it as broken
pip install twine
twine upload --repository pypi --skip-existing dist/*
```

Or use the PyPI web interface to "yank" the release.

## Troubleshooting

### "Package already exists"

You cannot replace a published version. Increment the version number.

### "Invalid credentials"

- Verify username/token
- Check `~/.pypirc` configuration
- For tokens, username should be `__token__`

### "Missing files in distribution"

Check `MANIFEST.in` and rebuild.

### "Import errors after installation"

Verify package structure and `setup.cfg` `packages` configuration.

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## Quick Reference

```bash
# Complete publishing workflow
git checkout main
git pull origin main

# Update version in setup.cfg
# Update CHANGELOG.md

# Build
rm -rf dist/ build/ *.egg-info
python -m build

# Test
python -m twine upload --repository testpypi dist/*
# ... test installation ...

# Publish
python -m twine upload dist/*

# Tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# Create GitHub release
```

## Support

For issues with:

- **Package functionality**: [GitHub Issues](https://github.com/lawaloy/stock-exchange-tracker/issues)
- **Publishing process**: [PyPI Support](https://pypi.org/help/)
- **Build system**: [setuptools documentation](https://setuptools.pypa.io/)
