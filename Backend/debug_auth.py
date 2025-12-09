import os
import django
import sys

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wms.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model

email = 'nitindaswani771@gmail.com'
password = 'admin123'

User = get_user_model()
try:
    user = User.objects.get(email=email)
    print(f"User found: {user.email}, Role: {user.role}, Active: {user.is_active}")
    print(f"Password set: {user.password[:10]}...")
    
    auth_user = authenticate(username=email, password=password)
    if auth_user:
        print("AUTHENTICATION SUCCESS via authenticate()")
    else:
        print("AUTHENTICATION FAILED via authenticate()")
        # Check password manually
        print(f"Manual check_password: {user.check_password(password)}")
except User.DoesNotExist:
    print("User not found in DB")
