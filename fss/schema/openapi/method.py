from .route import OpenApiRouteSchema
from schematics import Model
from schematics.types import ModelType


class OpenApiMethodSchema(Model):
    get_method = ModelType(OpenApiRouteSchema, serialized_name='get')
    post_method = ModelType(OpenApiRouteSchema, serialized_name='post')
    patch_method = ModelType(OpenApiRouteSchema, serialized_name='patch')
    delete_method = ModelType(OpenApiRouteSchema, serialized_name='delete')
