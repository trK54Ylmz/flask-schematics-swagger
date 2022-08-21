from flask import make_response, Response


def user_single_summary() -> Response:
    """
    A

    Z

    :response 200 test.schema.UserSuccessResponse: successful response
    :response 403 test.schema.UserErrorResponse: error response
    :return: flask.Response
    """
    return make_response('test')


def user_multi_summary() -> Response:
    """
    A
    B

    Y
    Z

    :parameter query integer user_id: the user id filter. default: None
    :parameter body test.schema.UserModel user: the user model
    :response 200 test.schema.UserSuccessResponse: successful response
    :response 403 test.schema.UserErrorResponse: error response
    :return: flask.Response
    """
    return make_response('test')
