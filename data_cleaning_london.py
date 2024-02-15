import pandas as pd 
from tqdm import tqdm
import utils
import os

id_list = []

os.mkdir('data/london_data')

print('Extracting Household Data...')

for i in tqdm(range(168)):
    file = pd.read_csv('data/Small LCL Data/LCL-June2015v2_' + str(i) + '.csv')
    ids_file = file['LCLid'].unique()
    for id in ids_file:
        if id not in id_list:
            id_list.append(id)
            file_id = file[file['LCLid'] == id]
            file_id.to_csv('data/london_data/' + id + '.csv', index=False)
        else:
            file_id = file[file['LCLid'] == id]
            load = pd.read_csv('data/london_data/' + id + '.csv')
            load = pd.concat([load, file_id])
            load.to_csv('data/london_data/' + id + '.csv', index=False)

os.chdir('data/london_data')
print('Cleaning Data...')

for file in tqdm(os.listdir('./')):
    df = pd.read_csv(file)
    utils.clean_df(df)
    df.to_csv(file, index=False)