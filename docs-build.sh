#!/bin/bash
# docs-build.sh - Build and serve documentation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if uv is available
if ! command -v uv &> /dev/null; then
    print_error "uv could not be found. Please install uv first."
    echo "Visit: https://github.com/astral-sh/uv"
    exit 1
fi

# Default action
ACTION=${1:-serve}

case $ACTION in
    "serve"|"dev")
        print_status "Starting documentation development server..."
        print_status "Documentation will be available at: http://127.0.0.1:8000/pdf_pycrack/"
        print_status "Press Ctrl+C to stop the server"
        echo
        uv run mkdocs serve
        ;;

    "build")
        print_status "Building static documentation..."
        uv run mkdocs build
        print_status "Documentation built successfully in: site/"
        ;;

    "deploy")
        print_status "Deploying to GitHub Pages..."
        uv run mkdocs gh-deploy
        print_status "Documentation deployed successfully!"
        ;;

    "clean")
        print_status "Cleaning build artifacts..."
        rm -rf site/
        print_status "Clean completed"
        ;;

    "install")
        print_status "Installing documentation dependencies..."
        uv sync
        print_status "Dependencies installed successfully!"
        ;;

    "check")
        print_status "Checking documentation..."
        uv run mkdocs build --strict
        print_status "Documentation check passed!"
        ;;

    "help"|"--help"|"-h")
        echo "PDF-PyCrack Documentation Build Script"
        echo
        echo "Usage: $0 [ACTION]"
        echo
        echo "Actions:"
        echo "  serve, dev    Start development server (default)"
        echo "  build         Build static documentation"
        echo "  deploy        Deploy to GitHub Pages"
        echo "  clean         Clean build artifacts"
        echo "  install       Install documentation dependencies"
        echo "  check         Check documentation for errors"
        echo "  help          Show this help message"
        echo
        echo "Examples:"
        echo "  $0                # Start development server"
        echo "  $0 serve          # Start development server"
        echo "  $0 build          # Build static site"
        echo "  $0 deploy         # Deploy to GitHub Pages"
        ;;

    *)
        print_error "Unknown action: $ACTION"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac
