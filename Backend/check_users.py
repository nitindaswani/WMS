
import os
import django
import sys

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wms.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print(f"{'Email':<30} | {'Role':<10} | {'Full Name'}")
print("-" * 60)
for user in User.objects.all():
    print(f"{user.email:<30} | {user.role:<10} | {user.full_name}")
