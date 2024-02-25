from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from tqdm import tqdm
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

for i in tqdm(range(len(miss))):
    df_miss = pd.read_csv(miss[i])
    df_full = pd.read_csv(full[i])

    nan_idx = []

    for i in range(len(df_miss)):
        if np.isnan(df_miss.iloc[i, 1]):
            nan_idx.append(i)
    
    pred, actual = [], []

    for idx in nan_idx:
        actual.append(df_full.iloc[idx, 1])
    
    df_miss['DateTime'] = df_miss['DateTime'].apply(utils.convert_datetime_to_num)
    
    X_train, y_train, X_pred = [], [], []

    for i in range(len(df_miss)):
        if i not in nan_idx:
            X_train.append(df_miss.iloc[i, 0])
            y_train.append(df_miss.iloc[i, 1])
        else:
            X_pred.append(df_miss.iloc[i, 0])

    X_train = np.asarray(X_train).reshape(-1, 1)
    X_pred = np.asarray(X_pred).reshape(-1, 1)
    y_train = np.asarray(y_train)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    pred = model.predict(X_pred)

    maes.append(utils.mae(pred, actual))
    rmses.append(utils.rmse(pred, actual))
    r2_scores.append(r2_score(actual, pred))

print('MAE')
print(statistics.mean(maes))
print('RMSE')
print(statistics.mean(rmses))
print('R2')
print(statistics.mean(r2_scores))