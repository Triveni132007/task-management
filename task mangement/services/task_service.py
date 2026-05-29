from models.task import Task
from config.database import db


def add_task_service(data, user_id):
    """Create a new task for `user_id`.

    Returns a tuple of (response_dict, status_code).
    """
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        user_id=user_id,
    )
    db.session.add(task)
    db.session.commit()

    return {"message": "Task Added"}, 201


def get_tasks_service(user_id):
    """Return a list of task dicts for the given user."""
    tasks = Task.query.filter_by(user_id=user_id).all()

    output = []
    for task in tasks:
        output.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        })

    return output


def get_task_service(task_id, user_id):
    """Return a single task dict or (message, 404) if not found."""
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return {"message": "Task not found"}, 404

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
    }


def update_task_service(task_id, data, user_id):
    """Update title/description for a task."""
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return {"message": "Task not found"}, 404

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)

    db.session.commit()
    return {"message": "Data Updated"}, 200


def delete_task_service(task_id, user_id):
    """Delete a task and return a message and status code."""
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return {"message": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()
    return {"message": "Task deleted"}, 200


def update_task_status_service(task_id, data, user_id):
    """Update only the `status` field on a task with validation."""
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return {"message": "Task not found"}, 404

    allowed_status = [
        "not started",
        "ongoing",
        "completed",
    ]
    status = data.get("status")
    if not status:
        return {"message": "Missing status"}, 400

    status_lower = status.strip().lower()
    if status_lower not in allowed_status:
        return {"message": "Invalid status"}, 400

    # Store status in title case for consistency (e.g. "Not Started")
    task.status = status_lower.title()
    db.session.commit()

    return {"message": "Status updated"}, 200