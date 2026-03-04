"""Google Sheets 기반 커스텀 인증 백엔드."""
from board import sheets


class SheetsUser:
    """Django User 인터페이스를 모방하는 Sheets 기반 사용자 클래스."""
    is_authenticated = True
    is_active = True
    is_anonymous = False
    is_staff = False
    is_superuser = False

    class _PK:
        def value_to_string(self, obj):
            return str(obj.pk)

    class _Meta:
        pass

    def __init__(self, user_id, username, email):
        self.id = int(user_id)
        self.pk = int(user_id)
        self.username = username
        self.email = email
        self._meta = self.__class__._Meta()
        self._meta.pk = self.__class__._PK()

    def get_username(self):
        return self.username

    def __str__(self):
        return self.username


class SheetsAuthBackend:
    """Google Sheets에서 사용자를 인증하는 백엔드."""

    def authenticate(self, request, username=None, password=None):
        user_data = sheets.get_user_by_username(username)
        if user_data and user_data.get('password') == password:
            return SheetsUser(user_data['id'], user_data['username'], user_data['email'])
        return None

    def get_user(self, user_id):
        try:
            user_data = sheets.get_user_by_id(int(user_id))
        except (ValueError, TypeError):
            return None
        if user_data:
            return SheetsUser(user_data['id'], user_data['username'], user_data['email'])
        return None
