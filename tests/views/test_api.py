import hashlib

from tests.conftest import db


# def test_로그인(client):



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