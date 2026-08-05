#!/usr/bin/env bash
# Railway build script
set -o errexit

echo "🚀 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate --noinput

echo "🌱 Seeding initial data..."
python manage.py setup_initial_data || echo "⚠️  Initial data setup skipped (may already exist)"

echo "👤 Ensuring admin superuser..."
python manage.py ensure_admin || echo "⚠️  Admin setup skipped"

echo "✅ Build complete!"
