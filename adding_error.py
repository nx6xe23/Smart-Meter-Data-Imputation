import pandas as pd
import numpy as np
import random, utils


seed = 123
mean, var = 56.19-1, 61508.03
log_mu, log_sigma = utils.lognorm_params(mean, var)
total_p = 0.01
rand_p, clus_p = total_p * 0.2, (total_p * 0.8)/(mean+1)

random.seed(seed)

df = pd.read_csv('./data/agg_168_data.csv')
df = df.drop(df[df['KWh'] == 'Null'].index)
idx_to_nan = []
# Creating clusters of missing datapoints
num_clus = int(len(df) * clus_p) + random.randint(-int(len(df) * clus_p * 0.1), int(len(df) * clus_p * 0.1))
for j in range(num_clus):
    length = int(np.ceil(random.lognormvariate(mu = log_mu, sigma = log_sigma))+1)
    while True:
        conflict = False
        idx_sample = random.randint(0, len(df) - length)
        for idx in range(idx_sample, idx_sample + length):
            if idx in idx_to_nan or idx-1 in idx_to_nan or idx+1 in idx_to_nan:
                conflict = True
                break
        if not conflict:
            for idx in range(idx_sample, idx_sample + length):
                idx_to_nan.append(idx)
            break

# Creating random missing datapoints
num_rand = int(len(df) * rand_p) + random.randint(-int(len(df) * rand_p * 0.1), int(len(df) * rand_p * 0.1))
for j in range(num_rand):
    while True:
        idx = random.randint(0, len(df) - length)
        if idx in idx_to_nan or idx-1 in idx_to_nan or idx+1 in idx_to_nan:
            continue
        idx_to_nan.append(idx)
        break

for idx in idx_to_nan:
    df.iloc[idx, 1] = np.nan

df.to_csv('./data/missing_agg_168_data.csv', index=False)