"""
Ensure the default superuser / admin account exists.

This command creates (or updates) the admin user used to log in to both the
custom admin panel and Django's built-in admin. It is idempotent and safe to
run on every deployment (e.g. from build.sh / Procfile) regardless of whether
the target database is SQLite, Railway Postgres, or Supabase Postgres.

Credentials are read from environment variables so they are not hard-coded
into the repository. Defaults are provided for convenience.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    help = 'Create or update the default superuser for the deployed site.'

    def handle(self, *args, **options):
        User = get_user_model()

        username = config('ADMIN_USERNAME', default='Parth')
        email    = config('ADMIN_EMAIL',    default='parth20098@gmail.com')
        password = config('ADMIN_PASSWORD', default='Parth@7990')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        if created:
            # Ensure flags are set even if defaults didn't apply.
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Superuser created: {username}'))
        else:
            # Update the password and flags so the credentials are always
            # correct on a fresh or existing database.
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Superuser updated: {username}'))

        self.stdout.write(f'    └ email: {email}')
        self.stdout.write(f'    └ is_staff: {user.is_staff}')
        self.stdout.write(f'    └ is_superuser: {user.is_superuser}')
