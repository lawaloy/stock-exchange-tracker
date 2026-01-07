# PyPI Publishing Action Plan

This document outlines the complete workflow for publishing your Stock Exchange Tracker to PyPI.

## 📋 Overview

**Branch:** `feature/pypi-publishing`
**Goal:** Set up automated publishing to PyPI
**Time Required:** ~20 minutes (one-time setup)

---

## Part 1: What YOU Need to Do (One-Time Setup)

These are actions only you can perform:

### ✅ Step 1: Update Author Email (2 minutes)

**File:** `setup.cfg`

**Action Required:**

1. Open `setup.cfg`
2. Line 8: Change `author_email = your.email@example.com`
3. Replace with your actual email address
4. Save the file

**Why?** PyPI requires a valid contact email for package publishers.

**Status:** ⏳ Waiting for your update

---

### ✅ Step 2: Create PyPI Account (5 minutes)

**Action Required:**

1. Go to: <https://pypi.org/account/register/>
2. Fill in:
   - Username (choose wisely - this is public)
   - Email (use the same one from setup.cfg)
   - Password (use a strong password)
3. Check your email and verify your account
4. Log in to confirm it works

**Why?** You need an account to publish packages to PyPI.

**Status:** ⏳ Waiting for you to create account

---

### ✅ Step 3: Generate PyPI API Token (3 minutes)

**Action Required:**

1. Log in to PyPI: <https://pypi.org/manage/account/>
2. Scroll to **"API tokens"** section
3. Click **"Add API token"**
4. Fill in:
   - **Token name:** `GitHub Actions - stock-exchange-tracker`
   - **Scope:** "Entire account" (will scope to project later)
5. Click **"Add token"**
6. **CRITICAL:** Copy the token immediately
   - It starts with `pypi-` and is very long
   - You can only see it ONCE
   - Save it temporarily in a secure place (password manager)

**Why?** GitHub Actions needs this token to publish on your behalf.

**Status:** ⏳ Waiting for you to generate token

---

### ✅ Step 4: Add Token to GitHub Secrets (2 minutes)

**Action Required:**

1. Go to: <https://github.com/lawaloy/stock-exchange-tracker/settings/secrets/actions>
2. Click **"New repository secret"** (green button)
3. Fill in:
   - **Name:** `PYPI_API_TOKEN` (exactly this, case-sensitive)
   - **Secret:** Paste the token you just copied
4. Click **"Add secret"**
5. Verify `PYPI_API_TOKEN` appears in your secrets list

**Why?** This securely stores your credentials so GitHub can auto-publish.

**Status:** ⏳ Waiting for you to add secret

---

### ✅ Step 5: Review & Merge Publishing Branch (5 minutes)

**Action Required:**

1. Review the changes in this branch:
   - Check `PUBLISHING.md` for detailed publishing guide
   - Check `AUTOMATION_SETUP_CHECKLIST.md` for setup steps
   - Check `.github/workflows/publish.yml` for automation workflow
   - Check `setup.cfg` has correct information

2. When satisfied, create a Pull Request:
   - Go to: <https://github.com/lawaloy/stock-exchange-tracker/compare/feature/pypi-publishing>
   - Click "Create pull request"
   - Review the changes
   - Merge to `main`

**Why?** Publishing infrastructure should be in main branch.

**Status:** ⏳ Waiting for you to review and merge

---

### ✅ Step 6: Create Your First Release (3 minutes)

**Action Required:**

1. After merging, go to: <https://github.com/lawaloy/stock-exchange-tracker/releases/new>

2. Fill in:
   - **Tag:** `v0.2.0` (create new tag on publish)
   - **Title:** `v0.2.0 - Stock Projections & Recommendations`
   - **Description:** Copy from `CHANGELOG.md`

3. Check **"Set as the latest release"**

4. Click **"Publish release"**

**Why?** This triggers the automated publishing workflow.

**Status:** ⏳ Waiting for you to create release

---

### ✅ Step 7: Monitor the Workflow (5 minutes)

**Action Required:**

1. Go to: <https://github.com/lawaloy/stock-exchange-tracker/actions>
2. Click on the running "Publish to PyPI" workflow
3. Watch the progress:
   - ✅ Test job (runs pytest)
   - ✅ Build job (creates package)
   - ✅ Publish job (uploads to PyPI)
4. Wait for all jobs to complete (~3-5 minutes)

**If it fails:**

- Check the error logs
- Common issues in Troubleshooting section below
- Fix the issue and create a new release with v0.2.1

**Why?** Ensure everything works correctly.

**Status:** ⏳ Will run after you create release

---

### ✅ Step 8: Verify & Test (3 minutes)

**Action Required:**

1. Check PyPI: <https://pypi.org/project/stock-exchange-tracker/>
   - Your package should be visible!

2. Test installation in a fresh environment:

```bash
# Open a NEW terminal (not in your project)
pip install stock-exchange-tracker

# Verify version
stock-tracker --version
# Should show: 0.2.0

# Test basic functionality
stock-tracker --help
```

1. Celebrate! 🎉

**Why?** Confirm users can actually install your package.

**Status:** ⏳ After successful publish

---

## Part 2: What's AUTOMATED (No Action Needed)

These happen automatically when you create a release:

### 🤖 Automated Testing

- Runs all pytest tests
- Checks markdown linting
- Validates code quality
- **If tests fail:** Publishing stops (safe!)

### 🤖 Automated Building

- Creates source distribution (.tar.gz)
- Creates wheel distribution (.whl)
- Validates package structure
- Checks metadata

### 🤖 Automated Publishing

- Uploads to PyPI
- Makes package available worldwide
- Updates package page
- **If upload fails:** You'll see error in Actions

### 🤖 Automated Notifications

