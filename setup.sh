#!/bin/bash
# CHAMP Development Environment Setup Script

set -e

echo "🎯 Setting up CHAMP development environment..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "🔨 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo ""
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install development dependencies
echo ""
echo "📦 Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks (only if git repo exists)
echo ""
if [ -d .git ]; then
    echo "🪝 Setting up pre-commit hooks..."
    pre-commit install
else
    echo "⏭️  Skipping pre-commit hooks (not a git repo yet)"
    echo "   Run 'git init && pre-commit install' when ready"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Open project in PyCharm"
echo "  3. Configure PyCharm to use venv/bin/python as interpreter"
echo "  4. Start developing!"
echo ""
echo "🧪 Run tests with: pytest"
echo "🎨 Format code with: black custom_components/"
echo "🔍 Lint code with: ruff check custom_components/"
echo "📊 Type check with: mypy custom_components/"
echo ""
