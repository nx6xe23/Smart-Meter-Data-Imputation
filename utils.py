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
    df['DateTime'] = df['DateTime'].apply(split_date)

    df.drop_duplicates(keep='first', inplace=True)
    df.drop(['LCLid', 'stdorToU'], axis=1, inplace=True)
    df.columns = ['DateTime', 'KWh']

    start_time, end_time = df['DateTime'].min(), df['DateTime'].max()
    times = timeseries(start_time, end_time)

    for time in times:
        if time not in df['DateTime'].values:
            df = pd.concat([df, pd.DataFrame({'DateTime': [time], 'KWh': [np.nan]})], ignore_index=True)
    
    df.sort_values(by='DateTime', inplace=True)
    return
