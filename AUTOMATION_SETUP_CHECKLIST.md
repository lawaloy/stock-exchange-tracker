# Automated Publishing Setup Checklist

Follow these steps to enable automated PyPI publishing for your Stock Exchange Tracker.

## ✅ Completed

- [x] Merge feature branch to main
- [x] GitHub Actions workflow created (`.github/workflows/publish.yml`)
- [x] Documentation created (`docs/RELEASE_PROCESS.md`)

## 🔧 To Complete (Takes ~5 minutes)

### Step 2: Update Your Email in setup.cfg

**Why?** PyPI requires a contact email for published packages.

**Action:**

1. Open `setup.cfg`
2. Find line 8:

```ini
author_email = your.email@example.com
```

1. Replace with your actual email
2. Save, commit, and push:

```bash
git add setup.cfg
git commit -m "chore: Update author email"
git push origin main
```

---

### Step 3: Create PyPI Account

**Why?** You need an account to publish packages.

**Action:**

1. Go to: <https://pypi.org/account/register/>
2. Fill in:
   - Username
   - Email
   - Password
3. Verify your email (check inbox)
4. ✅ Account created!

---

### Step 4: Generate PyPI API Token

**Why?** GitHub needs this token to publish on your behalf.

**Action:**

1. Log in to PyPI: <https://pypi.org/manage/account/>
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Fill in:
   - **Token name**: `GitHub Actions - stock-exchange-tracker`
   - **Scope**: Select "Entire account" *(you can scope it to just this project after first publish)*
5. Click "Add token"
6. **IMPORTANT**: Copy the token immediately (starts with `pypi-`)
   - It looks like: `pypi-AgEIcHlwaS5vcmc...` (very long)
   - You can only see it once!
   - Keep it safe for the next step

---

### Step 5: Add Token to GitHub Secrets

**Why?** Securely stores your token so GitHub Actions can use it.

**Action:**

1. Go to your repository: <https://github.com/lawaloy/stock-exchange-tracker>
2. Click **Settings** (top menu)
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **"New repository secret"** (green button)
5. Fill in:
   - **Name**: `PYPI_API_TOKEN` (exactly this, case-sensitive)
   - **Secret**: Paste the token you copied (the long `pypi-...` string)
6. Click **"Add secret"**
7. ✅ You should now see `PYPI_API_TOKEN` in your secrets list

---

### Step 6: Create Your First Release

**Why?** This triggers the automated publishing workflow!

**Action:**

1. Go to: <https://github.com/lawaloy/stock-exchange-tracker/releases/new>

2. Fill in the release form:

   **Choose a tag:**
   - Click "Choose a tag"
   - Type: `v0.2.0`
   - Click "Create new tag: v0.2.0 on publish"

   **Release title:**

```text
   v0.2.0 - Stock Projections & Recommendations
```

   **Description:** (copy and paste this)

```markdown
   ## What's New in v0.2.0

   ### 🚀 Major Features

   - **Stock Projection System**: 5-day price forecasts with technical analysis
   - **AI-Powered Recommendations**: STRONG BUY to STRONG SELL ratings
   - **Risk Assessment**: Confidence scores and risk levels (Low/Medium/High)
   - **Beautiful Reports**: Human-readable Markdown reports for product teams

   ### 📊 Technical Enhancements

   - Momentum and volatility calculations
   - Trend classification (Bullish/Neutral/Bearish)
   - Price targets (High/Mid/Low)
   - Enhanced CLI with projection summaries

   ### 🧪 Quality Improvements

   - Comprehensive test suite for projections
   - Markdown linting for documentation quality
   - Automated quality checks

   ### 📦 Package Improvements

   - Made OpenAI dependency optional (`pip install stock-exchange-tracker[ai]`)
   - Professional PyPI metadata
   - Automated publishing workflow

   ### 📚 Documentation

   - Stock Projections technical guide
   - Publishing guide
   - Release process documentation

   ## Installation

   ```bash
   # Basic installation
   pip install stock-exchange-tracker

   # With AI summaries
   pip install stock-exchange-tracker[ai]
   ```

## Usage

   ```bash
   stock-tracker run
   ```

   See the [README](https://github.com/lawaloy/stock-exchange-tracker#readme) for full documentation.

## Breaking Changes

   None - fully backward compatible with v0.1.0

## Contributors

- @lawaloy

   ---

   **Full Changelog**: <https://github.com/lawaloy/stock-exchange-tracker/compare/v0.1.0...v0.2.0>

1. Check "Set as the latest release"

1. Click **"Publish release"** (green button)

1. ✅ **Release published!**

---

### Step 7: Watch the Magic Happen 🎉

**Action:**

1. Go to: <https://github.com/lawaloy/stock-exchange-tracker/actions>
2. You should see "Publish to PyPI" workflow running
3. Click on it to watch progress:
   - ⏳ Test (runs pytest)
   - ⏳ Build (creates package)
   - ⏳ Publish (uploads to PyPI)
4. Wait ~3-5 minutes
5. ✅ All steps should show green checkmarks

If any step fails, check the logs and see troubleshooting below.

---

### Step 8: Verify It Worked

**Action:**

```bash
# In a NEW terminal (not your project directory)
pip install stock-exchange-tracker

