from schematics import Model
from schematics.types import (
    BooleanType, DictType, FloatType, IntType, ListType, ModelType, StringType
)


class StatusModel(Model):
    status = BooleanType(required=True)


class UserModel(Model):
    id = IntType(required=True)
    name = StringType()
    age = IntType()
    status = BooleanType()
    salary = FloatType()
    titles = ListType(StringType)
    model = ModelType(StatusModel)
    stats = ListType(ModelType(StatusModel))
    stats_dict = DictType(ModelType(StatusModel))


class UserSuccessResponse(Model):
    status = BooleanType(required=True)
    users = ListType(ModelType(UserModel))


class UserErrorResponse(Model):
    status = BooleanType(required=True)
    users = ListType(ModelType(UserModel))
