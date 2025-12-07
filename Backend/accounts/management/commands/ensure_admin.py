from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates an admin user if not exists'

    def handle(self, *args, **options):
        User = get_user_model()
        email = "nitindaswani771@gmail.com"
        password = "nitin1234"
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password, full_name="Admin", role='admin')
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin {email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin {email} already exists'))
