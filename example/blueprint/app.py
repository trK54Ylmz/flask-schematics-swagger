from flask import Flask
from fss import SchematicsSwagger


app = Flask('app')
ss = SchematicsSwagger(app)
