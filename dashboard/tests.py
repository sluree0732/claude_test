from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboard:index')
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={self.url}"
        )

    def test_dashboard_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_dashboard_shows_username(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.url)
        self.assertContains(response, 'testuser')
