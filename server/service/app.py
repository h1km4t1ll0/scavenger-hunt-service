from flask import Flask, jsonify

from service.cache import Cache
from service.environment import get_env
from service.getters import get_leaderboard

from flask_cors import CORS, cross_origin

from service.alert import send_alert

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

get_env()
# env.DATABASE_URL = 'postgresql://postgres:hFwI/MvZJJ[Y2WBq£1,(BN8\[-8Yu5^@45.95.234.124:9856/scavenger_hunt'
leaderboard_cache = Cache(10, get_leaderboard)


@app.route('/v1/leaderboard', methods=['GET'])
@cross_origin()
def get_leaderboard_endpoint():
    try:
        return jsonify(
            {
                'data': leaderboard_cache.get(),
                'code': 200
            }
        )
    except Exception as e:
        send_alert(f'An exception occurred in scavenger-hunt-service!\n\n{str(e)}')
        return jsonify(
            {
                'data': [],
                'code': 500
            }
        )
