from flask import Flask
from fss import FlaskSchematicsSwagger

app = Flask('app')
fss = FlaskSchematicsSwagger(app, 'localhost', '1.0', 'simple', 'description', '/documentation')
