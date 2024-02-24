import pandas as pd
from tqdm import tqdm 
import os

os.chdir('./data/london_data/')
write_file = open('complete_households.txt', 'w')

list_addr = sorted(os.listdir('./'))[:-1]
missing_files = []

missing, total = 0, 0

for i in tqdm(list_addr):
    file = pd.read_csv(i)
    file = file.drop(file[file['KWh'] == 'Null'].index)
    file = file['KWh']
    if file.isnull().values.any() == True:
        missing += file.isnull().values.sum()
        total += file.size
        missing_files.append(i)
        continue
    if len(file) == 0:
        continue
    write_file.write(i + '\n')

write_file.close()

print('Average Missing Data:', f'{(missing/total*100):.2f}%')

random, cluster = 0, 0
cluster_len = 0
cluster_sizes = []

for i in tqdm(missing_files):
    df = pd.read_csv(i)
    missing_idx = df[df['KWh'].isnull()].index.tolist()
    cluster_len = 1

    for j in range(len(missing_idx)-1):
        if missing_idx[j+1] - missing_idx[j] > 1:
            random += 1
            if cluster_len != 1:
                cluster_sizes.append(cluster_len)
            cluster_len = 1
        else:
            cluster += 1
            cluster_len += 1

    if cluster_len != 1:
        cluster += 1
        cluster_sizes.append(cluster_len)
    else:
        random += 1


print('Random Missing Data:', f'{(random/(random+cluster)*100):.2f}%')
print('Cluster Missing Data:', f'{(cluster/(random+cluster)*100):.2f}%')

mean = sum(cluster_sizes) / len(cluster_sizes) 
var = sum((i - mean) ** 2 for i in cluster_sizes) / (len(cluster_sizes) - 1)

print('Average Cluster Size:', f'{mean:.2f}')
print('Variance of Cluster Size:', f'{var:.2f}')
