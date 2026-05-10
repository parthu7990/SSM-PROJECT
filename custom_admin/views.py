from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from core.models import (
    Service, ServiceItem, Client, ContactInquiry,
    Testimonial, HeroSlide, CompanyInfo, Newsletter
)
from .models import AdminActivity
from .forms import (
    ServiceForm, ClientForm, TestimonialForm,
    HeroSlideForm, CompanyInfoForm
)


def is_staff(user):
    return user.is_staff or user.is_superuser


def admin_login(request):
    """Custom admin login"""
    if request.user.is_authenticated and is_staff(request.user):
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and is_staff(user):
            login(request, user)
            
            # Log activity
            AdminActivity.objects.create(
                user=user,
                action='login',
                description=f"User {username} logged in",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'custom_admin/login.html')


@login_required
@user_passes_test(is_staff)
def admin_logout(request):
    """Custom admin logout"""
    AdminActivity.objects.create(
        user=request.user,
        action='logout',
        description=f"User {request.user.username} logged out",
        ip_address=get_client_ip(request)
    )
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('custom_admin:login')


@login_required
@user_passes_test(is_staff)
def dashboard(request):
    """Admin dashboard"""
    # Statistics
    total_inquiries = ContactInquiry.objects.count()
    new_inquiries = ContactInquiry.objects.filter(status='new').count()
    total_clients = Client.objects.filter(is_active=True).count()
    total_services = Service.objects.filter(is_active=True).count()
    newsletter_subscribers = Newsletter.objects.filter(is_active=True).count()
    
    # Recent inquiries
    recent_inquiries = ContactInquiry.objects.all()[:5]
    
    # Recent activities
    recent_activities = AdminActivity.objects.all()[:10]
    
    # Inquiry trends (last 7 days)
    last_7_days = timezone.now() - timedelta(days=7)
    inquiry_trend = ContactInquiry.objects.filter(
        created_at__gte=last_7_days
    ).extra({'date': 'date(created_at)'}).values('date').annotate(count=Count('id'))
    
    context = {
        'total_inquiries': total_inquiries,
        'new_inquiries': new_inquiries,
        'total_clients': total_clients,
        'total_services': total_services,
        'newsletter_subscribers': newsletter_subscribers,
        'recent_inquiries': recent_inquiries,
        'recent_activities': recent_activities,
        'inquiry_trend': inquiry_trend,
    }
    
    return render(request, 'custom_admin/dashboard.html', context)


@login_required
@user_passes_test(is_staff)
def inquiries_list(request):
    """List all contact inquiries"""
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    inquiries = ContactInquiry.objects.all()
    
    if status_filter:
        inquiries = inquiries.filter(status=status_filter)
    
    if search_query:
        inquiries = inquiries.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    context = {
        'inquiries': inquiries,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'custom_admin/inquiries_list.html', context)


@login_required
@user_passes_test(is_staff)
def inquiry_detail(request, pk):
    """View and update inquiry details"""
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes')
        
        inquiry.status = status
        inquiry.admin_notes = admin_notes
        inquiry.save()
        
        AdminActivity.objects.create(
            user=request.user,
            action='update',
            model_name='ContactInquiry',
            object_id=inquiry.id,
            description=f"Updated inquiry from {inquiry.name}",
            ip_address=get_client_ip(request)
        )
        
        messages.success(request, 'Inquiry updated successfully.')
        return redirect('custom_admin:inquiry_detail', pk=pk)
    
    context = {'inquiry': inquiry}
    return render(request, 'custom_admin/inquiry_detail.html', context)


@login_required
@user_passes_test(is_staff)
def services_list(request):
    """List all services"""
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'custom_admin/services_list.html', context)


@login_required
@user_passes_test(is_staff)
def service_create(request):
    """Create new service"""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            
            AdminActivity.objects.create(
                user=request.user,
                action='create',
                model_name='Service',
                object_id=service.id,
                description=f"Created service: {service.title}",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Service created successfully.')
            return redirect('custom_admin:services_list')
    else:
        form = ServiceForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'custom_admin/service_form.html', context)


