from schematics import Model
from schematics.types import BooleanType, IntType, ListType, ModelType, StringType


class UserModel(Model):
    id = IntType(required=True)
    name = StringType()
    age = IntType()
    status = BooleanType()


class UserGetResponse(Model):
    status = BooleanType(required=True)
    users = ListType(ModelType(UserModel))