- GitHub shows success/failure
- You'll see the release in your repository
- Package appears on PyPI within minutes

---

## Part 3: Future Releases (After First Setup)

Once setup is complete, releasing new versions is simple:

### For Bug Fixes (0.2.0 → 0.2.1)

```bash
# 1. Make fixes on a feature branch
git checkout -b fix/bug-description
# ... make changes ...
git commit -am "fix: Description"
git push

# 2. Create PR and merge to main

# 3. Update version
# In setup.cfg: version = 0.2.1

# 4. Commit version bump
git add setup.cfg
git commit -m "chore: Bump version to 0.2.1"
git push

# 5. Create GitHub Release
# Tag: v0.2.1
# Title: v0.2.1 - Bug Fixes
# Description: What was fixed

# 6. Done! Auto-published 🎉
```

### For New Features (0.2.0 → 0.3.0)

```bash
# 1. Develop feature on a feature branch
git checkout -b feature/new-feature
# ... make changes ...
git commit -am "feat: New feature"
git push

# 2. Create PR and merge to main

# 3. Update version
# In setup.cfg: version = 0.3.0

# 4. Commit version bump
git add setup.cfg
git commit -m "chore: Bump version to 0.3.0"
git push

# 5. Create GitHub Release
# Tag: v0.3.0
# Title: v0.3.0 - Feature Name
# Description: What's new

# 6. Done! Auto-published 🎉
```

---

## Part 4: Testing Before Production (Optional)

To test publishing without affecting production:

### Set Up TestPyPI (One-Time)

1. Create account: <https://test.pypi.org/account/register/>
2. Generate API token (same as PyPI)
3. Add to GitHub Secrets as: `TEST_PYPI_API_TOKEN`

### Test a Release

1. Go to: <https://github.com/lawaloy/stock-exchange-tracker/actions>
2. Click **"Publish to PyPI"**
3. Click **"Run workflow"**
4. Select: **testpypi**
5. Watch it run

6. Test install:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ stock-exchange-tracker
```

1. If successful, publish to production PyPI!

---

## Troubleshooting Guide

### Issue: "Workflow didn't trigger"

**Cause:** Release wasn't created properly

**Solution:**

- Ensure you created a **Release**, not just a tag
- Workflow only triggers on release publication
- Check: <https://github.com/lawaloy/stock-exchange-tracker/actions>

### Issue: "Tests failed in CI"

**Cause:** Code has failing tests

**Solution:**

```bash
# Run tests locally first
pytest tests/ -v

# Fix any failures
# Then create new release
```

### Issue: "Publish failed - 403 Forbidden"

**Cause:** Authentication problem

**Solution:**

- Check `PYPI_API_TOKEN` is set in GitHub Secrets
- Verify token hasn't expired
- Regenerate token if needed
- Ensure token has correct permissions

### Issue: "Version 0.2.0 already exists"

**Cause:** Can't republish same version

**Solution:**

- Update `setup.cfg`: `version = 0.2.1`
- Commit and create new release: `v0.2.1`

### Issue: "Package name taken"

**Cause:** `stock-exchange-tracker` already exists on PyPI

**Solution:**

1. Choose different name: `stock-tracker-{yourusername}`
2. Update `setup.cfg`: `name = new-name`
3. Try publishing again

### Issue: "Import error after install"

**Cause:** Package structure issue

**Solution:**

- Check `MANIFEST.in` includes all files
- Verify `setup.cfg` package configuration
- Test locally: `pip install -e .`

---

## Important Files Reference

| File | Purpose | Action |
|------|---------|--------|
| `setup.cfg` | Package metadata | Update email address |
| `.github/workflows/publish.yml` | Auto-publish workflow | Review (no change needed) |
| `CHANGELOG.md` | Version history | Update for each release |
| `MANIFEST.in` | Files to include | Review (no change needed) |
| `PUBLISHING.md` | Detailed guide | Reference documentation |
| `AUTOMATION_SETUP_CHECKLIST.md` | Quick checklist | Follow steps |

---

## Quick Checklist Summary

Use this as your guide:

- [ ] Update email in `setup.cfg`
- [ ] Create PyPI account
- [ ] Generate PyPI API token
- [ ] Add token to GitHub Secrets
- [ ] Review this publishing branch
- [ ] Merge to main via PR
- [ ] Create GitHub Release (v0.2.0)
- [ ] Monitor workflow execution
- [ ] Verify package on PyPI
- [ ] Test installation
- [ ] 🎉 Done!

---

## Next Steps After Publishing

1. **Update README.md:**
   - Add installation instructions
   - Add PyPI badge
   - Link to package page

2. **Announce:**
   - Social media
   - Dev communities
   - GitHub discussions

3. **Monitor:**
   - PyPI download statistics
   - GitHub issues
   - User feedback

4. **Plan next release:**
   - Collect feature requests
   - Fix reported bugs
   - Improve documentation

---

## Support & Help

- **Publishing Issues:** Check `PUBLISHING.md`
- **Release Process:** Check `docs/RELEASE_PROCESS.md`
- **Package Info:** Check `PACKAGE_SUMMARY.md`
- **GitHub Actions:** <https://docs.github.com/en/actions>
- **PyPI Help:** <https://pypi.org/help/>

---

## Time Estimate

| Task | Time |
|------|------|
| One-time setup | ~15-20 min |
| First release | ~10 min |
| Future releases | ~3-5 min |

**Total first-time:** ~30 minutes
**Future releases:** ~5 minutes each (mostly automated!)

---

**Remember:** After the first setup, releasing is just:

1. Create feature branch → Make changes → Merge PR
2. Update version number
3. Create GitHub Release
4. ☕ Wait 5 minutes while it auto-publishes!

You've got this! 💪
