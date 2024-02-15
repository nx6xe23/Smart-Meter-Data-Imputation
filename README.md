# Smart-Meter-Data-Imputation

This repository contains code to perform various different methods of data imputation to smart meter data. The data used in this is "Smart Meter Energy Consumption Data in London Households" from UK Power Networks. This data is available at: https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households. This data contains the enrgy consumption of 5567 London households from November 2011, till February 2014. The data is collected at half-hourly intervals. The study had 1100 customers who were subjected to dynamic Time of Use pricing while the rest had the standard tariff structure. We aim to study and analyze the standard tariff customers only. 

---

## Data Cleaning

Download the dataset from the given link in the data folder and unzip it in the data folder. Download the Small LCL Data with 168 files as the big csv file seems to be corrupted. Run the data cleaning file to clean the data and save it for each household individually. 

```
python data_cleaning_london.py
```

This will go through the csv files and cluster the data for each household and save it in the data folder. It will also go through the data and add `NaN` values to the data with missing readings. 

---
