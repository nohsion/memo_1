import jwt
from flask import Blueprint, request, render_template



bp = Blueprint(
    'main',
    __name__,
    url_prefix='/',
)

@bp.route('/', methods=['GET'])  # 데코레이터 문법 @
def index():
    token = request.cookies.get('loginToken')

    if token:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            print(payload)
            memos = list(db.articles.find({'id': payload['id']}, {'_id': False}))
        # 쿠키
        except jwt.exceptions.ExpiredSignatureError:
            memos = []

    else:
        memos = []

    return render_template('index.html', test='테스트', memos=memos)