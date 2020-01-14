from flask import jsonify


def bad_request(message, *, status_code=400):
    response = jsonify({'message': message})
    response.status_code = status_code
    return response


def response_400(message):
    return bad_request(message, status_code=400)


def response_404(message):
    return bad_request(message, status_code=404)


def response_500(message):
    return bad_request(message, status_code=500)
