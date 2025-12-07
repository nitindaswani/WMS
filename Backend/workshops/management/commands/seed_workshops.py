import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from workshops.models import Workshop, Session
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with realistic workshop data matches the user request'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Create Speakers
        speakers = []
        speaker_names = ['Alice Tech', 'Bob Design', 'Charlie Biz', 'Dana Art', 'Eve Coder']
        for name in speaker_names:
            email = f"{name.split()[0].lower()}@example.com"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': name,
                    'role': 'speaker',
                    'is_staff': False
                }
            )
            if created:
                user.set_password('pass1234')
                user.save()
            speakers.append(user)
        
        # Ensure we have an admin or creator
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
             admin_user = User.objects.create_superuser('admin@example.com', 'adminpass')

        # 2. Workshop Data Pools
        titles_tech = ['React Masterclass', 'Django Deep Dive', 'AI for Beginners', 'Cloud Architecture 101']
        titles_design = ['UI/UX Principles', 'Figma Mastery', 'Graphic Design Trends']
        titles_biz = ['Startup 101', 'Agile Management', 'Product Strategy']
        
        categories = ['Technology', 'Design', 'Business']
        
        # 3. Create 3 Past, 4 Live, 3 Upcoming
        scenarios = [
            ('past', 3),
            ('live', 4),
            ('upcoming', 3)
        ]
        
        created_count = 0
        
        for status, count in scenarios:
            for i in range(count):
                # Pick category and title
                cat = random.choice(categories)
                if cat == 'Technology': title = random.choice(titles_tech)
                elif cat == 'Design': title = random.choice(titles_design)
                else: title = random.choice(titles_biz)
                
                # Add variation to title to avoid dupes
                title = f"{title} - {status.capitalize()} Edition {i+1}"
                
                # Set dates
                today = timezone.now().date()
                if status == 'past':
                    start_date = today - timedelta(days=random.randint(20, 60))
                    end_date = start_date + timedelta(days=2)
                elif status == 'live':
                    start_date = today - timedelta(days=1) # Started yesterday
                    end_date = today + timedelta(days=2) # Ends in 2 days
                else: # upcoming
                    start_date = today + timedelta(days=random.randint(10, 30))
                    end_date = start_date + timedelta(days=2)
                
                # Create Workshop
                workshop = Workshop.objects.create(
                    title=title,
                    description=f"A comprehensive workshop on {title}. Join us to learn from industry experts.",
                    category=cat,
                    seat_limit=random.randint(30, 100),
                    start_date=start_date,
                    end_date=end_date,
                    budget=random.randint(1000, 5000),
                    created_by=admin_user,
                    speaker=random.choice(speakers)
                )
                
                # Create Sessions
                Session.objects.create(
                    workshop=workshop,
                    session_title="Morning Session",
                    description="Introduction and Core Concepts",
                    start_time="09:00:00",
                    end_time="12:00:00",
                    day_of_week="Monday", # Simplified
                    mode='offline'
                )
                Session.objects.create(
                    workshop=workshop,
                    session_title="Afternoon Lab",
                    description="Hands-on practice.",
                    start_time="13:00:00",
                    end_time="16:00:00",
                    day_of_week="Monday",
                    mode='offline'
                )
                
                created_count += 1
                self.stdout.write(f"Created {status} workshop: {title}")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} workshops.'))
