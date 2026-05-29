from flask import Blueprint, request, jsonify
from middleware.jwt_middleware import token_required

from services.task_service import (
    add_task_service,
    get_tasks_service,
    update_task_service,
    delete_task_service,
    update_task_status_service
)

task_bp = Blueprint('task', __name__)


# ADD TASK
@task_bp.route('/', methods=['POST'])
@token_required
def add_task():

    user_id = request.user_id

    response, status = add_task_service(
        request.json,
        user_id
    )

    return jsonify(response), status


# GET ALL TASKS
@task_bp.route('/', methods=['GET'])
@token_required
def get_tasks():

    user_id = request.user_id

    response = get_tasks_service(user_id)

    return jsonify(response), 200


# UPDATE TASK
@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):

    user_id = request.user_id

    response, status = update_task_service(
        task_id,
        request.json,
        user_id
    )

    return jsonify(response), status


# DELETE TASK
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):

    user_id = request.user_id

    response, status = delete_task_service(
        task_id,
        user_id
    )

    return jsonify(response), status


# UPDATE TASK STATUS
@task_bp.route('/<int:task_id>/status', methods=['PATCH'])
@token_required
def update_task_status(task_id):

    user_id = request.user_id

    response, status = update_task_status_service(
        task_id,
        request.json,
        user_id
    )

    return jsonify(response), status