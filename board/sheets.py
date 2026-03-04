"""Google Sheets를 게시판 데이터 저장소로 사용하는 헬퍼 모듈."""
import os
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

BASE_DIR = Path(__file__).resolve().parent.parent

SPREADSHEET_ID = '133HEXK5lNUPmYXxbtNSHKsp69hW1NGPs4-3HMDa6604'
SHEET_NAME = 'board'
USERS_SHEET_NAME = 'users'

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

# 헤더 행 정의
HEADERS = ['id', 'title', 'content', 'author', 'created_at']
USER_HEADERS = ['id', 'username', 'email', 'password', 'date_joined']


def _get_client():
    """Google Sheets API 클라이언트를 반환한다."""
    # Render 배포: 환경변수에서 JSON 내용 직접 읽기
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    if credentials_json:
        import json
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(credentials_json)
            tmp_path = f.name
        creds = Credentials.from_service_account_file(tmp_path, scopes=SCOPES)
        os.unlink(tmp_path)
    else:
        # 로컬: 프로젝트 폴더의 credentials 파일
        creds_path = BASE_DIR / 'naverproject-416908-fe3d84160448.json'
        creds = Credentials.from_service_account_file(str(creds_path), scopes=SCOPES)

    return gspread.authorize(creds)


def _get_sheet():
    """board 시트를 가져온다. 없으면 생성한다."""
    client = _get_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    try:
        sheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=len(HEADERS))
        sheet.append_row(HEADERS)

    return sheet


def _get_users_sheet():
    """users 시트를 가져온다. 없으면 생성한다."""
    client = _get_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    try:
        sheet = spreadsheet.worksheet(USERS_SHEET_NAME)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=USERS_SHEET_NAME, rows=1000, cols=len(USER_HEADERS))
        sheet.append_row(USER_HEADERS)

    return sheet


def create_user_record(username: str, email: str, password: str) -> dict:
    """회원가입 시 사용자 정보를 Google Sheets에 저장한다."""
    from datetime import datetime

    sheet = _get_users_sheet()
    rows = sheet.get_all_records()

    existing_ids = [int(r['id']) for r in rows if str(r.get('id', '')).isdigit()]
    next_id = max(existing_ids, default=0) + 1

    date_joined = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([next_id, username, email, password, date_joined])

    return {'id': next_id, 'username': username, 'email': email, 'date_joined': date_joined}


def get_user_by_username(username: str) -> dict | None:
    """username으로 사용자를 조회한다."""
    sheet = _get_users_sheet()
    rows = sheet.get_all_records()
    for row in rows:
        if row.get('username') == username:
            return row
    return None


def get_user_by_id(user_id: int) -> dict | None:
    """id로 사용자를 조회한다."""
    sheet = _get_users_sheet()
    rows = sheet.get_all_records()
    for row in rows:
        if str(row.get('id')) == str(user_id):
            return row
    return None


def get_all_posts():
    """모든 게시글을 최신순으로 반환한다.

    Returns:
        list[dict]: 각 게시글 {'id', 'title', 'content', 'author', 'created_at'}
    """
    sheet = _get_sheet()
    rows = sheet.get_all_records()
    # 최신순 정렬 (created_at 내림차순)
    return sorted(rows, key=lambda r: r.get('created_at', ''), reverse=True)


def get_post(post_id: int):
    """특정 ID의 게시글을 반환한다.

    Returns:
        dict | None
    """
    sheet = _get_sheet()
    rows = sheet.get_all_records()
    for row in rows:
        if str(row.get('id')) == str(post_id):
            return row
    return None


def create_post(title: str, content: str, author: str) -> dict:
    """새 게시글을 저장하고 반환한다."""
    from datetime import datetime

    sheet = _get_sheet()
    rows = sheet.get_all_records()

    # 다음 ID 계산
    existing_ids = [int(r['id']) for r in rows if str(r.get('id', '')).isdigit()]
    next_id = max(existing_ids, default=0) + 1

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_row = [next_id, title, content, author, created_at]
    sheet.append_row(new_row)

    return {
        'id': next_id,
        'title': title,
        'content': content,
        'author': author,
        'created_at': created_at,
    }
