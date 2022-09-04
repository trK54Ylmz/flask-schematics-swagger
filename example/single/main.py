from flask import Flask, request
from fss import FlaskSchematicsSwagger, SecurityDefinition
from example.schema import UserModel, UserGetResponse

host = 'localhost'
version = '1.0'
title = 'simple'
description = 'description'
base = '/api/v1'
route = '/doc'

app = Flask('app')
sec = SecurityDefinition('basic_auth').basic()
fss = FlaskSchematicsSwagger(app, host, version, title, description, sec, base, route)


@app.get('/api/v1/example')
def get_users() -> dict:
    """
    Get list of users

    :parameter query integer user_id: the user id filter. default: None
    :response 200 example.schema.response.UserGetResponse:
    :return: flask response as dictionary
    """
    user_id = request.args.get('user_id')

    items = [
        {'id': 1, 'name': 'Test 1', 'age': 20, 'status': True},
        {'id': 2, 'name': 'Test 2', 'age': 30, 'status': False},
    ]

    users = []
    for item in items:
        if user_id is not None and user_id != item['id']:
            continue
        users.append(UserModel(item))

    response = UserGetResponse()
    response.status = True
    response.users = users

    return response.to_primitive()


if __name__ == '__main__':
    fss.add_route()
    app.run()
