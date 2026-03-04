from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views import View

from .forms import RegisterForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:index')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        # Mask username enumeration: replace duplicate-username error with generic message
        if form.errors.get('username'):
            form.errors['username'] = ['입력하신 정보를 다시 확인해주세요.']
        return render(request, 'accounts/register.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('accounts:login')
