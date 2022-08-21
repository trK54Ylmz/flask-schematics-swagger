from flask import Flask
from fss import FlaskSchematicsSwagger

app = Flask('app')
fss = FlaskSchematicsSwagger(app)