# Check version
stock-tracker --version
# Should show: 0.2.0 or similar

# Test it
stock-tracker --help
```

1. Check PyPI: <https://pypi.org/project/stock-exchange-tracker/>
   - Your package should be live!

---

## 🎉 Success! You're Done

Your package is now:

- ✅ Published on PyPI
- ✅ Installable via `pip install stock-exchange-tracker`
- ✅ Automatically published on future releases

## Future Releases (Now Super Easy!)

For all future updates:

```bash
# 1. Update version in setup.cfg
version = 0.3.0

# 2. Update CHANGELOG.md with changes

# 3. Commit and push
git add setup.cfg CHANGELOG.md
git commit -m "chore: Bump version to 0.3.0"
git push origin main

# 4. Create GitHub Release (same as Step 6 above)
# - Tag: v0.3.0
# - Title and description with changes

# 5. Done! 🎉 GitHub auto-publishes
```

---

## Troubleshooting

### "Workflow didn't trigger"

- Check you created a **Release**, not just a tag
- Workflow only runs on release publication

### "Publish step failed - 403 Forbidden"

- Check `PYPI_API_TOKEN` is set correctly in GitHub Secrets
- Verify token hasn't expired
- Regenerate token if needed

### "Version already exists"

- You can't republish the same version
- Increment version in `setup.cfg` and create new release

### "Tests failed"

Fix the failing tests before publishing:

```bash
pytest tests/ -v
```

Once fixed, create a new release with bumped version.

### "Package name taken"

If `stock-exchange-tracker` is already taken on PyPI:

1. Choose a different name (e.g., `stock-tracker-pro`)
2. Update `setup.cfg`: `name = your-new-name`
3. Try publishing again

### Still stuck?

Check the detailed guide: `docs/RELEASE_PROCESS.md`

---

## Optional: Set Up TestPyPI

For testing releases before production:

1. Create account: <https://test.pypi.org/account/register/>
2. Generate API token
3. Add to GitHub Secrets as `TEST_PYPI_API_TOKEN`
4. Manually trigger workflow:
   - Actions → "Publish to PyPI" → "Run workflow"
   - Choose "testpypi"

---

## Next Steps

After your first release is live:

1. **Update README** with installation instructions
2. **Share your package**:
   - Social media
   - Dev communities
   - GitHub discussions
3. **Gather feedback** from users
4. **Plan v0.3.0** features!

---

## Quick Reference

| What                | Where                                                                |
|---------------------|----------------------------------------------------------------------|
| **Package on PyPI** | <https://pypi.org/project/stock-exchange-tracker/>                  |
| **GitHub Releases** | <https://github.com/lawaloy/stock-exchange-tracker/releases>        |
| **GitHub Actions**  | <https://github.com/lawaloy/stock-exchange-tracker/actions>         |
| **PyPI Account**    | <https://pypi.org/manage/account/>                                  |
| **Repo Settings**   | <https://github.com/lawaloy/stock-exchange-tracker/settings>        |

---

**You've got this! 💪 The setup is straightforward, and future releases will be a breeze.**

Questions? Check `PUBLISHING.md` or `docs/RELEASE_PROCESS.md` for more details.
