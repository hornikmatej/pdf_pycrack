# Release Process

This document outlines the release process for PDF-PyCrack.

## Automated Release Process

PDF-PyCrack uses an automated release process through GitHub Actions. When a version tag is pushed, the following happens automatically:

1. **Continuous Integration**: All tests are run across Python 3.12 and 3.13
2. **Code Quality Checks**: Pre-commit hooks are executed to ensure code quality
3. **Package Building**: The package is built and verified using `uv build`
4. **PyPI Publication**: The package is automatically published to PyPI using trusted publishing
5. **GitHub Release Creation**: A comprehensive GitHub release is created with detailed release notes

## Creating a Release

To create a new release:

1. **Update Version**: Update the version in `pyproject.toml`
2. **Update Documentation**: Ensure README.md and other docs are up to date
3. **Run Tests**: Make sure all tests pass locally
4. **Create Tag**: Use the existing `release.sh` script or create a tag manually:
   ```bash
   git tag -a "v1.0.1" -m "Release v1.0.1"
   git push origin "v1.0.1"
   ```

## Release Notes

The GitHub Actions workflow automatically generates comprehensive release notes that include:

### Key Sections
- **Key Features**: Highlighting main functionality
- **Technical Highlights**: Architecture and implementation details
- **Installation Instructions**: Multiple installation methods
- **Usage Examples**: Both CLI and library usage
- **Performance Information**: Benchmarking and optimization details
- **Development Features**: Build system and code quality tools
- **Use Cases**: Target scenarios and applications
- **Future Roadmap**: Planned improvements and features

### Feature Categories Covered
- Multi-core processing capabilities
- Memory optimization and efficiency
- Comprehensive error handling
- PyPI package availability
- Rich terminal output and progress tracking
- Extensive testing and validation
- Modern Python support (3.12+)
- Development and build tooling

## Workflow Details

The release workflow (`.github/workflows/publish.yml`) includes:

- **Permissions**: `contents: write` for creating releases, `id-token: write` for PyPI trusted publishing
- **Testing Matrix**: Python 3.12 and 3.13 across Ubuntu latest
- **Dependencies**: Automatic caching and installation via `uv`
- **Security**: Uses trusted publishing instead of API tokens
- **Verification**: Package contents are verified before publishing

## Manual Release Creation

If you need to create a release manually (not recommended):

1. Go to the [GitHub Releases page](https://github.com/hornikmatej/pdf_pycrack/releases)
2. Click "Draft a new release"
3. Select the existing tag (e.g., `v0.1.0`)
4. Use the comprehensive release notes template from the workflow
5. Publish the release

## Troubleshooting

### Common Issues

**Workflow Fails on PyPI Upload:**
- Ensure trusted publishing is configured in PyPI project settings
- Verify the workflow has the correct permissions

**Release Creation Fails:**
- Check that `contents: write` permission is set
- Ensure the tag exists before the workflow runs
- Verify GITHUB_TOKEN has sufficient permissions

**Tests Fail During Release:**
- All tests must pass before release creation
- Fix any failing tests and re-tag if necessary

### Validation

After a successful release:
- ✅ Check the [PyPI package page](https://pypi.org/project/pdf-pycrack/)
- ✅ Verify the GitHub release appears with correct notes
- ✅ Test installation from PyPI: `pip install pdf-pycrack`
- ✅ Confirm version number matches across PyPI and GitHub

## Security Considerations

- Uses trusted publishing for PyPI (more secure than API tokens)
- No secrets stored in repository
- Automated workflow reduces human error
- Package verification before publishing
- Signed releases and attestations when supported