from django.contrib import admin
from .models import (
    Service, ServiceItem, Client, ContactInquiry,
    Testimonial, HeroSlide, CompanyInfo, Newsletter
)


class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    inlines = [ServiceItemInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active']
    search_fields = ['client_name', 'company', 'content']


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not CompanyInfo.objects.exists()


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
