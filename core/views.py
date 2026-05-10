from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import (
    Service, Client, ContactInquiry,
    Testimonial, HeroSlide, CompanyInfo, Newsletter
)
from .forms import ContactForm, NewsletterForm


def home(request):
    """Homepage view"""
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True),
        'clients': Client.objects.filter(is_active=True),
        'total_clients': Client.objects.filter(is_active=True).count(),
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
    }
    return render(request, 'core/home.html', context)


def contact_submit(request):
    """Handle contact form submission — supports both AJAX and regular POST"""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Send email notification to admin
            try:
                subject = f"New Inquiry: {inquiry.subject}"
                body = (
                    f"New contact inquiry received:\n\n"
                    f"Name: {inquiry.name}\n"
                    f"Email: {inquiry.email}\n"
                    f"Phone: {inquiry.phone}\n"
                    f"Company: {inquiry.company or 'N/A'}\n"
                    f"Subject: {inquiry.subject}\n\n"
                    f"Message:\n{inquiry.message}\n\n"
                    f"---\nSubmitted at: {inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                send_mail(
                    subject, body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your inquiry! We will get back to you within 24 hours.'
                })
            messages.success(request, 'Thank you! We will get back to you within 24 hours.')
            return redirect('home')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            messages.error(request, 'Please fill in all required fields correctly.')

    return redirect('home')


def newsletter_subscribe(request):
    """Handle newsletter subscription — supports both AJAX and regular POST"""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            obj, created = Newsletter.objects.get_or_create(email=email)
            msg = 'Successfully subscribed!' if created else 'You are already subscribed.'
            if is_ajax:
                return JsonResponse({'success': True, 'message': msg})
            messages.success(request, msg)
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Invalid email address.'}, status=400)
            messages.error(request, 'Invalid email address.')

    return redirect('home')


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)
