"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging
from datetime import datetime

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

logger = logging.getLogger(__name__)


def health_check(request):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('[WAKE] 서버 활성 확인 - %s', now)
    return JsonResponse({'status': 'ok', 'time': now})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('board/', include('board.urls', namespace='board')),
]
