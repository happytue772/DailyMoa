1. 프로젝트 소개

**DailyMoa**는 할 일, 일정, 감정, 일기를 하나의 흐름으로 관리할 수 있도록 만든 **Flask 기반 개인 라이프 아카이빙 웹 서비스**입니다. 사용자가 하루를 `계획 → 일정 관리 → 감정 기록 → 일기 작성 → 회고`의 흐름으로 관리할 수 있도록 설계했으며, 단순한 Todo 또는 Diary 기능을 넘어서 여러 기록 기능을 하나의 서비스 안에서 연결하는 것을 목표로 했습니다.

2. 기술 스택

- **Language**: Python, JavaScript, HTML5, CSS3
- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy
- **Template Engine**: Jinja2
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Frontend Library**: FullCalendar
- **Browser Storage**: localStorage, sessionStorage
- **Development Environment**: Windows, WSL Ubuntu, VS Code
- **Version Control**: Git, GitHub

3. 주요 기능

- 회원가입, 로그인, 로그아웃
- Flask-Login 기반 사용자 인증 및 로그인 상태 관리
- `current_user`를 기준으로 한 사용자별 데이터 분리
- Dashboard에서 오늘의 Todo, 일정, 최근 Diary, 하루 요약, 실시간 시계 확인
- Todo 등록, 조회, 수정, 삭제, 완료 여부, 우선순위, 마감일, 검색, 필터 기능
- FullCalendar 기반 일정 등록, 수정, 삭제 및 날짜별 Schedule 관리
- Diary 등록, 조회, 수정, 삭제
- Diary 제목/내용 검색, 감정 필터, 행복 점수 기록
- `ImportantDiary`를 활용한 중요 기록 등록/해제 및 중요 Diary 필터링
- Diary 감정 데이터를 Flask JSON API로 변환하여 Calendar Event로 표시
- 날짜 기반 `오늘의 질문` 제공
- 로그인 직후 오늘의 질문 Modal 자동 표시
- `sessionStorage`를 활용한 질문 답변 임시 저장 및 Diary 작성 화면 연결
- `localStorage`를 활용한 Dark Mode 상태 유지
- 반응형 UI 구성

  4. 데이터베이스 구조

DailyMoa는 **SQLite**를 사용하며, SQLAlchemy ORM을 통해 데이터를 관리합니다.

주요 모델은 다음과 같습니다.

- `User`: 사용자 계정 정보
- `Todo`: 할 일, 우선순위, 마감일, 완료 여부
- `Schedule`: 일정 정보
- `Diary`: 제목, 내용, 감정, 행복 점수, 작성 날짜
- `ImportantDiary`: 사용자별 중요 Diary 관리

각 주요 데이터는 `user_id`를 기준으로 현재 로그인한 사용자와 연결되어 있으며, 다른 사용자의 개인 데이터가 조회되지 않도록 구성했습니다.

5. 프로젝트 구조

```text
DailyMoa/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── todo.py
│   ├── schedule.py
│   └── diary.py
│
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   └── dashboard.html
│   ├── calendar/
│   │   └── calendar.html
│   ├── todo/
│   │   ├── todo_add.html
│   │   ├── todo_edit.html
│   │   └── todo_list.html
│   └── diary/
│       ├── diary_add.html
│       ├── diary_detail.html
│       ├── diary_edit.html
│       └── diary_list.html
│
└── static/
    ├── css/
    │   ├── auth.css
    │   ├── calendar.css
    │   ├── common.css
    │   ├── dark.css
    │   ├── dashboard.css
    │   ├── diary.css
    │   ├── layout.css
    │   ├── login.css
    │   └── todo.css
    │
    └── js/
        ├── calendar.js
        ├── common.js
        ├── dashboard.js
        ├── diary.js
        └── todo.js
