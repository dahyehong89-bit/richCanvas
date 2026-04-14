# 💸 가계부 (Django Accountbook)

모바일 친화적 반응형 가계부 웹앱

## 기능
- 💚 수입/지출 입력 및 관리
- 🗂 카테고리별 분류
- 📊 월별 통계 차트 (Chart.js)
- 🎯 예산 설정 및 초과 알림

## 기술 스택
- **Backend**: Python 3, Django 4.2
- **DB**: SQLite (개발) / PostgreSQL 전환 가능
- **Frontend**: Vanilla JS, Chart.js
- **Version Control**: Git

## 빠른 시작

```bash
# 1. 저장소 클론
git clone <your-repo-url>
cd accountbook

# 2. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경변수 설정
cp .env.example .env
# .env 파일에서 SECRET_KEY 수정

# 5. DB 마이그레이션
python manage.py migrate

# 6. 샘플 데이터 (선택)
python manage.py seed_data

# 7. 서버 실행
python manage.py runserver
```

브라우저에서 http://127.0.0.1:8000 접속

## 디렉토리 구조

```
accountbook/
├── accountbook/        # 프로젝트 설정
│   ├── settings.py
│   └── urls.py
├── ledger/             # 가계부 앱
│   ├── models.py       # Category, Transaction, Budget
│   ├── views.py        # 뷰 로직
│   ├── urls.py         # URL 라우팅
│   ├── admin.py        # 관리자 페이지
│   ├── templates/      # HTML 템플릿
│   └── management/     # 커스텀 명령어
├── requirements.txt
├── .gitignore
└── README.md
```

## Git 연동 및 업데이트

```bash
git add .
git commit -m "feat: 거래 내역 추가"
git push origin main
```
