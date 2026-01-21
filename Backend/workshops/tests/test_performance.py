from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from workshops.models import Workshop, Session
from datetime import date

User = get_user_model()

class WorkshopPerformanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='password', full_name='Test User', role='student')
        self.admin = User.objects.create_user(email='admin@example.com', password='password', full_name='Admin User', role='admin')
        self.client.force_authenticate(user=self.user)

        # Create multiple workshops
        for i in range(10):
            w = Workshop.objects.create(
                title=f'Workshop {i}',
                description='Desc',
                start_date=date(2025, 1, 1),
                end_date=date(2025, 1, 2),
                seat_limit=10,
                created_by=self.admin
            )
            # Create sessions for each
            for j in range(3):
                Session.objects.create(
                    workshop=w,
                    session_title=f'Session {j}',
                    start_time='10:00',
                    end_time='11:00',
                    day_of_week='Monday'
                )

    def test_workshop_list_performance(self):
        # We expect a constant number of queries regardless of N workshops because of prefetch
        # 1. Auth user (Cached/Session) - often not counted if using force_authenticate correctly or depends on middleware
        # 2. Count workshops (pagination - if any, default might be none)
        # 3. Fetch workshops
        # 4. Fetch sessions (prefetch)

        # In the test output we saw 2 queries:
        # 1. Main fetch with joins
        # 2. Prefetch sessions
        # The session auth or user query might be skipped or already cached in test client setup

        with self.assertNumQueries(2):
            response = self.client.get('/api/workshops/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 10)
            self.assertTrue('sessions' in response.data[0])

    def test_workshop_detail_performance(self):
        workshop = Workshop.objects.first()
        with self.assertNumQueries(2): # 1 for workshop+related, 1 for prefetch sessions
            response = self.client.get(f'/api/workshops/{workshop.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

class AdminAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(email='newadmin@example.com', password='password', full_name='New Admin', role='admin')

    def test_admin_login(self):
        # Test that any admin can login, not just the hardcoded one
        response = self.client.post('/api/auth/login/', {
            'username': 'newadmin@example.com',
            'password': 'password',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
