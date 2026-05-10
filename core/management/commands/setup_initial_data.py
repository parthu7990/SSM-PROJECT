from django.core.management.base import BaseCommand
from core.models import CompanyInfo, HeroSlide, Service, ServiceItem, Client, Testimonial


class Command(BaseCommand):
    help = 'Populate database with initial SSM data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('\n=== SSM Initial Data Setup ===\n'))

        # ── Company Info ──────────────────────────────
        if not CompanyInfo.objects.exists():
            CompanyInfo.objects.create(
                company_name='PSK Future Innovation FZE',
                tagline='Pioneering Smart Knowledge for Enterprise Growth',
                about_text=(
                    'Based in Sharjah Publishing City Free Zone, UAE, PSK Future Innovation FZE '
                    'partners with enterprises navigating modernization, digital expansion, and '
                    'strategic repositioning in competitive markets.'
                ),
                email='info@pskfutureinnovation.com',
                phone='+971 58 268 4800',
                address='Sharjah Publishing City Free Zone, Sharjah, United Arab Emirates',
                linkedin_url='https://linkedin.com',
                instagram_url='https://instagram.com',
            )
            self.stdout.write(self.style.SUCCESS('  ✓ Company information created'))
        else:
            self.stdout.write('  • Company information already exists')

        # ── Services ──────────────────────────────────
        services_data = [
            {
                'title': 'IT Expertise',
                'category': 'it',
                'description': (
                    'Comprehensive enterprise-grade infrastructure and application solutions '
                    'designed for performance, scalability, and security.'
                ),
                'order': 1,
                'items': [
                    'Network Solutions',
                    'Structured Cabling & Rack Stack Installations',
                    'Wired & Wireless Network Solutions',
                    'Enterprise Data Networks',
                    'Wi-Fi Infrastructure Solutions',
                    'Cloud Infrastructure Solutions',
                    'Datacenter Infrastructure Solutions',
                    'Software & IT Application Development',
                ],
            },
            {
                'title': 'Creativities',
                'category': 'creative',
                'description': (
                    'Brand strategy, visual identity, and high-impact corporate communication '
                    'that elevates your business presence in the market.'
                ),
                'order': 2,
                'items': [
                    'Logo Ideation, Concept & Creation',
                    'Corporate Collateral',
                    'Leaflet, Brochure, Business Stationery',
                    'Graphics, Animations',
                ],
            },
            {
                'title': 'Digital Solutions',
                'category': 'digital',
                'description': (
                    'End-to-end digital transformation, automation, and platform innovation '
                    'to modernize your business operations and online presence.'
                ),
                'order': 3,
                'items': [
                    'Website Coding, Concept & Development',
                    'Web Banners',
                    'E-Mailers',
                    'E-Commerce Website with Payment Gateway',
                    'Search Engine Optimization (Google)',
                    'Social Media Strategies',
                    'Multimedia Presentation',
                ],
            },
            {
                'title': 'Social Media Marketing',
                'category': 'marketing',
                'description': (
                    'Strategic campaigns, digital engagement, and performance-driven growth '
                    'across all major social media platforms.'
                ),
                'order': 4,
                'items': [
                    'Facebook Marketing',
                    'Twitter Marketing',
                    'LinkedIn Marketing',
                    'Instagram Marketing',
                    'Pinterest Marketing',
                    'YouTube Marketing',
                ],
            },
        ]

        for sd in services_data:
            items = sd.pop('items')
            s, created = Service.objects.get_or_create(
                title=sd['title'],
                defaults={**sd, 'image': ''},
            )
            if created:
                for i, item_title in enumerate(items):
                    ServiceItem.objects.create(service=s, title=item_title, order=i)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Service: {s.title}'))
            else:
                self.stdout.write(f'  • Service exists: {s.title}')

        # ── Clients ───────────────────────────────────
        client_names = [
            'PIXCOM', 'Just Click', 'Film District', 'The Laundry Point',
            'Supernova Photography', 'Taste of Malabar', 'Highway 311',
            'BiCXO', 'LEADGE', 'VISHWASWAROOP', 'AMBIENCE', 'TSS',
            'SNOW WHITE', 'MARIA MARIA', 'ERP PANDIT', 'KUUIZZ',
            'LAUKYA', 'OBL PRINTSTORE', 'YRSK', 'eresource', 'Print Mart', 'DEXA',
        ]
        for i, name in enumerate(client_names):
            _, created = Client.objects.get_or_create(
                name=name, defaults={'logo': '', 'order': i + 1}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Client: {name}'))

        # ── Testimonials ──────────────────────────────
        testimonials = [
            {
                'client_name': 'Ahmed Al Mansoori',
                'company': 'TechVentures UAE',
                'position': 'CEO',
                'content': (
                    'SSM Future Innovation transformed our entire IT infrastructure. '
                    'Their team delivered beyond expectations with professionalism and speed.'
                ),
                'rating': 5,
            },
            {
                'client_name': 'Priya Sharma',
                'company': 'Digital First Media',
                'position': 'Marketing Director',
                'content': (
                    'The social media strategy SSM developed for us tripled our engagement '
                    'in just three months. Absolutely exceptional work.'
                ),
                'rating': 5,
            },
            {
                'client_name': 'Omar Hassan',
                'company': 'Gulf Retail Group',
                'position': 'Operations Manager',
                'content': (
                    'From our e-commerce platform to our brand identity, SSM handled '
                    'everything seamlessly. Highly recommend their digital solutions.'
                ),
                'rating': 5,
            },
        ]
        for t in testimonials:
            _, created = Testimonial.objects.get_or_create(
                client_name=t['client_name'], defaults=t
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Testimonial: {t["client_name"]}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Setup complete!\n'))
        self.stdout.write('Next steps:')
        self.stdout.write('  1. python manage.py runserver')
        self.stdout.write('  2. Open http://localhost:8000/admin/login/')
        self.stdout.write('  3. Upload service images, client logos, and hero slides\n')
