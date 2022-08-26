from flask import make_response, Response


def user_single_summary() -> Response:
    """
    A

    Z

    :response 200 test.schema.response.UserSuccessResponse: successful response
    :response 403 test.schema.response.UserErrorResponse: error response
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
    :parameter body test.schema.request.UserRequest user: the user form
    :response 200 test.schema.response.UserSuccessResponse: successful response
    :response 403 test.schema.response.UserErrorResponse: error response
    :return: flask.Response
    """
    return make_response('test')


def user_complex_type() -> Response:
    """
    :parameter query array[integer] a: b
    :parameter query float b: c
    :response 200 array[test.schema.response.UserSuccessResponse]: x
    :return: flask.Response
    """
    return make_response('test')
