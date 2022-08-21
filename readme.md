### Flask Schematics Swagger

Flask Swagger generator for Schematics models.

#### Install

Install library by using `pip` command,

```bash
$ pip3 install flask-schematics-swagger
```

#### Usage

```python
from flask import Flask, request
from fss import FlaskSchematicsSwagger

app = Flask('app')
fss = FlaskSchematicsSwagger(app)


@app.get('/users')
def get_users() -> dict:
    """
    Get list of users

    :parameter query integer user_id: the user id filter. default: None
    :response 200 schema.UserGetResponse:
    :return: flask response as dictionary
    """
    user_id = request.args.get('user_id')

    # ...

    return response.to_primitive()


if __name__ == '__main__':
    fss.add_route()
    app.run()
```
