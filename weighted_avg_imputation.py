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
alphas = [i/100 for i in range(0, 200, 5)]

for alpha in alphas:
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
        pred = utils.optimally_wavg_imputation(nan_idx, miss_arr, alpha)
        
        maes.append(utils.mae(pred, actual))
        rmses.append(utils.rmse(pred, actual))
        r2_scores.append(r2_score(actual, pred))

    print('Alpha:', alpha)
    print('========================================')
    print('MAE:', f'{statistics.mean(maes):.4f}')
    print('RMSE', f'{statistics.mean(rmses):.4f}')
    print('R2', f'{statistics.mean(r2_scores):.4f}')
    print('========================================')
