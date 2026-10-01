from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from models import db, Todo


todo_bp = Blueprint(
    "todo",
    __name__,
    url_prefix="/todo"
)


@todo_bp.route("/")
@login_required
def todo_list():

    todos = Todo.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Todo.completed.asc(),
        Todo.due_date.asc()
    ).all()

    return render_template(
        "todo/todo_list.html",
        todos=todos
    )


@todo_bp.route("/add", methods=["GET", "POST"])
@login_required
def todo_add():

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")
        priority = request.form.get("priority")

        due_date_text = request.form.get("due_date")

        due_date = None

        if due_date_text:
            due_date = datetime.strptime(
                due_date_text,
                "%Y-%m-%d"
            ).date()

        todo = Todo(
            user_id=current_user.id,
            title=title,
            content=content,
            due_date=due_date,
            priority=priority
        )

        db.session.add(todo)
        db.session.commit()

        return redirect(
            url_for("todo.todo_list")
        )

    return render_template(
        "todo/todo_add.html"
    )


@todo_bp.route("/<int:todo_id>/edit", methods=["GET", "POST"])
@login_required
def todo_edit(todo_id):

    todo = Todo.query.filter_by(
        id=todo_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        todo.title = request.form.get("title")
        todo.content = request.form.get("content")
        todo.priority = request.form.get("priority")

        due_date_text = request.form.get("due_date")

        if due_date_text:
            todo.due_date = datetime.strptime(
                due_date_text,
                "%Y-%m-%d"
            ).date()
        else:
            todo.due_date = None

        db.session.commit()

        return redirect(
            url_for("todo.todo_list")
        )

    return render_template(
        "todo/todo_edit.html",
        todo=todo
    )


@todo_bp.route("/<int:todo_id>/complete", methods=["POST"])
@login_required
def todo_complete(todo_id):

    todo = Todo.query.filter_by(
        id=todo_id,
        user_id=current_user.id
    ).first_or_404()

    todo.completed = not todo.completed

    db.session.commit()

    return redirect(
        url_for("todo.todo_list")
    )


@todo_bp.route("/<int:todo_id>/delete", methods=["POST"])
@login_required
def todo_delete(todo_id):

    todo = Todo.query.filter_by(
        id=todo_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(todo)
    db.session.commit()

    return redirect(
        url_for("todo.todo_list")
    )