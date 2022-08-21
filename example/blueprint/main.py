from blueprint.app import app, fss
from blueprint.user import user

app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    fss.add_route()
    app.run()
