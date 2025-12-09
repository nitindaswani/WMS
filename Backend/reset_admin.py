import os
import django
import sys

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wms.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

email = 'nitindaswani771@gmail.com'
password = 'admin123'

try:
    user = User.objects.get(email=email)
    user.set_password(password)
    user.role = 'admin' # Ensure role is admin
    user.save()
    print(f"Successfully reset password for {email}")
except User.DoesNotExist:
    print(f"User {email} not found. Creating...")
    User.objects.create_superuser(email=email, password=password, full_name='Admin User', role='admin')
    print(f"Created new admin user {email}")
except Exception as e:
    print(f"Error: {e}")
