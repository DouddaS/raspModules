from flask import Flask, request
from flask_restful import Api
import flask
import os
# import requests

app = Flask(__name__)
API = Api(app)
port = int(os.getenv("PORT", 1092))


# SCREEN_WIDTH = 160
# SCREEN_HIGHT = 120
# BALL_SIZE_MIN = SCREEN_HIGHT/10
# BALL_SIZE_MAX = SCREEN_HIGHT/3


@app.route('/', methods=['GET'])
def decide():
    # docker response = requests.request("POST", url="http://perception_module:1090/")
    # response = requests.request("POST", url="http://perception:1090/")
    # data = response.json()
    # 
    # tmp_r = -2
    # 
    # print('x= ',data['tmp_x'])
    # print('y= ',data['tmp_y'])
    # print('r= ',data['tmp_r'])
    # 
    # if 'tmp_x' in data:
    #     if 'tmp_y' in data:
    #         if 'tmp_r' in data:
    #             tmp_x = data['tmp_x']
    #             tmp_y = data['tmp_y']
    #             tmp_r = data['tmp_r']
    # 
    # print('tmp_x= ',tmp_x)
    # print('tmp_y= ',tmp_y)
    # print('tmp_r= ',tmp_r)

    # if tmp_r == -2 or tmp_r < BALL_SIZE_MIN or tmp_r > BALL_SIZE_MAX:
    # if tmp_r < BALL_SIZE_MIN:

    # Get the arguments
    args = request.get_json(force=True)
    tmp_r = args.get('tmp_r')
    # ou tmp_r = args['tmp_r']

    if tmp_r == -2 or tmp_r > 0:
        reponse = 'STOP!'
    else:
        reponse = 'RAS'

    # print("FROM DECISION MODULE, reponse", reponse)

    verdict = {'rep': reponse}
    verdict = flask.jsonify(verdict)
    verdict.status_code = 200
    return verdict


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
