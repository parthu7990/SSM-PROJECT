#!/bin/bash

# SSM Future Innovation FZE - Quick Setup Script
# This script automates the initial setup process

echo "================================================"
echo "SSM Future Innovation FZE - Website Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python is installed"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Dependencies installed"
echo ""

# Run migrations
echo "🗄️  Setting up database..."
python manage.py migrate

echo ""
echo "✓ Database setup complete"
echo ""

# Create superuser prompt
echo "👤 Creating admin user..."
echo "Please provide the following information:"
python manage.py createsuperuser

echo ""

# Create initial company info
echo "🏢 Creating initial company information..."
python manage.py shell << EOF
from core.models import CompanyInfo
if not CompanyInfo.objects.exists():
    CompanyInfo.objects.create(
        company_name='SSM Future Innovation FZE',
        tagline='Enterprise Innovation With Measurable Impact',
        about_text='Based in Sharjah Publishing City Free Zone, UAE, SSM Future Innovation FZE partners with enterprises navigating modernization, digital expansion, and strategic repositioning in competitive markets.',
        email='info@ssmfutureinnovation.com',
        phone='+971 58 268 4800',
        address='Sharjah Publishing City Free Zone, Sharjah, United Arab Emirates'
    )
    print("✓ Company information created")
else:
    print("✓ Company information already exists")
EOF

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "2. Access the website at:"
echo "   http://localhost:8000/"
echo ""
echo "3. Access the admin panel at:"
echo "   http://localhost:8000/admin/login/"
echo ""
echo "4. Add content through the admin panel:"
echo "   - Upload service images"
echo "   - Add client logos"
echo "   - Create hero slides"
echo "   - Manage inquiries"
echo ""
echo "================================================"
echo "🚀 Ready to launch!"
echo "================================================"
