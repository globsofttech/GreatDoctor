#!/bin/bash
# Medical Knowledge Portal - Quick Setup Script

echo "🏥 Medical Knowledge Portal Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements_enhanced.txt

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example_enhanced .env
    echo "⚠️  IMPORTANT: Edit .env with your credentials:"
    echo "   - MongoDB URI"
    echo "   - Gmail SMTP password"
    echo "   - Flask secret key"
    echo ""
    echo "Then run: python app_enhanced.py"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Run: python app_enhanced.py"
echo "3. Visit: http://localhost:5000/register"
echo ""
