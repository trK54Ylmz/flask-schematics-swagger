from flask import make_response, Response


def user_single_summary() -> Response:
    """
    A

    Z

    :response 200 test.schema.user.UserSuccessResponse: successful response
    :response 403 test.schema.user.UserErrorResponse: error response
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
    :parameter body test.schema.user.UserModel user: the user model
    :response 200 test.schema.user.UserSuccessResponse: successful response
    :response 403 test.schema.user.UserErrorResponse: error response
    :return: flask.Response
    """
    return make_response('test')


def user_complex_type() -> Response:
    """
    :parameter query array[integer] a: b
    :parameter query float b: c
    :response 200 array[test.schema.user.UserSuccessResponse]: x
    :return: flask.Response
    """
    return make_response('test')
