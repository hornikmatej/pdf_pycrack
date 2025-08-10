# Publishing Guide

This document outlines the process for publishing pdf-pycrack to PyPI and creating GitHub releases.

## Prerequisites

Before you can publish to PyPI, you need to:

1. **Create a PyPI account**: Sign up at https://pypi.org/account/register/
2. **Configure trusted publishing** (recommended):
   - Go to https://pypi.org/manage/account/publishing/
   - Click "Add a new pending publisher"
   - Fill in:
     - PyPI project name: `pdf-pycrack`
     - Owner: `hornikmatej`
     - Repository name: `pdf_pycrack`
     - Workflow name: `publish.yml`
     - Environment name: (leave blank)

## Publishing Process

### Automated Release (Recommended)

1. **Run the release script**:
   ```bash
   ./release.sh
   ```

   This script will:
   - Verify you're on the main branch
   - Check that working directory is clean
   - Pull latest changes
   - Run all tests
   - Build the package locally
   - Create and push the git tag `v0.1.0`

2. **Monitor the GitHub Actions workflow**:
   - Go to: https://github.com/hornikmatej/pdf_pycrack/actions
   - The publish workflow will automatically trigger when the tag is pushed
   - The workflow will run tests and publish to PyPI

### Manual Process

If you prefer to do it manually:

1. **Ensure working directory is clean**:
   ```bash
   git status
   ```

2. **Run tests**:
   ```bash
   uv run pytest
   ```

3. **Build package locally**:
   ```bash
   uv build
   ```

4. **Create and push tag**:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

## After Publishing

1. **Verify on PyPI**: Check that your package appears at https://pypi.org/project/pdf-pycrack/
2. **Test installation**: Try installing from PyPI:
   ```bash
   pip install pdf-pycrack
   pdf-pycrack --help
   ```
3. **Update documentation**: Update any installation instructions in README or docs

## GitHub Release

The GitHub Actions workflow will automatically create a GitHub release with:
- Release notes
- Source code archives
- Built wheel and source distribution files

You can enhance the release by:
- Adding detailed release notes
- Uploading additional assets
- Marking as pre-release if needed

## Troubleshooting

### Common Issues

1. **PyPI project name already taken**: Try a different name or contact PyPI support
2. **Trusted publishing not configured**: Set up trusted publishing as described above
3. **Tests failing**: Fix all test failures before publishing
4. **Permission denied**: Ensure you have the correct repository permissions

### Checking Build

If the build fails, you can check locally:

```bash
uv build
twine check dist/*
```

### Cleaning Build Artifacts

If you need to start fresh:

```bash
rm -rf dist/ build/ src/*.egg-info
```

## Security Best Practices

- Use trusted publishing instead of API tokens when possible
- Never commit API tokens to the repository
- Regularly rotate any API tokens
- Monitor PyPI downloads and security advisories

## Version Management

- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `pyproject.toml` before releasing
- Create meaningful git tags and release notes
- Consider using automated version bumping tools for future releases
