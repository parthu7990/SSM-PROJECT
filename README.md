# PSK Future Innovation FZE - Website Upgrade

A modern, fully-featured Django-based website with glassmorphism effects, responsive design, and a custom admin panel.

## 🌟 Features

### Frontend
- ✅ **Modern Glassmorphism Design** - Beautiful glass effects throughout
- ✅ **Animated Background** - Floating gradient blobs
- ✅ **Responsive Design** - Works perfectly on mobile, tablet, and desktop
- ✅ **Smooth Animations** - AOS (Animate On Scroll) library integration
- ✅ **Hero Slider** - Multiple slides with smooth transitions
- ✅ **Interactive Service Cards** - Expandable cards with details
- ✅ **Infinite Client Carousel** - Auto-scrolling client logos
- ✅ **Contact Form** - With email notifications
- ✅ **Newsletter Subscription**
- ✅ **Testimonials Section**
- ✅ **Scroll Animations** - Elements animate as you scroll

### Backend
- ✅ **Django 6.0** - Latest Django framework
- ✅ **Custom Admin Panel** - Beautiful custom admin (not Django default)
- ✅ **Complete CRUD** - Create, Read, Update, Delete for all models
- ✅ **Email Integration** - Contact form sends emails
- ✅ **Activity Logging** - Track all admin actions
- ✅ **Status Tracking** - For inquiries (New, In Progress, Resolved, Closed)
- ✅ **Image Management** - Upload and manage images
- ✅ **SEO Ready** - Proper meta tags and structure

### Custom Admin Features
- ✅ Dashboard with statistics
- ✅ Inquiry management with filtering
- ✅ Services CRUD operations
- ✅ Clients portfolio management
- ✅ Company information editor
- ✅ Newsletter subscribers list
- ✅ Activity log viewer
- ✅ Secure authentication
- ✅ Beautiful glassmorphism UI

## 📋 Requirements

- Python 3.8+
- Django 6.0
- Pillow (for image handling)

## 🚀 Installation

### 1. Clone or extract the project
```bash
cd ssm_website
```

### 2. Install dependencies
```bash
pip install django pillow
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Create a superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 5. Create initial company info
```bash
python manage.py shell
```
Then in the Python shell:
```python
from core.models import CompanyInfo
CompanyInfo.objects.create(
    company_name='PSK Future Innovation FZE',
    tagline='Enterprise Innovation With Measurable Impact',
    about_text='Based in Sharjah Publishing City Free Zone, UAE, SSM Future Innovation FZE partners with enterprises navigating modernization, digital expansion, and strategic repositioning in competitive markets.',
    email='parth20098@gmail.com',
    phone='+917990661705',
    address='Sharjah Publishing City Free Zone, Sharjah, United Arab Emirates'
)
exit()
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Access the website
- **Main Website**: http://localhost:8000/
- **Custom Admin Panel**: http://localhost:8000/admin/login/
- **Django Admin (backup)**: http://localhost:8000/django-admin/

## 📁 Project Structure

```
ssm_website/
├── core/                      # Main website app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── forms.py              # Form classes
│   ├── admin.py              # Django admin config
│   └── urls.py               # URL routing
├── custom_admin/             # Custom admin panel app
│   ├── models.py             # Admin activity logging
│   ├── views.py              # Admin view functions
│   ├── forms.py              # Admin form classes
│   └── urls.py               # Admin URL routing
├── templates/
│   ├── base.html             # Base template
│   ├── core/
│   │   └── home.html         # Homepage template
│   └── custom_admin/         # Admin templates
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       └── ...
├── static/
│   ├── css/
│   │   ├── main.css          # Main website styles
│   │   └── admin.css         # Admin panel styles
│   └── js/
│       └── main.js           # JavaScript interactions
├── media/                    # Uploaded files
├── ssm_config/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## 🎨 Customization

### Changing Colors
Edit `/static/css/main.css` and modify the CSS variables:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    --accent-color: #8b5cf6;
}
```

### Email Configuration
For production, update `ssm_config/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Adding Content
Use the custom admin panel at `/admin/` to:
- Add/edit services
- Upload client logos
- Manage contact inquiries
- Update company information
- View newsletter subscribers

## 📊 Database Models

### Core Models
- **Service** - Services offered with categories
- **ServiceItem** - Individual features under each service
- **Client** - Client portfolio with logos
- **ContactInquiry** - Contact form submissions with status tracking
- **Testimonial** - Client testimonials
- **HeroSlide** - Homepage hero carousel slides
- **CompanyInfo** - Company details (singleton)
- **Newsletter** - Newsletter email subscriptions

### Admin Models
- **AdminActivity** - Activity logging for admin actions

## 🔒 Security Notes

1. **Change SECRET_KEY** in production:
   ```python
   # In settings.py
   SECRET_KEY = 'your-secure-random-key-here'
   ```

2. **Set DEBUG = False** in production:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **Use environment variables** for sensitive data

## 📱 Responsive Breakpoints

- Desktop: 1024px+
- Tablet: 768px - 1024px
- Mobile: < 768px

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📧 Contact Information

The website uses:
- **Email**: parth20098@gmail.com
- **Phone**: +917990661705
- **Address**: Sharjah Publishing City Free Zone, Sharjah, UAE

These can be updated through the admin panel under "Company Info".

## 🛠️ Deployment

### For Production:

1. Set environment variables
2. Configure static files: `python manage.py collectstatic`
3. Use a production server (Gunicorn, uWSGI)
4. Set up a reverse proxy (Nginx, Apache)
5. Use a production database (PostgreSQL recommended)
6. Enable HTTPS
7. Set up email service (SendGrid, AWS SES, etc.)

### Recommended Stack:
- **Server**: AWS EC2, DigitalOcean, or Heroku
- **Database**: PostgreSQL
- **Web Server**: Nginx + Gunicorn
- **Email**: SendGrid or AWS SES
- **Static Files**: AWS S3 or Cloudinary

## 📝 License

Copyright © 2026 SSM Future Innovation FZE. All rights reserved.

## 🤝 Support

For support, email parth20098@gmail.com or call +91 7990661705.

## 🎯 Features Checklist

- [x] Glassmorphism design
- [x] Responsive layout
- [x] Custom admin panel
- [x] Contact form with email
- [x] Newsletter subscription
- [x] Services management
- [x] Client portfolio
- [x] Testimonials
- [x] Hero slider
- [x] Activity logging
- [x] Status tracking for inquiries
- [x] Image upload handling
- [x] Smooth animations
- [x] SEO optimization
- [x] Mobile-friendly navigation

## 🚀 Quick Start Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Create migrations (if you modify models)
python manage.py makemigrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic
```

---

**Built with Django & Modern Web Technologies** 🚀
