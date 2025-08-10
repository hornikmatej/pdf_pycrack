#!/bin/bash

# Release script for pdf-pycrack
# This script will create a git tag and push it to trigger the GitHub Actions workflow

set -e

VERSION="v0.1.0"
BRANCH="main"

echo "🚀 Preparing release $VERSION"

# Ensure we're on the main branch
echo "📋 Checking git status..."
if [[ $(git rev-parse --abbrev-ref HEAD) != "$BRANCH" ]]; then
    echo "❌ You must be on the $BRANCH branch to create a release"
    exit 1
fi

# Check if working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean. Please commit or stash your changes."
    git status
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin $BRANCH

# Run tests to ensure everything is working
echo "🧪 Running tests..."
uv run pytest

# Build the package locally to verify
echo "🔨 Building package..."
uv build

# Create and push tag
echo "🏷️  Creating tag $VERSION..."
git tag -a "$VERSION" -m "Release $VERSION"

echo "📤 Pushing tag to GitHub..."
git push origin "$VERSION"

echo "✅ Release $VERSION has been created!"
echo "🌐 Check the GitHub Actions workflow at: https://github.com/hornikmatej/pdf_pycrack/actions"
echo "📦 Once the workflow completes, your package will be available on PyPI!"
