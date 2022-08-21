from flask import Flask
from fss import SchematicsSwagger
from schema import UserModel, UserGetResponse


app = Flask('app')
ss = SchematicsSwagger(app)


@app.get('/example')
@ss.doc()
def get_users() -> dict:
    """
    Get list of users

    :response 200 schema.UserGetResponse:
    :return: flask response as dictionary
    """
    items = [
        {'id': 1, 'name': 'Test 1', 'age': 20, 'status': True},
        {'id': 2, 'name': 'Test 2', 'age': 30, 'status': False},
    ]

    users = []
    for item in items:
        users.append(UserModel(item))

    response = UserGetResponse()
    response.status = True
    response.users = users

    return response.to_primitive()


if __name__ == '__main__':
    app.run()
