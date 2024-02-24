from tqdm import tqdm
import pandas as pd
import numpy as np
import random
import utils
import os


file = open('./data/london_data/complete_households.txt')
complete_hh = [i.split('\n')[0] for i in file.readlines()]

seed = 123
mean, var = 56.19-1, 61508.03
log_mu, log_sigma = utils.lognorm_params(mean, var)
rand_p, clus_p = 0.002, 0.008/(mean+1)

random.seed(seed)

if 'london_dataset' in os.listdir('./data/'):
    os.system('rm -rf ./data/london_dataset')
os.mkdir('./data/london_dataset')

for i in tqdm(complete_hh):
    df = pd.read_csv('./data/london_data/' + i)
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

    df.to_csv('./data/london_dataset/full_' + i.split('MAC')[1], index=False)
    for idx in idx_to_nan:
        df.iloc[idx, 1] = np.nan
    df.to_csv('./data/london_dataset/miss_' + i.split('MAC')[1], index=False)
    