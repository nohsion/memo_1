import jwt
from flask import Blueprint, request, render_template

from app import JWT_SECRET, db, CLIENT_ID, CALLBACK_URL, SERVICE_URL

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


@bp.route('/login', methods=['GET'])
def login():
    return render_template(
        'login.html',
        CLIENT_ID=CLIENT_ID,
        CALLBACK_URL=CALLBACK_URL,
        SERVICE_URL=SERVICE_URL
    )


@bp.route('/naver', methods=['GET'])
def callback():
    return render_template('callback.html', CLIENT_ID=CLIENT_ID, CALLBACK_URL=CALLBACK_URL)


@bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')