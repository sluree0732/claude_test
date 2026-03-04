from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from board import sheets
from .backends import SheetsUser
from .forms import RegisterForm


def _session_login(request, user):
    """세션에 사용자 ID를 저장한다."""
    request.session['_sheets_user_id'] = user.id
    request.user = user


def _session_logout(request):
    """세션에서 사용자 정보를 제거한다."""
    request.session.flush()


class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user_data = sheets.get_user_by_username(username)
        if user_data and user_data.get('password') == password:
            user = SheetsUser(user_data['id'], user_data['username'], user_data['email'])
            _session_login(request, user)
            return redirect('dashboard:index')

        return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if sheets.get_user_by_username(username):
                form.add_error('username', '이미 사용 중인 아이디입니다.')
                return render(request, 'accounts/register.html', {'form': form})

            record = sheets.create_user_record(username, email, password)
            user = SheetsUser(record['id'], username, email)
            _session_login(request, user)
            return redirect('dashboard:index')

        return render(request, 'accounts/register.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        _session_logout(request)
        return redirect('accounts:login')


@method_decorator(login_required, name='dispatch')
class MyPageView(View):
    def get(self, request):
        return render(request, 'accounts/mypage.html')


class CheckUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', '').strip()
        if not username:
            return JsonResponse({'available': False, 'message': '아이디를 입력해주세요.'})
        if len(username) < 4:
            return JsonResponse({'available': False, 'message': '아이디는 4자 이상이어야 합니다.'})
        if sheets.get_user_by_username(username):
            return JsonResponse({'available': False, 'message': '이미 사용 중인 아이디입니다.'})
        return JsonResponse({'available': True, 'message': '사용 가능한 아이디입니다.'})
