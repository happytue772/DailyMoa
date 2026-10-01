from datetime import date

from sqlalchemy import func

from flask import (
    Blueprint,
    render_template,
    session
)

from flask_login import (
    login_required,
    current_user
)

from models import (
    db,
    Todo,
    Diary,
    Schedule
)

from routes.diary import (
    get_daily_question
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route(
    "/dashboard"
)
@login_required
def dashboard():

    today = date.today()


    # =====================================================
    # Dashboard Todo
    # =====================================================

    todos = (
        Todo.query
        .filter_by(
            user_id=current_user.id,
            completed=False
        )
        .order_by(
            Todo.due_date.asc()
        )
        .limit(5)
        .all()
    )


    # =====================================================
    # 오늘 일정
    # =====================================================

    schedules = (
        Schedule.query
        .filter(
            Schedule.user_id
            == current_user.id,

            func.date(
                Schedule.start_datetime
            )
            == today.isoformat()
        )
        .order_by(
            Schedule.start_datetime.asc()
        )
        .all()
    )


    # =====================================================
    # 최근 Diary
    # =====================================================

    diaries = (
        Diary.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Diary.diary_date.desc(),
            Diary.created_at.desc()
        )
        .limit(3)
        .all()
    )


    # =====================================================
    # 오늘 Todo
    # =====================================================

    today_todos = (
        Todo.query
        .filter_by(
            user_id=current_user.id,
            due_date=today
        )
        .all()
    )


    todo_total = len(
        today_todos
    )


    todo_completed = sum(
        1
        for todo in today_todos
        if todo.completed
    )


    # =====================================================
    # 오늘 Diary
    # =====================================================

    today_diary = (
        Diary.query
        .filter_by(
            user_id=current_user.id,
            diary_date=today
        )
        .order_by(
            Diary.created_at.desc()
        )
        .first()
    )


    # =====================================================
    # 하루 마무리 카드
    # =====================================================

    day_summary = {
        "todo_total":
            todo_total,

        "todo_completed":
            todo_completed,

        "schedule_count":
            len(schedules),

        "diary":
            today_diary
    }


    # =====================================================
    # 오늘의 질문
    # =====================================================

    daily_question = (
        get_daily_question()
    )


    # Dashboard와 Diary가
    # 같은 임시 답변을 사용하도록 Key 생성
    question_storage_key = (
        f"dailymoa-question-"
        f"{current_user.id}-"
        f"{today.isoformat()}"
    )


    # =====================================================
    # 로그인 직후 팝업 여부
    # =====================================================

    show_question_popup = session.get(
        "show_daily_question_popup",
        False
    )


    print(
        "오늘의 질문 자동 팝업:",
        show_question_popup
    )


    # 이번 Dashboard에서 한 번 사용했으므로
    # 다음 새로고침부터는 자동 팝업 X
    session[
        "show_daily_question_popup"
    ] = False


    # =====================================================
    # Template
    # =====================================================

    return render_template(
        "dashboard/dashboard.html",

        todos=todos,

        schedules=schedules,

        diaries=diaries,

        day_summary=day_summary,

        daily_question=(
            daily_question
        ),

        question_storage_key=(
            question_storage_key
        ),

        show_question_popup=(
            show_question_popup
        )
    )