from schematics import Model
from schematics.types import (
    BooleanType, FloatType, IntType, ListType, ModelType, StringType
)


class UserModel(Model):
    id = IntType(required=True)
    name = StringType()
    age = IntType()
    status = BooleanType()
    salary = FloatType()


class UserSuccessResponse(Model):
    status = BooleanType(required=True)
    users = ListType(ModelType(UserModel))


class UserErrorResponse(Model):
    status = BooleanType(required=True)
    users = ListType(ModelType(UserModel))
