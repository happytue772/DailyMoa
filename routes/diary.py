from datetime import datetime, date

from sqlalchemy import or_

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from models import (
    db,
    Diary,
    ImportantDiary
)


diary_bp = Blueprint(
    "diary",
    __name__,
    url_prefix="/diary"
)


# =========================================================
# 오늘의 질문
# =========================================================

DAILY_QUESTIONS = [
    "오늘 가장 기억에 남는 순간은 무엇인가요?",
    "오늘 나를 웃게 만든 일은 무엇인가요?",
    "오늘 가장 감사했던 일은 무엇인가요?",
    "오늘 조금 아쉬웠던 순간은 무엇인가요?",
    "오늘 내가 잘했다고 생각하는 일은 무엇인가요?",
    "오늘 새롭게 알게 된 것은 무엇인가요?",
    "오늘 가장 편안했던 순간은 언제였나요?",
    "내일의 나에게 한마디를 남긴다면?",
    "오늘 나에게 가장 필요했던 것은 무엇인가요?",
    "오늘 하루를 한 문장으로 표현한다면?"
]


def get_daily_question():

    index = (
        date.today().toordinal()
        % len(DAILY_QUESTIONS)
    )

    return DAILY_QUESTIONS[index]


# =========================================================
# Diary 목록
# 검색 + 기분 + 중요 기록 필터
# =========================================================

@diary_bp.route("/")
@login_required
def diary_list():

    keyword = request.args.get(
        "q",
        ""
    ).strip()

    selected_mood = request.args.get(
        "mood",
        "all"
    )

    only_important = (
        request.args.get(
            "important",
            "0"
        )
        == "1"
    )


    query = Diary.query.filter_by(
        user_id=current_user.id
    )


    # 제목 / 내용 검색
    if keyword:

        query = query.filter(
            or_(
                Diary.title.ilike(
                    f"%{keyword}%"
                ),
                Diary.content.ilike(
                    f"%{keyword}%"
                )
            )
        )


    # 기분 필터
    if selected_mood != "all":

        query = query.filter(
            Diary.mood == selected_mood
        )


    # 중요 기록만
    if only_important:

        query = (
            query
            .join(
                ImportantDiary,
                ImportantDiary.diary_id
                == Diary.id
            )
            .filter(
                ImportantDiary.user_id
                == current_user.id
            )
        )


    diaries = (
        query
        .order_by(
            Diary.diary_date.desc(),
            Diary.created_at.desc()
        )
        .all()
    )


    # 현재 사용자의 중요 기록 ID
    important_rows = (
        ImportantDiary.query
        .filter_by(
            user_id=current_user.id
        )
        .all()
    )


    important_ids = {
        row.diary_id
        for row in important_rows
    }


    return render_template(
        "diary/diary_list.html",
        diaries=diaries,
        keyword=keyword,
        selected_mood=selected_mood,
        only_important=only_important,
        important_ids=important_ids
    )


# =========================================================
# Diary 추가
# =========================================================

@diary_bp.route(
    "/add",
    methods=["GET", "POST"]
)
@login_required
def diary_add():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        mood = request.form.get(
            "mood",
            ""
        ).strip()

        happiness_score_text = (
            request.form.get(
                "happiness_score",
                ""
            ).strip()
        )

        diary_date_text = (
            request.form.get(
                "diary_date",
                ""
            ).strip()
        )


        if (
            not title
            or not content
            or not mood
            or not happiness_score_text
            or not diary_date_text
        ):

            flash(
                "모든 필수 항목을 입력해주세요."
            )

            return redirect(
                url_for(
                    "diary.diary_add"
                )
            )


        try:

            happiness_score = int(
                happiness_score_text
            )

        except ValueError:

            flash(
                "행복 점수는 숫자로 입력해주세요."
            )

            return redirect(
                url_for(
                    "diary.diary_add"
                )
            )


        if not 1 <= happiness_score <= 10:

            flash(
                "행복 점수는 1~10점 사이여야 합니다."
            )

            return redirect(
                url_for(
                    "diary.diary_add"
                )
            )


        try:

            diary_date = datetime.strptime(
                diary_date_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            flash(
                "올바른 날짜를 입력해주세요."
            )

            return redirect(
                url_for(
                    "diary.diary_add"
                )
            )


        diary = Diary(
            user_id=current_user.id,
            title=title,
            content=content,
            mood=mood,
            happiness_score=happiness_score,
            diary_date=diary_date
        )


        db.session.add(diary)

        db.session.commit()


        flash(
            "일기가 저장되었습니다."
        )


        return redirect(
            url_for(
                "diary.diary_list"
            )
        )


    question_storage_key = (
    f"dailymoa-question-"
    f"{current_user.id}-"
    f"{date.today().isoformat()}"
)


    return render_template(
    "diary/diary_add.html",

    daily_question=(
        get_daily_question()
    ),

    question_storage_key=(question_storage_key)
)


# =========================================================
# 감정 Calendar API
# =========================================================

@diary_bp.route("/api/moods")
@login_required
def diary_mood_events():

    diaries = (
        Diary.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Diary.diary_date.asc()
        )
        .all()
    )


    events = []


    for diary in diaries:

        mood = diary.mood or ""


        if "행복" in mood:
            mood_class = "mood-happy"

        elif "좋음" in mood:
            mood_class = "mood-good"

        elif "보통" in mood:
            mood_class = "mood-normal"

        elif "슬픔" in mood:
            mood_class = "mood-sad"

        elif "화남" in mood:
            mood_class = "mood-angry"

        else:
            mood_class = "mood-normal"


        events.append(
            {
                "id": f"diary-{diary.id}",

                "title": diary.mood,

                "start":
                    diary.diary_date.isoformat(),

                "allDay": True,

                "classNames": [
                    "diary-mood-event",
                    mood_class
                ],

                "extendedProps": {
                    "type": "diary",

                    "detailUrl":
                        url_for(
                            "diary.diary_detail",
                            diary_id=diary.id
                        ),

                    "score":
                        diary.happiness_score
                }
            }
        )


    return jsonify(events)


