import os
# import pandas as pd
import flask
from flask import Flask, request
from flask_restful import Api
import hs_functions_list as hsfl
import statsmodels.api as sm

app = Flask(__name__)
API = Api(app)
port = int(os.getenv("PORT", 1094))


@app.route('/', methods=['GET'])
def predict():
    # Get the arguments
    args = request.get_json(force=True)

    if len(args) > 0:
        series = hsfl.to_df(args)
    else:
        series = hsfl.load_big_csv(50, 'S')
        # series = latency_data.tail(50)
    # Stationarity test
    diff_time = 0
    stat, diff_time = hsfl.i_order(series, 2, diff_time)
    if diff_time > 0:
        # Outliers detection : moving mean
        outliers = hsfl.mov_med_list_outliers(series)
        # Remove the outliers
        if len(outliers) > 0:
            series = hsfl.replace_outliers(series, outliers)
    # Detect the arima orders p & q
    npseries = series.to_numpy()
    p, q = hsfl.arma_order(npseries, diff_time)
    try:
        mod = sm.tsa.statespace.SARIMAX(npseries, order=(p, diff_time, q))
        mod_fitted = mod.fit(disp=False)
        forecasted = mod_fitted.get_forecast()
        predicted = forecasted.predicted_mean[0]
        # res = mod_fitted.resid

    except:
        # pass
        print('     !!! Here exception ARIMA')
        val_m = npseries.mean()
        predicted = val_m

    response = flask.jsonify({'Prediction': predicted})
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
