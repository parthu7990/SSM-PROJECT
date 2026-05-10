from django import forms
from core.models import Service, Client, Testimonial, HeroSlide, CompanyInfo


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'category', 'description', 'icon', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'logo', 'website_url', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['client_name', 'company', 'position', 'content', 'rating', 'image', 'is_active', 'order']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = ['title', 'subtitle', 'description', 'image', 'cta_text', 'cta_link', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'cta_text': forms.TextInput(attrs={'class': 'form-control'}),
            'cta_link': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = [
            'company_name', 'tagline', 'about_text', 'email', 'phone', 'address',
            'facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'youtube_url', 'logo'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'about_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
