from flask import Flask, jsonify, request, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text


# Default JSON encorder 는 set 을 JSON 으로 변환할 수 없음
# 그러므로 JSON encorder 를 오버라이드해서 set 을 list 로 변환해서
# JSON 으로 변환 가능해야 하게 해야함
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def insert_user(user):
    return current_app.db.execute(text("""
        INSERT INTO users (
            name, 
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
    """), user).lastrowid


def get_user(user_id):
    user = current_app.db.execute(text("""
        SELECT 
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id': user_id
    }).fetchone()

    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'profile': user['profile']
    } if user else None


def insert_tweet(user_tweet):
    return current_app.db.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet
        )
    """), user_tweet).rowcount


def insert_follow(user_follow):
    return current_app.db.execute(text("""
        INSERT INTO users_follow_list
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow
        )
    """), user_follow).rowcount


def insert_unfollow(user_unfollow):
    return current_app.db.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
    """), user_unfollow).rowcount


def create_app(test_config = None):
    app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    db = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.db = db

    @app.get('/ping', methods=['GET'])
    def ping():
        return 'pong'

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        new_user = request.json
        new_user_id = insert_user(new_user)
        new_user = get_user(new_user_id)

        return jsonify(new_user)

    @app.route('/tweet', methods=['POST'])
    def tweet():
        user_tweet = request.json
        tweet = user_tweet['tweet']

        if len(tweet) > 300:
            return '300자를 초과했습니다', 400

        insert_tweet(user_tweet)

        return '', 200

    @app.route('/follow', methods=['POST'])
    def follow():
        payload = request.json
        insert_follow(payload)

        return '', 200

    # @app.route('/unfollow', methods=['POST'])
    #
    # @app.route('/timeline/<int:user_id>', methods=['GET'])
    # def timeline(user_id):
    #     return

    return app