@login_required
@user_passes_test(is_staff)
def service_edit(request, pk):
    """Edit existing service"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            
            AdminActivity.objects.create(
                user=request.user,
                action='update',
                model_name='Service',
                object_id=service.id,
                description=f"Updated service: {service.title}",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Service updated successfully.')
            return redirect('custom_admin:services_list')
    else:
        form = ServiceForm(instance=service)
    
    context = {'form': form, 'action': 'Edit', 'service': service}
    return render(request, 'custom_admin/service_form.html', context)


@login_required
@user_passes_test(is_staff)
def service_delete(request, pk):
    """Delete service"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        title = service.title
        service.delete()
        
        AdminActivity.objects.create(
            user=request.user,
            action='delete',
            model_name='Service',
            description=f"Deleted service: {title}",
            ip_address=get_client_ip(request)
        )
        
        messages.success(request, 'Service deleted successfully.')
        return redirect('custom_admin:services_list')
    
    context = {'service': service}
    return render(request, 'custom_admin/service_confirm_delete.html', context)


@login_required
@user_passes_test(is_staff)
def clients_list(request):
    """List all clients"""
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'custom_admin/clients_list.html', context)


@login_required
@user_passes_test(is_staff)
def client_create(request):
    """Create new client"""
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            
            AdminActivity.objects.create(
                user=request.user,
                action='create',
                model_name='Client',
                object_id=client.id,
                description=f"Added client: {client.name}",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Client added successfully.')
            return redirect('custom_admin:clients_list')
    else:
        form = ClientForm()
    
    context = {'form': form, 'action': 'Add'}
    return render(request, 'custom_admin/client_form.html', context)


@login_required
@user_passes_test(is_staff)
def client_edit(request, pk):
    """Edit existing client"""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            
            AdminActivity.objects.create(
                user=request.user,
                action='update',
                model_name='Client',
                object_id=client.id,
                description=f"Updated client: {client.name}",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Client updated successfully.')
            return redirect('custom_admin:clients_list')
    else:
        form = ClientForm(instance=client)
    
    context = {'form': form, 'action': 'Edit', 'client': client}
    return render(request, 'custom_admin/client_form.html', context)


@login_required
@user_passes_test(is_staff)
def client_delete(request, pk):
    """Delete client"""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        name = client.name
        client.delete()
        
        AdminActivity.objects.create(
            user=request.user,
            action='delete',
            model_name='Client',
            description=f"Deleted client: {name}",
            ip_address=get_client_ip(request)
        )
        
        messages.success(request, 'Client deleted successfully.')
        return redirect('custom_admin:clients_list')
    
    context = {'client': client}
    return render(request, 'custom_admin/client_confirm_delete.html', context)


@login_required
@user_passes_test(is_staff)
def company_info(request):
    """Edit company information"""
    company, created = CompanyInfo.objects.get_or_create(
        defaults={
            'company_name': 'SSM Future Innovation FZE',
            'tagline': 'Enterprise Innovation With Measurable Impact',
            'about_text': 'Strategic Growth Through Innovation',
            'email': 'info@ssmfutureinnovation.com',
            'phone': '+971 58 268 4800',
            'address': 'Sharjah Publishing City Free Zone, Sharjah, UAE'
        }
    )
    
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            
            AdminActivity.objects.create(
                user=request.user,
                action='update',
                model_name='CompanyInfo',
                object_id=company.id,
                description="Updated company information",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Company information updated successfully.')
            return redirect('custom_admin:company_info')
    else:
        form = CompanyInfoForm(instance=company)
    
    context = {'form': form, 'company': company}
    return render(request, 'custom_admin/company_info.html', context)


@login_required
@user_passes_test(is_staff)
def newsletter_subscribers(request):
    """List newsletter subscribers"""
    subscribers = Newsletter.objects.all()
    context = {'subscribers': subscribers}
    return render(request, 'custom_admin/newsletter_subscribers.html', context)


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
