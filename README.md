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


The average missing data is 0.38% for the non-complete households, of which 21.79% and 78.21% are random and cluster missing data. The average length of a cluster is 56.19 and the variance is 61508.03. The average half hourly reading for the complete household energy data is 0.2331. 

---

## Creating Missing Dataset from Complete Dataset

Run the following python script to remove datapoints from the complete household dataset. 

```
python creating_dataset.py
```

This uses the mean and variance of the already incomplete dataset to remove datapoints from complete household data. 1% of the data is removed per dataset of which 20% will correspond to the random missing data points and the rest 80% will denote the cluster missing values. Furthermore to find the length of the cluster, we use the log normal distribution $X = e^{\mu + \sigma Z}$ where $Z$ is the standard normal variable. To calculate $\mu$ and $\sigma$ we use the statistically derived mean and variance for $X$. This python script will remove these clusters and random missing data points making sure there are no conflicts.

---

## Linear, Historical and Weighted Average Imputation

For the missing values, between index $i$ and $j$ with values $x_i$ and $x_j$ respectively, the imputed values are denoted by $\hat{x}_k = \cfrac{(x_j - x_i) \cdot (k - i)}{j - i} + x_i$  for $i < k < j$. 

```
python linear_imputation.py
```

For the historical average imputation, we look at the average readings across different years during the same days and time. For this we have chosen $\pm2$ years, $\pm8$ days and $\pm 1.5$ hours. The average of these values is taken as the imputed value.

```
python hist_avg_imputation.py
```

Weighted average imputation uses the previous two methods two impute the missing data with a weight parameter $w_i = e^{-\alpha d_i}$ where $\alpha$ is a hyperparameter and $d_i$ is the distance to the closest non-missing data point. The imputed value for this method is $\hat{y}_i = w_i \cdot \hat{y}^{LI}_i + (1 - w_i) \cdot \hat{y}^{HA}_i$. The best performing value of $\alpha$ was $\alpha = 1.05$ based on the $R^2$ score. 

```
python weighted_avg_imputation.py
````
The results for the following imputation techniques are as follows, 

| Error | LI | HA | WA | 
| :----- | -- | -- | -- |
| MAE | 0.1318 | 0.1183 | 0.1066 | 
| RMSE | 0.2127 | 0.1862 | 0.1723 | 
| $R^2$ score | -0.0777 | 0.1749 | 0.2798 | 

---

## Bilinear, KNN and Random Forest Imputation

Bilinear imputation uses the linear imputation as well as it interpolates weekly, i.e., the imputation value will be the average of the linearly interpolated and weekly interpolated values. To find the weekly interpolated values, we find closest week data for which the day and time are same and interpolate using it. 

$$\hat{x}^{LI}_k = \cfrac{(x_j - x_i) \cdot (k - i)}{(j - i)} + x_i \text{ for } i < k < j$$
$$\hat{w}^{LI}_k = \cfrac{(w_j - w_i) \cdot (k - i)}{(j - i)} + w_i \text{ for } i < k < j$$

And finally the imputed value will be $\hat{x}_i = (\hat{x}_i^{LI} + \hat{w}^{LI}_i)/ 2$. 

```
python bilinear_imputation.py
```

KNN imputer uses the KNN algorithm to impute the missing values, it takes the nearest neighbours of the missing value and takes their average as the imputation value.

```
python knn_imputation.py
```

For the random forest imputation method, each household energy data which is not missing is trained to a random forest and the missing dates are predicted then from the random forest. 

```
python rf_imputation.py
```
| Error | BI | KNN | RF | 
| :----- | -- | -- | -- |
| MAE | 0.1144 | 0.1573 | 0.1484 | 
| RMSE | 0.1839 | 0.2231 | 0.2184 | 
| $R^2$ score | 0.2192 | -0.0931 | -0.0317 | 

---