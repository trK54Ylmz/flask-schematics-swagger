from blueprint.app import app, ss
from blueprint.user import user


app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    ss.add_route()
    app.run()
