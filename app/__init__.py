import os

from dotenv import load_dotenv
from flask import Flask, render_template

from pymongo import MongoClient

# mongoDB 추가
client = MongoClient('localhost', 27017)
db = client.get_database('sparta')

# .env 파일을 환경변수로 설정
load_dotenv()
# 환경변수 읽어오기
JWT_SECRET = os.environ['JWT_SECRET']
CLIENT_ID = os.environ['CLIENT_ID']
CALLBACK_URL = os.environ['CALLBACK_URL']
SERVICE_URL = os.environ['SERVICE_URL']
def create_app():
    # flask Web Server 생성하기
    app = Flask(__name__)

    from app.views import api
    from app.views import memo
    from app.views import main
    from app.views import user

    app.register_blueprint(api.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(memo.bp)
    app.register_blueprint(user.bp)

    return app