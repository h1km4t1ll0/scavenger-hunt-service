from flask import Flask, jsonify

from server.service.cache import Cache
from server.service.environment import get_env, env
from server.service.getters import get_leaderboard

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

get_env()
# env.DATABASE_URL = 'postgresql://postgres:hFwI/MvZJJ[Y2WBq£1,(BN8\[-8Yu5^@45.95.234.124:9856/scavenger_hunt'
leaderboard_cache = Cache(10, get_leaderboard)


@app.route('/v1/leaderboard', methods=['GET'])
@cross_origin()
def get_leaderboard_endpoint():
    return jsonify(
        leaderboard_cache.get()
    )
