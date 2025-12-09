import os
import django
from datetime import timedelta
from django.utils import timezone
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wms.settings")
django.setup()

from django.contrib.auth import get_user_model
from workshops.models import Workshop

User = get_user_model()

# Ensure we have an admin and a speaker
admin, _ = User.objects.get_or_create(email="nitindaswani771@gmail.com", defaults={
    "role": "admin", "full_name": "Nitin Daswani"
})
if not admin.check_password("admin123"):
    admin.set_password("admin123")
    admin.save()

speaker, _ = User.objects.get_or_create(email="speaker@demo.com", defaults={
    "role": "speaker", "full_name": "Demo Speaker"
})
if not speaker.check_password("speaker123"):
    speaker.set_password("speaker123")
    speaker.save()

print("Users checked/created.")

# Delete existing
Workshop.objects.all().delete()
print("Cleared existing workshops.")

workshops_data = [
    {"title": "AI for Beginners", "cat": "AI / ML"},
    {"title": "Cloud Computing Bootcamp", "cat": "Cloud"},
    {"title": "Web Development Crash Course", "cat": "Programming"},
    {"title": "Data Science Essentials", "cat": "AI / ML"},
    {"title": "Cybersecurity Basics", "cat": "Technology"},
    {"title": "UI/UX Fundamentals", "cat": "Design"},
    {"title": "Python Masterclass", "cat": "Programming"},
    {"title": "ML Hands-on", "cat": "AI / ML"},
    {"title": "Public Speaking Workshop", "cat": "Soft Skills"},
    {"title": "Entrepreneurship 101", "cat": "Business"}
]

now = timezone.now().date()

for i, w in enumerate(workshops_data):
    # Determine status by date
    # 3 past, 4 live (today/near future), 3 upcoming (far future)
    if i < 3:
        start = now - timedelta(days=10 + i)
        end = start + timedelta(days=1)
    elif i < 7:
        start = now + timedelta(days=i) # Today or next few days
        end = start + timedelta(days=2)
    else:
        start = now + timedelta(days=20 + i)
        end = start + timedelta(days=2)

    Workshop.objects.create(
        title=w["title"],
        description=f"A comprehensive workshop on {w['title']}. Learn from industry experts and gain hands-on experience.",
        category=w["cat"],
        start_date=start,
        end_date=end,
        seat_limit=50,
        created_by=admin,
        speaker=speaker,
        budget=1000 + (i * 100)
    )

print(f"Seeded {len(workshops_data)} workshops.")
