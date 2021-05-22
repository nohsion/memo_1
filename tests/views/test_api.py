import hashlib

import jwt

from tests.conftest import db


def test_로그인(client):
    id = 'tester02'
    pw = 'tester02'
    data = {
        'id_give': id,
        'pw_give': pw,
    }

    # 먼저 회원가입
    client.post('/api/register', data=data)
    # 로그인
    response = client.post('api/login', data=data)
    assert response.status_code == 200
    assert response.json['result'] == 'success'

    token = response.json['token']
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    assert payload['id'] == id


def test_회원가입(client):
    id = 'tester01'
    pw = 'tester01'
    data = {
        'id_give': id,
        'pw_give': pw,
    }

    response = client.post(
        '/api/register',
        data=data
    )
    assert response.status_code == 200

    user = db.users.find_one({'id': id}, {'_id': False})
    # 패스워드 평문으로 저장 x
    assert user['pw'] != pw
    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    assert user['pw'] == pw_hash