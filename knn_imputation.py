from sklearn.impute import KNNImputer
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import statistics
import utils
import glob

full = sorted(glob.glob('./data/london_dataset/full_*'))
miss = sorted(glob.glob('./data/london_dataset/miss_*'))

maes = []
rmses = []
r2_scores = []
n_neighbours = 5

for i in range(len(miss)):
    df_miss = pd.read_csv(miss[i])['KWh']
    df_full = pd.read_csv(full[i])['KWh']
    miss_arr = pd.to_numeric(df_miss, errors='coerce').to_numpy().reshape(-1, 1)
    full_arr = pd.to_numeric(df_full, errors='coerce').to_numpy()

    nan_idx = []

    for idx in range(len(miss_arr)):
        if np.isnan(miss_arr[idx]):
            nan_idx.append(idx)

    imputer = KNNImputer(n_neighbors=n_neighbours)
    final = imputer.fit_transform(miss_arr)

    pred, actual = [], []

    for idx in nan_idx:
        pred.append(final[idx])
        actual.append(full_arr[idx])

    maes.append(utils.mae(pred, actual))
    rmses.append(utils.rmse(pred, actual))
    r2_scores.append(r2_score(actual, pred))

print('MAE')
print(statistics.mean(maes))
print('RMSE')
print(statistics.mean(rmses))
print('R2')
print(statistics.mean(r2_scores))