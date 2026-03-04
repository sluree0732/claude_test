from django.contrib.auth.models import AnonymousUser

from board import sheets
from accounts.backends import SheetsUser


class SheetsAuthMiddleware:
    """세션 쿠키에서 사용자 ID를 읽어 Google Sheets에서 사용자를 조회한다."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('_sheets_user_id')
        if user_id:
            user_data = sheets.get_user_by_id(user_id)
            if user_data:
                request.user = SheetsUser(user_data['id'], user_data['username'], user_data['email'])
            else:
                request.session.flush()
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        return self.get_response(request)
