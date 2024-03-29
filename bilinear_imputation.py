from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import statistics
import utils
import glob

full = sorted(glob.glob('./data/london_dataset/full_*'))
miss = sorted(glob.glob('./data/london_dataset/miss_*'))

maes, mapes, rmses, rmspes, r2_scores = [], [], [], [], [] 

for i in range(len(miss)):
    df_miss = pd.read_csv(miss[i])['KWh']
    df_full = pd.read_csv(full[i])['KWh']
    miss_arr = pd.to_numeric(df_miss, errors='coerce').to_numpy()
    full_arr = pd.to_numeric(df_full, errors='coerce').to_numpy()

    nan_idx, actual = [], []

    for idx in range(len(miss_arr)):
        if np.isnan(miss_arr[idx]):
            nan_idx.append(idx)
    
    for idx in nan_idx:
        actual.append(full_arr[idx])
    pred = utils.bilinear_imputation(nan_idx, miss_arr)

    maes.append(utils.mae(actual, pred))
    mapes.append(utils.mape(actual, pred))
    rmses.append(utils.rmse(actual, pred))
    rmspes.append(utils.rmspe(actual, pred))
    r2_scores.append(r2_score(actual, pred))


print('MAE')
print(statistics.mean(maes))
print('MAPE')
print(statistics.mean(mapes))
print('RMSE')
print(statistics.mean(rmses))
print('RMSPE')
print(statistics.mean(rmspes))
print('R2')
print(statistics.mean(r2_scores))