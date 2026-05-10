from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('it',        'IT Expertise'),
        ('creative',  'Creativities'),
        ('digital',   'Digital Solutions'),
        ('marketing', 'Social Media Marketing'),
    ]
    title       = models.CharField(max_length=200)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    icon        = models.ImageField(upload_to='services/icons/', null=True, blank=True)
    image       = models.ImageField(upload_to='services/',       null=True, blank=True)
    order       = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    @property
    def image_url(self):
        """Safe URL — returns empty string if no image so template {% if service.image_url %} works."""
        if self.image:
            try:
                return self.image.url
            except Exception:
                return ''
        return ''

    @property
    def icon_url(self):
        if self.icon:
            try:
                return self.icon.url
            except Exception:
                return ''
        return ''


class ServiceItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='items')
    title   = models.CharField(max_length=200)
    order   = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.service.title} – {self.title}"


class Client(models.Model):
    name        = models.CharField(max_length=200)
    logo        = models.ImageField(upload_to='clients/', null=True, blank=True)
    website_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    order       = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        if self.logo:
            try:
                return self.logo.url
            except Exception:
                return ''
        return ''


class ContactInquiry(models.Model):
    STATUS_CHOICES = [
        ('new',         'New'),
        ('in_progress', 'In Progress'),
        ('resolved',    'Resolved'),
        ('closed',      'Closed'),
    ]
    name        = models.CharField(max_length=200)
    email       = models.EmailField(validators=[EmailValidator()])
    phone       = models.CharField(max_length=20)
    company     = models.CharField(max_length=200, blank=True)
    subject     = models.CharField(max_length=300)
    message     = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        return f"{self.name} – {self.subject}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    company     = models.CharField(max_length=200)
    position    = models.CharField(max_length=200)
    content     = models.TextField()
    rating      = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    image       = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    order       = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.client_name} – {self.company}"

    @property
    def image_url(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                return ''
        return ''


class HeroSlide(models.Model):
    title       = models.CharField(max_length=300)
    subtitle    = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='hero/', null=True, blank=True)
    cta_text    = models.CharField(max_length=100, default='Schedule Consultation')
    cta_link    = models.CharField(max_length=200, default='#contact')
    order       = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                return ''
        return ''


class CompanyInfo(models.Model):
    company_name  = models.CharField(max_length=200, default='PSK Future Innovation FZE')
    tagline       = models.CharField(max_length=300)
    about_text    = models.TextField()
    email         = models.EmailField()
    phone         = models.CharField(max_length=20)
    address       = models.TextField()
    facebook_url  = models.URLField(blank=True)
    twitter_url   = models.URLField(blank=True)
    linkedin_url  = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url   = models.URLField(blank=True)
    logo          = models.ImageField(upload_to='company/', null=True, blank=True)

    class Meta:
        verbose_name        = 'Company Information'
        verbose_name_plural = 'Company Information'

    def __str__(self):
        return self.company_name

    @property
    def logo_url(self):
        if self.logo:
            try:
                return self.logo.url
            except Exception:
                return ''
        return ''


class Newsletter(models.Model):
    email         = models.EmailField(unique=True)
    is_active     = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
