from flask import Flask
from fss import FlaskSchematicsSwagger, SecurityDefinition

host = 'localhost'
version = '1.0'
title = 'simple'
description = 'description'

security = SecurityDefinition('apikey')
security.api_key('header', 'X-Test')

app = Flask('app')
fss = FlaskSchematicsSwagger(app, host, version, title, description, security)
