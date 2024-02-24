# Smart-Meter-Data-Imputation

This repository contains code to perform various different methods of data imputation to smart meter data. The data used in this is "Smart Meter Energy Consumption Data in London Households" from UK Power Networks. This data is available at: https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households. This data contains the enrgy consumption of 5567 London households from November 2011, till February 2014. The data is collected at half-hourly intervals. The study had 1100 customers who were subjected to dynamic Time of Use pricing while the rest had the standard tariff structure. We aim to study and analyze the standard tariff customers only. 

---

## Data Cleaning

Download the dataset from the given link in the data folder and unzip it in the data folder. Download the Small LCL Data with 168 files as the big csv file seems to be corrupted. Run the data cleaning file to clean the data and save it for each household individually. 

```
python data_cleaning.py
```

This will go through the csv files and cluster the data for each household and save it in the data folder. It will also go through the data and add `NaN` values to the data with missing readings. 

---
## Data Analysis

Run the following python script to analyze the dataset. 

```
python data_analysis.py
```

For analyzing the dataset, first we find which of the households have no missing data points. This is saved in `complete_households.txt` file in the `data/london_data/` folder. The percentage of missing values in the non complete households is calculated. Furthermore, the ratio of random and clustered missing data values is calculated. The mean and the variance of the cluster sizes is also calculated. The mean is calculated using $\bar{x} = \cfrac{\sum x_i}{n}$ and the variance is $\sigma^2 = \cfrac{\sum(x_i - \bar{x})^2}{n-1}$. 


The average missing data is 0.38% for the non-complete households, of which 21.79% and 78.21% are random and cluster missing data. The average length of a cluster is 56.18 and the variance is 61490.90. 

---

## Creating Missing Dataset from Complete Dataset

Run the following python script to remove datapoints from the complete household dataset. 

```
python creating_dataset.py
```

This uses the mean and variance of the already incomplete dataset to remove datapoints from complete household data. 1% of the data is removed per dataset of which 20% will correspond to the random missing data points and the rest 80% will denote the cluster missing values. Furthermore to find the length of the cluster, we use the log normal distribution $X = e^{\mu + \sigma Z}$ where $Z$ is the standard normal variable. To calculate $\mu$ and $\sigma$ we use the statistically derived mean and variance for $X$. This python script will remove these clusters and random missing data points making sure there are no conflicts.

---
