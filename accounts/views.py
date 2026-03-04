from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from board import sheets
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
            user = form.save()
            sheets.create_user_record(user.username, user.email)
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


class CheckUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', '').strip()
        if not username:
            return JsonResponse({'available': False, 'message': '아이디를 입력해주세요.'})
        if len(username) < 4:
            return JsonResponse({'available': False, 'message': '아이디는 4자 이상이어야 합니다.'})
        exists = User.objects.filter(username=username).exists()
        if exists:
            return JsonResponse({'available': False, 'message': '이미 사용 중인 아이디입니다.'})
        return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('accounts:login')


@method_decorator(login_required, name='dispatch')
class MyPageView(View):
    def get(self, request):
        return render(request, 'accounts/mypage.html')
