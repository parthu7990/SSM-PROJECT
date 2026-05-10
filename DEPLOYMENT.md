# Deployment Guide - SSM Future Innovation FZE Website

## Production Deployment Checklist

### 1. Pre-Deployment Configuration

#### Update settings.py for production:

```python
# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'your-server-ip']

# Generate a new SECRET_KEY
# You can use: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = 'your-production-secret-key-here'

# Database Configuration (PostgreSQL recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ssm_db',
        'USER': 'ssm_user',
        'PASSWORD': 'your-secure-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@ssmfutureinnovation.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = 'info@ssmfutureinnovation.com'
ADMIN_EMAIL = 'info@ssmfutureinnovation.com'

# Static and Media Files
STATIC_ROOT = '/var/www/ssm_website/static/'
MEDIA_ROOT = '/var/www/ssm_website/media/'

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 2. Server Setup (Ubuntu/Debian)

#### Install required packages:
```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
```

#### Install Python packages:
```bash
sudo pip3 install virtualenv
```

#### Create virtual environment:
```bash
cd /var/www/
sudo mkdir ssm_website
sudo chown $USER:$USER ssm_website
cd ssm_website
virtualenv venv
source venv/bin/activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. Database Setup (PostgreSQL)

```bash
sudo -u postgres psql
```

In PostgreSQL:
```sql
CREATE DATABASE ssm_db;
CREATE USER ssm_user WITH PASSWORD 'your-secure-password';
ALTER ROLE ssm_user SET client_encoding TO 'utf8';
ALTER ROLE ssm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ssm_user SET timezone TO 'Asia/Dubai';
GRANT ALL PRIVILEGES ON DATABASE ssm_db TO ssm_user;
\q
```

#### Run migrations:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py setup_initial_data
python manage.py collectstatic
```

### 4. Gunicorn Setup

Create Gunicorn socket file:
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Add:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Create Gunicorn service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ssm_website
ExecStart=/var/www/ssm_website/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          ssm_config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable Gunicorn:
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

### 5. Nginx Configuration

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/ssm_website
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/ssm_website/static/;
    }
    
    location /media/ {
        alias /var/www/ssm_website/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/ssm_website /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts to configure SSL.

### 7. File Permissions

```bash
sudo chown -R www-data:www-data /var/www/ssm_website
sudo chmod -R 755 /var/www/ssm_website
sudo chmod -R 775 /var/www/ssm_website/media
```

### 8. Environment Variables (Recommended)

Create .env file:
```bash
nano /var/www/ssm_website/.env
```

Add:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_NAME=ssm_db
DATABASE_USER=ssm_user
DATABASE_PASSWORD=your-password
EMAIL_HOST_USER=info@ssmfutureinnovation.com
EMAIL_HOST_PASSWORD=your-email-password
```

Install python-decouple:
```bash
pip install python-decouple
```

Update settings.py to use environment variables:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## Cloud Deployment Options

### Option 1: AWS EC2
1. Launch EC2 instance (Ubuntu 22.04)
2. Configure security groups (HTTP, HTTPS, SSH)
3. Follow server setup steps above
4. Use RDS for PostgreSQL
5. Use S3 for media files
6. Use CloudFront for CDN

### Option 2: DigitalOcean
1. Create Droplet (Ubuntu 22.04)
2. Follow server setup steps above
3. Use Spaces for media files
4. Add domain and SSL

### Option 3: Heroku
1. Install Heroku CLI
2. Create Procfile:
   ```
   web: gunicorn ssm_config.wsgi --log-file -
   ```
3. Create runtime.txt:
   ```
   python-3.11.0
   ```
4. Deploy:
   ```bash
   heroku create ssm-website
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Option 4: PythonAnywhere
1. Upload project files
2. Create virtual environment
3. Configure WSGI file
4. Set up static files
5. Configure domain

## Post-Deployment

### 1. Configure Email Service

#### Gmail Setup:
1. Enable 2-factor authentication
2. Generate app-specific password
3. Update EMAIL_HOST_PASSWORD in settings

#### SendGrid Setup:
```bash
pip install sendgrid
```

Update settings.py:
```python
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your-sendgrid-api-key'
```

### 2. Media Files on AWS S3

```bash
pip install boto3 django-storages
```

Update settings.py:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'ssm-media'
AWS_S3_REGION_NAME = 'us-east-1'
```

### 3. Monitoring and Logging

Install Sentry for error tracking:
```bash
pip install sentry-sdk
```

Add to settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### 4. Backup Strategy

Create backup script:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump ssm_db > /backups/db_$DATE.sql
tar -czf /backups/media_$DATE.tar.gz /var/www/ssm_website/media/
```

Add to crontab:
```bash
0 2 * * * /path/to/backup_script.sh
```

## Maintenance

### Update Application:
```bash
cd /var/www/ssm_website
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### View Logs:
```bash
# Gunicorn logs
sudo journalctl -u gunicorn

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Performance Optimization

### 1. Enable Caching:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Optimize Database:
```python
CONN_MAX_AGE = 600
```

### 3. Compress Static Files:
```bash
pip install django-compressor
```

## Security Best Practices

1. Keep Django and dependencies updated
2. Use strong passwords
3. Regular security audits
4. Monitor server logs
5. Implement rate limiting
6. Use HTTPS everywhere
7. Regular backups
8. Keep SECRET_KEY secure
9. Use environment variables
10. Implement CSRF protection

## Support

For deployment assistance, contact: info@ssmfutureinnovation.com
