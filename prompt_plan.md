# Implementation Plan: 로그인 기능

**확정일**: 2026-03-04
**대상 경로**: `C:\Users\SW-2\Desktop\git-practice\claude_test`
**스택**: Python + Django + SQLite

## Overview
Django의 내장 인증 시스템을 활용해 이메일/비밀번호 로그인을 구현합니다. HTML 템플릿 기반의 풀스택 웹 앱으로, 별도 프론트엔드 없이 완성됩니다.

## Requirements
- Django 프로젝트 초기화 (Python 3.10+)
- 이메일/비밀번호 회원가입 + 로그인
- 로그인 후 대시보드 이동, 미인증 시 로그인 페이지 리다이렉트
- Django 내장 `auth` 모듈 활용 (비밀번호 해싱 자동 처리)
- SQLite 기본 DB

## Architecture
```
claude_test/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── accounts/                   # 인증 앱
│   ├── views.py                # 로그인/회원가입/로그아웃 뷰
│   ├── forms.py                # 입력 폼 (유효성 검증)
│   ├── urls.py
│   └── templates/accounts/
│       ├── login.html
│       └── register.html
└── dashboard/                  # 보호된 페이지
    ├── views.py
    ├── urls.py
    └── templates/dashboard/
        └── index.html
```

## Implementation Steps

### Phase 1: 프로젝트 초기화
1. **Django 프로젝트 생성** (터미널)
   - Action: `python -m venv venv` → 활성화 → `pip install django` → `django-admin startproject`
   - Acceptance Criteria: `python manage.py runserver` 성공, 기본 페이지 확인
   - Risk: Low

### Phase 2: 인증 앱 구성
2. **accounts 앱 생성 + 폼** (`accounts/forms.py`)
   - Action: `python manage.py startapp accounts`, `UserCreationForm` 상속해 이메일 필드 추가
   - Acceptance Criteria: 폼 유효성 검증 (빈 필드, 비밀번호 불일치 에러)
   - Risk: Low

3. **로그인/회원가입/로그아웃 뷰** (`accounts/views.py`)
   - Action: Django `LoginView`, `LogoutView` 활용 + 커스텀 `RegisterView` 구현
   - Acceptance Criteria: 올바른 자격증명으로 세션 생성, 잘못된 자격증명 시 에러 메시지
   - Risk: Low

### Phase 3: 보호된 페이지 + 템플릿
4. **dashboard 앱 + `@login_required`** (`dashboard/views.py`)
   - Action: `startapp dashboard`, 뷰에 `@login_required` 데코레이터 적용
   - Acceptance Criteria: 비인증 접근 시 `/accounts/login/?next=/dashboard/`로 리다이렉트
   - Risk: Low

5. **HTML 템플릿 작성** (`templates/`)
   - Action: 로그인/회원가입 폼 HTML, CSS 기본 스타일 적용
   - Acceptance Criteria: 폼 렌더링 정상, 에러 메시지 표시
   - Risk: Low

## Testing Strategy
- 수동 테스트: 회원가입 → 로그인 → 대시보드 → 로그아웃
- 에러 케이스: 잘못된 비밀번호, 중복 이메일, 빈 폼

## Risks & Mitigations
- **Risk**: `SECRET_KEY` 운영 환경 노출
  - Mitigation: `.env` 파일로 분리, `.gitignore` 추가
- **Risk**: `DEBUG=True` 운영 배포
  - Mitigation: `settings.py`에 환경별 분기 처리

## Success Criteria
- [ ] `runserver` 후 로그인 페이지 정상 표시
- [ ] 회원가입 후 로그인 성공
- [ ] `/dashboard/` 직접 접근 시 로그인 페이지로 리다이렉트
- [ ] 잘못된 비밀번호 입력 시 에러 메시지 표시
