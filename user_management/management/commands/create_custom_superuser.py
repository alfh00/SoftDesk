from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with additional fields'

    def handle(self, *args, **options):
        username = input('Username: ')
        email = input('Email address: ')
        password = None
        while not password:
            password = input('Password: ')
            password2 = input('Password (again): ')
            if password != password2:
                self.stdout.write(self.style.ERROR('Passwords do not match. Please try again.'))
                password = None

        date_of_birth = input('Date of birth (YYYY-MM-DD): ')

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            is_superuser=True,
            is_staff=True,
        )

        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
