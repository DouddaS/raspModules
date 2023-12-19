# Author: Henda Sfx

# Import libraries
import pandas as pd
import numpy as np
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm


# Load a csv file with a given nb rows and frequence
def load_big_csv(nb, frequence):
    df = pd.read_csv('./data/dataset.csv', sep=';', usecols=['Latency_Edge2'], nrows=nb, encoding="utf-8")

    df.columns = ['Latencies']

    now = datetime(2020, 1, 1, 1, 0, 0).strftime('%Y-%m-%d %H:%M:%S')

    df["Time"] = pd.date_range(pd.to_datetime(now), periods=nb, freq=frequence)

    df.set_index("Time", inplace=True)

    df = df.asfreq(pd.infer_freq(df.index))

    return df


# Stationarity tests :
# ADF
# Return true or false
def adf_test(series, reg):
    result = adfuller(series, regression=reg)

    p_value = result[1]

    return False if p_value > 0.05 else True


# Displays the ADFULLER results
def adf_test_display(series, reg):
    result = adfuller(series, regression=reg)

    return result[1]


# Detect outliers
def mov_med_list_outliers(series):
    # Dataframe to store the mov med results
    df_movmed_res = pd.DataFrame(columns=['Window', 'Std', 'Nb_Out', 'Outliers'])
    df_movmed_res.style.hide_index()
    i_movmed_res = 0

    maxout = 0
    wout = 0

    vout = 2

    v = 2

    res = []

    for w in range(2, 5):
        # for v in range(1,4):

        # Calculate rolling median/mean and std
        series['mov_avg'] = series['Latencies'].rolling(window=w).median()
        series['std'] = series['Latencies'].rolling(window=w).std()

        # Calculate the thresholds
        up_th = series['Latencies'].median() + v * series['Latencies'].std()
        low_th = series['Latencies'].median() - v * series['Latencies'].std()

        # Filter setup to mark the flags to be dropped
        series['drop_flag'] = np.where((series['Latencies'] <= up_th) & (series['Latencies'] >= low_th), 0, 1)

        # Get and print the outliers indexes
        outl_idx = [i for i in range(len(series['drop_flag'])) if series['drop_flag'][i] == 1]

        if len(outl_idx) <= (len(series) * 0.1):

            # Add a result to the dataframe
            df_movmed_res.loc[i_movmed_res] = ([w, v, len(outl_idx), outl_idx])
            i_movmed_res += 1

            if maxout < len(outl_idx):
                maxout = len(outl_idx)
                wout = w
                # vout = v

    if maxout > 0:
        # arrayList type for outliers
        outliers = df_movmed_res.loc[(df_movmed_res['Nb_Out'] == maxout) & (df_movmed_res['Window'] == wout) & (
                df_movmed_res['Std'] == vout), 'Outliers'].values

        res = list(map(int, outliers[0]))

    # Remove the extra columns
    series.drop(['mov_avg', 'std', 'drop_flag'], axis=1, inplace=True)

    return res


# REPLACEMENT BY MEDIAN
def replace_outliers(series, outliers_idx):
    x = series.median()

    for outl in outliers_idx:
        series.loc[series.index[outl], 'Latencies'] = x[0]

    # Re-assign the frequency
    series = series.asfreq(freq='S')

    return series


# Hyper parameters grid search
def arma_order(series, diff_time):
    # Starting AIC, p, and q.
    best_aic = 999999
    # best_bic = 0
    best_p = 0
    best_q = 0
    # Iterating over values of p and q.

    # From 5 -> 4
    for p in range(4):
        for q in range(4):
            try:
                # Fitting an ARIMA(p, 0, q) model.
                # print(f'Attempting to fit ARIMA({p}, 0, {q}) model.')

                if p != 0 or p != 0:

                    # Create the autoregression model
                    # model = ARIMA(series, order=(p, diff_time, q))
                    # Fit the model
                    # model_fitted = model.fit()
                    # model_fitted = model.fit(method='innovations_mle', low_memory=True, cov_type='none')
                    # thisaic = model_fitted.aic

                    mod = sm.tsa.statespace.SARIMAX(series, order=(p, diff_time, q))
                    mod_fitted = mod.fit(disp=False)
                    thisaic = mod_fitted.aic

                    # Is my current model's AIC better than our best_aic?
                    if thisaic < best_aic and not (p == 0 and q == 0):  # and model.bic < best_bic:
                        # If so, let's overwrite best_aic, best_p, and best_q.
                        best_aic = thisaic
                        # best_bic = model.bic
                        best_p = p
                        best_q = q
            except:
                pass
    return best_p, best_q


# def launchGARCH(series, gp, gq):
# garch = arch.arch_model(series, p=gp, q=gq)
# garch_model = garch.fit()

# garch_forecast = garch_model.forecast(horizon=1)
# predictions = garch_forecast.variance['h.1'].iloc[-1]

# return predictions


# LOULOU
def i_order(series, times, d):
    # Check whether the series is stationary
    stationary = adf_test(series, 'c')
    if (stationary is False) and (d < times):
        # Increment the differentiation order
        d += 1
        # Differentiate the series term by term (S[i+1] = S[i+1] - S[i])
        series = series.diff()
        # Reject the first element as not differentiated (S[0] = S[0] - S[-1] !)
        series = series[1:].copy()
        # Check whether the differentiated series is stationary otherwise
        # differentiate again (as long as the maximum times of differentiations
        # is not reached)
        stationary, d = i_order(series, times, d)

    return stationary, d


# Converts a list to a dataframe with time index
def to_df(list_json):
    df = pd.DataFrame({'Latencies': list_json})

    now = datetime(2020, 1, 1, 1, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
    df["Time"] = pd.date_range(pd.to_datetime(now), periods=len(list_json), freq='S')
    df.set_index("Time", inplace=True)
    df = df.asfreq(pd.infer_freq(df.index))

    return df
