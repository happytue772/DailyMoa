from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from models import db, Schedule


schedule_bp = Blueprint(
    "schedule",
    __name__
)


@schedule_bp.route("/calendar")
@login_required
def calendar():

    return render_template(
        "calendar/calendar.html"
    )

@schedule_bp.route(
    "/api/schedules/<int:schedule_id>",
    methods=["PUT"]
)
@login_required
def schedule_update(schedule_id):

    schedule = Schedule.query.filter_by(
        id=schedule_id,
        user_id=current_user.id
    ).first_or_404()


    data = request.get_json()


    if not data.get("title"):
        return jsonify({
            "message": "제목이 필요합니다."
        }), 400


    if not data.get("start"):
        return jsonify({
            "message": "시작 시간이 필요합니다."
        }), 400


    schedule.title = data["title"]

    schedule.content = (
        data.get("content")
        or ""
    )

    schedule.start_datetime = (
        datetime.fromisoformat(
            data["start"]
        )
    )


    schedule.end_datetime = (
        datetime.fromisoformat(
            data["end"]
        )

        if data.get("end")

        else None
    )


    db.session.commit()


    return jsonify({
        "message":
            "일정이 수정되었습니다."
    })

@schedule_bp.route("/api/schedules")
@login_required
def schedules():

    schedules = Schedule.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify([
        {
            "id": schedule.id,
            "title": schedule.title,
            "start": schedule.start_datetime.isoformat(),
            "end": (
                schedule.end_datetime.isoformat()
                if schedule.end_datetime
                else None
            ),
            "extendedProps": {
                "content": schedule.content or ""
            }
        }

        for schedule in schedules
    ])


@schedule_bp.route("/api/schedules", methods=["POST"])
@login_required
def schedule_add():

    data = request.get_json()

    schedule = Schedule(
        user_id=current_user.id,
        title=data["title"],
        content=data.get("content"),
        start_datetime=datetime.fromisoformat(
            data["start"]
        ),
        end_datetime=(
            datetime.fromisoformat(data["end"])
            if data.get("end")
            else None
        )
    )

    db.session.add(schedule)
    db.session.commit()

    return jsonify({
        "message": "일정 등록 완료"
    })


@schedule_bp.route("/api/schedules/<int:schedule_id>",methods=["DELETE"])
@login_required
def schedule_delete(schedule_id):

    schedule = Schedule.query.filter_by(
        id=schedule_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(schedule)
    db.session.commit()

    return jsonify({
        "message": "일정 삭제 완료"
    })