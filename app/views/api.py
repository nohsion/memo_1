import datetime
import hashlib
import re

import jwt
from flask import Blueprint, request, jsonify

from app import db, JWT_SECRET

bp = Blueprint(
    'api',  # 블루프린트 이름
    __name__,  # 파일 등록(현재 파일)
    url_prefix='/api',  # 패스 접두사
)


@bp.route('/register/naver', methods=['POST'])
def api_register_naver():
    naver_id = request.form['naver_id']
    if not db.users.find_one({'id': naver_id}, {'_id': False}):
        db.users.insert_one({'id': naver_id, 'pw': ''})
    # JWT 발급
    expiration_time = datetime.timedelta(hours=1)
    payload = {
        'id': naver_id,
        'exp': datetime.datetime.utcnow() + expiration_time
    }
    token = jwt.encode(payload, JWT_SECRET)
    print(token)
    return jsonify({'result': 'success', 'token': token})


@bp.route('/login', methods=['POST'])
def api_login():
    id = request.form['id_give']
    pw = request.form['pw_give']

    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    user = db.users.find_one({'id': id, 'pw': pw_hash}, {'_id': False})

    # 만약 가입했다면
    if user:
        # JWT 생성
        expiration_time = datetime.timedelta(hours=1)
        payload = {
            'id': id,
            # 발급시간으로부터 1시간동안 JWT 유효
            'exp': datetime.datetime.utcnow() + expiration_time
        }
        token = jwt.encode(payload, JWT_SECRET)
        print(token)

        return jsonify({'result': 'success', 'token': token})

    # 가입하지 않은 상태
    else:
        return jsonify({'result': 'fail', 'msg': '실패'})

    # < salting >
    # 1. pw + 랜덤 문자열 추가(salt)
    # 솔트 추가된 비밀번호를 해시
    # DB에 저장할 때는 (해시 결과물 + 적용한 솔트) 묶어서 저장

@bp.route('/register', methods=['POST'])
def api_register():
    id = request.form['id_give']
    pw = request.form['pw_give']

    if db.users.find_one({'id': id}, {'_id': False}):
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 아이디입니다'})

    # id 유효성 검사
    if checkisEmpty(id):
        return jsonify({'result': 'fail', 'msg': '아이디를 입력해주세요'})
    if checkSpace(id):
        return jsonify({'result': 'fail', 'msg': '아이디에 공백이 있으면 안됩니다'})
    if checkUserID(id):
        return jsonify({'result': 'fail', 'msg': '아이디는 영문 대소문자와 숫자 4~12자리로 입력해야합니다!'})

    # pw 유효성 검사
    if checkisEmpty(pw):
        return jsonify({'result': 'fail', 'msg': '패스워드를 입력해주세요'})
    if checkSpace(pw):
        return jsonify({'result': 'fail', 'msg': '패스워드에 공백이 있으면 안됩니다'})

    # 회원가입
    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    db.users.insert_one({'id': id, 'pw': pw_hash})

    return jsonify({'result': 'success'})

def checkisEmpty(value):
    if not value:
        return True

def checkSpace(value):
    t = value.split(" ")
    if len(t) > 1:
        return True

def checkUserID(id):
    idRegExp = '[a-zA-z0-9]{4,12}'
    try:
        re.match(idRegExp, id).group()
    except AttributeError:
        return True

def checkUserPW(pw):
    if len(pw) < 8:
        return False
