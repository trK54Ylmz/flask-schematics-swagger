from flask import Blueprint, request
from example.schema import UserModel, UserGetResponse

user = Blueprint('user', '/user')
items = [
    {'id': 1, 'name': 'Test 1', 'age': 20, 'status': True},
    {'id': 2, 'name': 'Test 2', 'age': 30, 'status': False},
]


@user.get('/hello')
def get_users() -> dict:
    """
    Get list of users

    :parameter query integer user_id: the user id filter. default: None
    :response 200 example.schema.response.UserGetResponse:
    :return: flask response as dictionary
    """
    user_id = request.args.get('user_id')

    users = []
    for item in items:
        if user_id is not None and user_id != item['id']:
            continue
        users.append(UserModel(item))

    response = UserGetResponse()
    response.status = True
    response.users = users

    return response.to_primitive()


@user.post('/hi')
def update_user() -> None:
    """
    Update user detail

    User more detailed description

    :parameter body example.schema.request.UserForm user: the user id filter. default: None
    :response 200 None:
    """
    user_id = request.args.get('user_id')
    name = request.args.get('name')

    for item in items:
        if user_id is not None and user_id != item['id']:
            continue
        item['name'] = name

    return '', 204
