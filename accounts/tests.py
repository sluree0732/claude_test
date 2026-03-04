from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:register')

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_password_mismatch(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass456!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='testuser', password='pass123')
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'other@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_register_empty_fields(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!'
        )

    def test_login_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_success_redirects_to_dashboard(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('dashboard:index'))

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.url, {
            'username': 'nobody',
            'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_empty_fields(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!'
        )
        self.client.login(username='testuser', password='StrongPass123!')

    def test_logout_redirects_to_login(self):
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))

    def test_logout_clears_session(self):
        self.client.post(reverse('accounts:logout'))
        response = self.client.get(reverse('dashboard:index'))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('dashboard:index')}"
        )
