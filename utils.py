from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def split_date(value):
    """
    This function removes the miniseconds from the date and time.
    """
    return value.split('.')[0]


def timeseries(start_time, end_time):
    """
    This function takes two strings as input and returns the difference in hours between the two times.
    """
    start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    delta = timedelta(minutes=30)
    times = [start.strftime('%Y-%m-%d %H:%M:%S')]
    curr = start
    while(curr < end):
        curr += delta
        times.append(curr.strftime('%Y-%m-%d %H:%M:%S'))
    return times


def clean_df(df):
    """
    This function takes a pandas dataframe as input and returns a cleaned dataframe.
    """
    if len(df.columns) == 2:
        return df

    df['DateTime'] = df['DateTime'].apply(split_date)

    df.drop_duplicates(keep='first', inplace=True)
    df.drop(['LCLid', 'stdorToU'], axis=1, inplace=True)
    df.columns = ['DateTime', 'KWh']

    start_time, end_time = df['DateTime'].min(), df['DateTime'].max()
    times = timeseries(start_time, end_time)

    row_list = []
    for time in times:
        if time not in df['DateTime'].values:
            row_list.append({'DateTime': time, 'KWh': np.nan})
    
    new_df = pd.DataFrame(row_list, columns=['DateTime', 'KWh'])
    df = pd.concat([df, new_df], ignore_index=True, sort=False)
    df.sort_values(by='DateTime', inplace=True)
    return df


def lognorm_params(mean, var):
    sigma = np.sqrt(np.log(var/(mean**2) + 1))
    mu = np.log(mean) - 0.5 * sigma**2
    return mu, sigma


def mae(pred, actual):
    pred_arr = np.array(pred)
    actual_arr = np.array(actual)
    return np.mean(np.abs(pred_arr - actual_arr))


def rmse(pred, actual):
    pred = np.asarray(pred)
    actual = np.asarray(actual)
    return np.sqrt(np.mean((pred - actual) ** 2))


def linear_interpolation(nan_idx, miss_arr):
    clusters, pred = [], []

    for idx in nan_idx:
        if idx-1 in nan_idx:
            clusters[-1][1] += 1
            continue
        clusters.append([idx, 1])

    for idx, length in clusters:
        prev, next = idx - 1, idx + length
        if prev < 0 and next < len(miss_arr):
            prev = next
        if next >= len(miss_arr):
            next = prev
        for itr in range(length):
            pred_li = (miss_arr[next] - miss_arr[prev]) * (itr + 1) / (length + 1) + miss_arr[prev]
            pred.append(pred_li)
    return pred


def hist_avg_imputaiton(nan_idx, miss_arr):
    pred = []

    for idx in nan_idx:    
        ha_idx = []
        for yr in range(-2, 3):
            for d in range(-8, 9):
                for h in range(-3, 4):
                    if idx  + yr * 17520 + d * 48 + h >= 0 and idx  + yr * 17520 + d * 48 + h < len(miss_arr):
                        if idx  + yr * 17520 + d * 48 + h not in nan_idx:
                            ha_idx.append(miss_arr[idx  + yr * 17520 + d * 48 + h])

        if len(ha_idx) == 0:
            pred.append(0)
        else:
            pred.append(sum(ha_idx)/len(ha_idx))
    return pred


def optimally_wavg_imputation(nan_idx, miss_arr, alpha):
    pred_li = linear_interpolation(nan_idx, miss_arr)
    pred_ha = hist_avg_imputaiton(nan_idx, miss_arr)
    
    d = []
    for idx in nan_idx:
        dis = 1
        while True:
            if idx - dis >= 0 and idx - dis not in nan_idx:
                d.append(dis)
                break
            if idx + dis < len(miss_arr) and idx + dis not in nan_idx:
                d.append(dis)
                break
            dis += 1
    
    pred = []

    for i in range(len(nan_idx)):
        w = np.exp(-alpha * d[i])
        pred.append(w * pred_li[i] + (1 - w) * pred_ha[i])
    return pred


def bilinear_imputation(nan_idx, miss_arr):
    preds = []
    for idx in nan_idx:
        prev, next = idx, idx
        while prev >= 0:
            if prev not in nan_idx:
                break
            else:
                prev -= 336
        
        while next < len(miss_arr):
            if next not in nan_idx:
                break
            else:
                next += 336

        if prev < 0 and next >= len(miss_arr):
            preds.append(0)
        elif prev < 0:
            preds.append(miss_arr[next])
        elif next >= len(miss_arr):
            preds.append(miss_arr[prev])
        else:
            preds.append(miss_arr[prev] + (miss_arr[next] - miss_arr[prev]) * (idx - prev) / (next - prev))
        
    pred_day = linear_interpolation(nan_idx, miss_arr)

    pred = [(preds[i] + pred_day[i])/2 for i in range(len(nan_idx))]
    return pred


def convert_datetime_to_num(str1):
    date = datetime.strptime(str1, '%Y-%m-%d %H:%M:%S')
    return int(date.strftime('%Y%m%d%H%M%S'))