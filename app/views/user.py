import jwt
from flask import Blueprint, request, jsonify

from app import JWT_SECRET

bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)

@bp.route('', methods=['POST'])
def user_info():
    token_receive = request.headers['authorization']
    token = token_receive.split()[1]
    print(token)

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        print(payload)
        return jsonify({'result': 'success', 'id': payload['id']})
    # jwt 만료되면
    except jwt.exceptions.ExpiredSignatureError:
        # try 부분을 실행했지만 위와 같은 에러가 난다면
        return jsonify({'result': 'fail'})