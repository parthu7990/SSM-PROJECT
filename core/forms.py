from django import forms
from .models import ContactInquiry, Newsletter


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+971 XX XXX XXXX',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name (Optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            })
        }