# =========================================================
# Diary 상세
# =========================================================

@diary_bp.route(
    "/<int:diary_id>"
)
@login_required
def diary_detail(
    diary_id
):

    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=current_user.id
    ).first_or_404()


    important = (
        ImportantDiary.query
        .filter_by(
            user_id=current_user.id,
            diary_id=diary.id
        )
        .first()
    )


    return render_template(
        "diary/diary_detail.html",
        diary=diary,
        is_important=(
            important is not None
        )
    )


# =========================================================
# 중요 기록 등록 / 해제
# =========================================================

@diary_bp.route(
    "/<int:diary_id>/important",
    methods=["POST"]
)
@login_required
def diary_toggle_important(
    diary_id
):

    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=current_user.id
    ).first_or_404()


    important = (
        ImportantDiary.query
        .filter_by(
            user_id=current_user.id,
            diary_id=diary.id
        )
        .first()
    )


    # 이미 중요 기록이면 제거
    if important:

        db.session.delete(
            important
        )


    # 아니라면 새로 등록
    else:

        important = ImportantDiary(
            user_id=current_user.id,
            diary_id=diary.id
        )

        db.session.add(
            important
        )


    db.session.commit()


    return redirect(
        url_for(
            "diary.diary_detail",
            diary_id=diary.id
        )
    )


# =========================================================
# Diary 수정
# =========================================================

@diary_bp.route(
    "/<int:diary_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def diary_edit(
    diary_id
):

    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=current_user.id
    ).first_or_404()


    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        mood = request.form.get(
            "mood",
            ""
        ).strip()

        happiness_score_text = (
            request.form.get(
                "happiness_score",
                ""
            ).strip()
        )

        diary_date_text = (
            request.form.get(
                "diary_date",
                ""
            ).strip()
        )


        if (
            not title
            or not content
            or not mood
            or not happiness_score_text
            or not diary_date_text
        ):

            flash(
                "모든 필수 항목을 입력해주세요."
            )

            return redirect(
                url_for(
                    "diary.diary_edit",
                    diary_id=diary.id
                )
            )


        try:

            happiness_score = int(
                happiness_score_text
            )

        except ValueError:

            flash(
                "행복 점수는 숫자로 입력해주세요."
            )

            return redirect(
                url_for(
                    "diary.diary_edit",
                    diary_id=diary.id
                )
            )


        if not 1 <= happiness_score <= 10:

            flash(
                "행복 점수는 1~10점 사이여야 합니다."
            )

            return redirect(
                url_for(
                    "diary.diary_edit",
                    diary_id=diary.id
                )
            )


        try:

            diary_date = datetime.strptime(
                diary_date_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            flash(
                "올바른 날짜를 입력해주세요."
            )

            return redirect(
                url_for(
                    "diary.diary_edit",
                    diary_id=diary.id
                )
            )


        diary.title = title
        diary.content = content
        diary.mood = mood

        diary.happiness_score = (
            happiness_score
        )

        diary.diary_date = (
            diary_date
        )


        db.session.commit()


        flash(
            "일기가 수정되었습니다."
        )


        return redirect(
            url_for(
                "diary.diary_detail",
                diary_id=diary.id
            )
        )


    return render_template(
        "diary/diary_edit.html",
        diary=diary
    )


# =========================================================
# Diary 삭제
# =========================================================

@diary_bp.route(
    "/<int:diary_id>/delete",
    methods=["POST"]
)
@login_required
def diary_delete(
    diary_id
):

    diary = Diary.query.filter_by(
        id=diary_id,
        user_id=current_user.id
    ).first_or_404()


    # 중요 기록부터 삭제
    ImportantDiary.query.filter_by(
        user_id=current_user.id,
        diary_id=diary.id
    ).delete()


    db.session.delete(
        diary
    )

    db.session.commit()


    flash(
        "일기가 삭제되었습니다."
    )


    return redirect(
        url_for(
            "diary.diary_list"
        )
    )