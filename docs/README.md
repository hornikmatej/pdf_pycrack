# PDF-PyCrack Documentation

This directory contains the complete documentation for PDF-PyCrack, built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## 📚 Documentation Structure

- **Getting Started**: Installation, quick start, and basic usage
- **User Guide**: Comprehensive CLI and Python library documentation
- **Performance**: Benchmarking and optimization guides
- **API Reference**: Detailed API documentation (auto-generated)
- **Development**: Contributing, testing, and release information

## 🚀 Quick Start

### Prerequisites

Make sure you have the documentation dependencies installed:

```bash
uv sync  # Installs all dependencies including docs
```

### Local Development

Start the local documentation server:

```bash
uv run mkdocs serve
```

This will start a local server at `http://127.0.0.1:8000/pdf_pycrack/` with live reload.

### Building Static Site

Generate the static documentation site:

```bash
uv run mkdocs build
```

The built site will be in the `site/` directory.

## 📝 Contributing to Documentation

### Writing Guidelines

1. **Use clear, concise language**
2. **Include practical examples**
3. **Add code snippets** with proper syntax highlighting
4. **Use admonitions** for tips, warnings, and notes
5. **Cross-reference** related sections

### Markdown Extensions

The documentation uses several Markdown extensions:

- **Code highlighting**: ` ```python ` for syntax highlighting
- **Tabbed content**: ` === "Tab Name" ` for multiple options
- **Admonitions**: ` !!! tip "Title" ` for callouts
- **Mermaid diagrams**: ` ```mermaid ` for flowcharts

### Examples

#### Code Tabs

```markdown
=== "CLI"
    ```bash
    pdf-pycrack file.pdf --cores 4
    ```

=== "Python"
    ```python
    crack_pdf_password("file.pdf", num_processes=4)
    ```
```

#### Admonitions

```markdown
!!! tip "Performance Tip"
    Use specific character sets to reduce search space.

!!! warning "Important"
    Always ensure you have permission to crack the PDF.

!!! note "Note"
    Results may vary based on hardware.
```

## 🏗️ Documentation Architecture

### File Organization

```
docs/
├── index.md                    # Homepage
├── getting-started/
│   ├── installation.md         # Installation guide
│   ├── quickstart.md          # Quick start tutorial
│   └── basic-usage.md         # Basic usage patterns
├── user-guide/
│   ├── cli.md                 # Command-line interface
│   ├── library.md             # Python library
│   ├── configuration.md       # Configuration guide
│   └── error-handling.md      # Error handling (TBD)
├── performance/
│   ├── benchmarking.md        # Benchmarking guide
│   └── optimization.md        # Optimization tips (TBD)
├── api/
│   ├── core.md               # Core API reference (TBD)
│   ├── models.md             # Data models (TBD)
│   └── cli.md                # CLI API (TBD)
└── development/
    ├── contributing.md        # Contribution guide (TBD)
    ├── testing.md            # Testing guide (TBD)
    └── releases.md           # Release notes (TBD)
```

### MkDocs Configuration

The documentation is configured in `mkdocs.yml`:

- **Theme**: Material with custom colors and features
- **Plugins**: Search and auto-generated API docs
- **Extensions**: Code highlighting, tabs, admonitions
- **Navigation**: Organized by user journey

## 🎨 Styling and Themes

### Color Scheme

- **Primary**: Red (matching the security/cracking theme)
- **Accent**: Red
- **Light/Dark**: Both modes supported

### Custom Features

- Navigation tabs and sections
- Code copy buttons
- Search functionality
- Edit/view links to GitHub
- Social links

## 📊 Documentation Metrics

### Completeness Status

- ✅ **Getting Started**: Complete
- ✅ **User Guide**: CLI and Library complete, others TBD
- ✅ **Performance**: Benchmarking complete, optimization TBD
- ❌ **API Reference**: To be generated from docstrings
- ❌ **Development**: To be created

### TODO Items

1. **API Reference**: Auto-generate from docstrings using mkdocstrings
2. **Error Handling**: Complete error handling guide
3. **Performance Optimization**: Detailed optimization techniques
4. **Contributing Guide**: Development setup and guidelines
5. **Testing Guide**: How to run and write tests
6. **Release Notes**: Version history and changes

## 🚀 Deployment

### GitHub Pages (Recommended)

Deploy to GitHub Pages using the MkDocs GitHub Action:

```yaml
# .github/workflows/docs.yml
name: Deploy Documentation
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: 3.x
    - run: pip install mkdocs-material mkdocstrings[python]
    - run: mkdocs gh-deploy --force
```

### Manual Deployment

```bash
# Build and deploy to gh-pages branch
uv run mkdocs gh-deploy
```

## 🔧 Maintenance

### Regular Tasks

1. **Update examples** when API changes
2. **Add new features** to documentation
3. **Fix broken links** and references
4. **Update performance numbers** from benchmarks
5. **Review and improve** content based on user feedback

### Link Checking

```bash
# Check for broken links (requires additional tools)
mkdocs serve &
sleep 5
wget --spider -r -nd -nv -H -l 1 -w 1 -o linkcheck.log http://127.0.0.1:8000/pdf_pycrack/
```

## 📞 Getting Help

- **MkDocs Documentation**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **Markdown Guide**: https://www.markdownguide.org/
- **GitHub Issues**: Report documentation bugs and suggestions

---

**Happy documenting!** 📖✨
