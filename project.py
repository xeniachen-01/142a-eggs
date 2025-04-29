# Imports:
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Import avian bird flu data

bird_flu = pd.read_csv('bird flu.csv')
bird_flu.head()
bird_flu['Outbreak Date'] = pd.to_datetime(bird_flu['Outbreak Date'])
bird_flu = bird_flu.groupby(bird_flu["Outbreak Date"].dt.to_period("M"))["Outbreaks"].sum().reset_index()
bird_flu["Outbreak Date"] = bird_flu["Outbreak Date"].astype(str) # Convert date to string format
bird_flu.rename(columns={"Outbreak Date": "Year-Month"}, inplace=True)
# bird_flu.head()

df = bird_flu.copy()

# Import and initialize y, add to the dataframe
prices = pd.read_excel("grade a egg prices.xlsx", sheet_name="Monthly")

# Convert the observation_date column to datetime format
prices['observation_date'] = pd.to_datetime(prices['observation_date'])

# Convert observation_date to Year-Month format
prices['observation_date'] = prices['observation_date'].dt.to_period('M').astype(str)

# Rename column
prices.rename(columns={"observation_date": "Year-Month", "APU0000708111":"Price"}, inplace=True)
prices.head()

# Merge df and prices on Year-Month
df = pd.merge(df, prices, on='Year-Month', how='left')
df

# Import Bacon prices
bacon_prices = pd.read_excel("bacon prices.xlsx", sheet_name="Monthly")

# Rename the second column to "bacon price"
bacon_prices = bacon_prices.rename(columns={bacon_prices.columns[1]: "bacon price"})
# bacon_prices.head()

# Convert the observation date to datetime format
bacon_prices["observation_date"] = pd.to_datetime(bacon_prices["observation_date"])

# Group by year and month, and calculate the mean bacon price
bacon_prices["year_month"] = bacon_prices["observation_date"].dt.to_period("M")
bacon_prices_grouped = bacon_prices.groupby("year_month")["bacon price"].mean().reset_index()
bacon_prices_grouped["year_month"] = bacon_prices_grouped["year_month"].astype(str) # Convert year_month to string format
bacon_prices_grouped.head()

# Merge df and bacon_prices_grouped on Year-Month
df = pd.merge(df, bacon_prices_grouped, left_on="Year-Month", right_on="year_month", how="left")
df = df.drop(columns=["year_month"])
df

# # Take out commercial backyard flocks because no datea after 2021
# # Commerical Backyard Flocks
# commercial_backyard_flocks = pd.read_csv("commercial-backyard-flocks.csv")
# commercial_backyard_flocks.head()

# # Convert the date column to datetime format
# commercial_backyard_flocks['date'] = pd.to_datetime(commercial_backyard_flocks['Outbreak Date'])

# # Group by year and month, and calculate the mean number of commercial backyard flocks
# commercial_backyard_flocks['year_month'] = commercial_backyard_flocks['date'].dt.to_period('M')
# commercial_backyard_flocks_grouped = commercial_backyard_flocks.groupby('year_month')['Flock Size'].sum().reset_index()
# commercial_backyard_flocks_grouped.head()

# # Concat df and commercial_backyard_flocks_grouped on Year-Month
# df = pd.merge(df, commercial_backyard_flocks_grouped, left_on="Year-Month", right_on="year_month", how="left")
# # Drop year_month column from df
# df = df.drop(columns=["year_month"])
# df.head()

# #Cage free - no data after 2021, drop from the model

# cage_free = pd.read_csv('cage-free-percentages.csv')
# cage_free.dropna()
# cage_free['observed_month'] = pd.to_datetime(cage_free['observed_month'])
# cage_free = cage_free.groupby(cage_free['observed_month'].dt.to_period('M'))['percent_eggs'].sum().reset_index()

# cage_free = cage_free[cage_free['percent_eggs'] != 0]
# cage_free

# # Concat X and cage_free on observed_month and Year-Month
# X = pd.concat([X, cage_free], axis=1)
# # Drop observed_month column from X
# X = X.drop(columns=["observed_month"])
# X.head()


# # Egg production (number of hens) - also no data after 2021, drop from the model

# # Import egg production data
# egg_production = pd.read_csv("egg-production.csv")
# egg_production.head()

# # Convert the date column to datetime format
# egg_production['observed_month'] = pd.to_datetime(egg_production['observed_month'])

# # Group by year and month, and calculate the mean number of eggs produced
# egg_production['year_month'] = egg_production['observed_month'].dt.to_period('M')
# egg_production.head()
# egg_production_grouped = egg_production.groupby('year_month')['n_hens'].sum().reset_index()
# egg_production_grouped

# ### Milk Prices - also no data after 1986, drop from the model

# # Import milk prices data
# milk_prices = pd.read_excel("milk prices.xlsx", sheet_name="Monthly")
# milk_prices.head()

# # Rename the second column to "milk price"
# milk_prices = milk_prices.rename(columns={milk_prices.columns[1]: "milk price"})
# milk_prices.head()

# # Convert the date column to datetime format
# milk_prices['observation_date'] = pd.to_datetime(milk_prices['observation_date'])

# # Group by year and month, and calculate the mean milk price
# milk_prices['year_month'] = milk_prices['observation_date'].dt.to_period('M')
# milk_prices_grouped = milk_prices.groupby('year_month')['milk price'].mean().reset_index()
# milk_prices_grouped

# Potato Prices
# Import potato prices data
potato_prices = pd.read_excel("potato prices.xlsx", sheet_name="Monthly")

# Rename the second column to "potato price"
potato_prices = potato_prices.rename(columns={potato_prices.columns[1]: "potato price"})

# Convert the date column to datetime format
potato_prices['observation_date'] = pd.to_datetime(potato_prices['observation_date'])

# Group by year and month, and calculate the mean potato price
potato_prices['year_month'] = potato_prices['observation_date'].dt.to_period('M')
potato_prices_grouped = potato_prices.groupby('year_month')['potato price'].mean().reset_index()
potato_prices_grouped['year_month'] = potato_prices_grouped['year_month'].astype(str) # Convert year_month to string format
# potato_prices_grouped.head()

# Merge df with potato_prices_grouped on Year-Month
df = pd.merge(df, potato_prices_grouped, left_on="Year-Month", right_on="year_month", how="left")
df = df.drop(columns=["year_month"])
df.head()

# ### Soybean prices
# Import the soybean prices csv but only rows 16 to 14237, where row 16 is header
soybean_prices = pd.read_csv('soybean-prices-historical-chart-data.csv', skiprows=15, nrows=14222)
soybean_prices.head()

# Rename the second column to "soybean price"
soybean_prices = soybean_prices.rename(columns={soybean_prices.columns[1]: "soybean price"})
soybean_prices.head()

# Rename the column to remove leading/trailing spaces
soybean_prices.rename(columns=lambda x: x.strip(), inplace=True)

# Convert the date column to datetime format
soybean_prices['date'] = pd.to_datetime(soybean_prices['date'])
soybean_prices['year-month'] = soybean_prices['date'].dt.to_period('M')
# Group by year and month, and calculate the mean soybean price
soybean_prices_grouped = soybean_prices.groupby('year-month')['soybean price'].mean().reset_index()
soybean_prices_grouped['year-month'] = soybean_prices_grouped['year-month'].astype(str) # Convert year-month to string format
# soybean_prices_grouped.head()

# Merge df and soybean_prices_grouped on Year-Month
df = pd.merge(df, soybean_prices_grouped, left_on="Year-Month", right_on="year-month", how="left")
# Drop Year-Month column from df
df = df.drop(columns=["year-month"])
df.head()


# Wheat Prices
# Import wheat prices excel file
wheat_prices = pd.read_excel("wheat prices.xlsx", sheet_name="Data")
wheat_prices.head()

# Rename the second column to "wheat price"
wheat_prices = wheat_prices.rename(columns={wheat_prices.columns[1]: "wheat price"})
wheat_prices.head()

# Date is currently in form Jan-2023, so convert to datetime format
wheat_prices['Date'] = pd.to_datetime(wheat_prices['Date'], format='%b-%Y')

# Convert Date to Year-Month format
wheat_prices['year-month'] = wheat_prices['Date'].dt.to_period('M')

# Drop Date column from wheat_prices
wheat_prices = wheat_prices.drop(columns=["Date"])

# Reset index of wheat_prices
wheat_prices.reset_index(drop=True, inplace=True)

# Change date to string format
wheat_prices['year-month'] = wheat_prices['year-month'].astype(str)

# Merge df and wheat prices on Year-Month
df = pd.merge(df, wheat_prices, left_on="Year-Month", right_on="year-month", how="left")
# Drop Year-Month column from df
df = df.drop(columns=["year-month"])
df


# Corn prices
# Import corn prices csv from row 16 onwards where row 16 is header
corn_prices = pd.read_csv('corn-prices-historical-chart-data.csv', skiprows=15)
corn_prices.head()

# Rename the second column to "corn price"
corn_prices = corn_prices.rename(columns={corn_prices.columns[1]: "corn price"})

# Convert the date column to datetime format
corn_prices['date'] = pd.to_datetime(corn_prices['date'])
corn_prices['year-month'] = corn_prices['date'].dt.to_period('M')

# Group by year and month, and calculate the mean corn price
corn_prices_grouped = corn_prices.groupby('year-month')['corn price'].mean().reset_index()
corn_prices_grouped['year-month'] = corn_prices_grouped['year-month'].astype(str) # Convert year-month to string format

# Merge df and corn_prices_grouped on Year-Month
df = pd.merge(df, corn_prices_grouped, left_on="Year-Month", right_on="year-month", how="left")
# Drop year-month column from df
df = df.drop(columns=["year-month"])
df.head()


# Egg Holidays
# Import the egg_hols.xlsx file
egg_hols = pd.read_excel("egg_hols.xlsx", sheet_name="Sheet1")

# Rename the second column to "egg_hols"
egg_hols = egg_hols.rename(columns={egg_hols.columns[1]: "egg_hols"})

# Convert the date column to datetime format
egg_hols['Year-Month'] = pd.to_datetime(egg_hols['Year-Month'])
egg_hols['Year-Month'] = egg_hols['Year-Month'].dt.to_period('M')
egg_hols['Year-Month'] = egg_hols['Year-Month'].astype(str) # Convert Year-Month to string format

# Merge df and egg_hols on Year-Month
df = pd.merge(df, egg_hols, left_on="Year-Month", right_on="Year-Month", how="left")
df.head()


# Gas Prices

# Import the U.S._All_Grades_All_Formulations_Retail_Gasoline_Prices.csv file
gas_prices = pd.read_csv("U.S._All_Grades_All_Formulations_Retail_Gasoline_Prices.csv")
gas_prices.head()

# Rename the second column to "gas price"
gas_prices = gas_prices.rename(columns={gas_prices.columns[1]: "gas price"})
gas_prices.head()

gas_prices['Year-Month'] = pd.to_datetime(gas_prices['Year-Month'])
gas_prices['Year-Month'] = gas_prices['Year-Month'].dt.to_period('M')
gas_prices['Year-Month'] = gas_prices['Year-Month'].astype(str) # Convert Year-Month to string format
gas_prices.head()

# Gas price and df column types
gas_prices.dtypes
df.dtypes

# Merge df and gas_prices on Year-Month
df = pd.merge(df, gas_prices, left_on="Year-Month", right_on="Year-Month", how="left")
df.head()

# # One Hot encode the dates

# # Encode Year-Month as an integer "months since start"
# i = 0
# # Calculate months_since_start based on the Year-Month column
# df['months_since_start'] = (df['Year-Month'] - df['Year-Month'].min()).apply(lambda x: x.n)

# # Drop Year-Month column from df
# df = df.drop(columns=["Year-Month"])
# df



# Preprocessing
# Drop rows with NaN values
df = df.dropna()

# Split the data into features and target variable
X = df.drop(columns=["Price"])
y = df["Price"]

# Export X, y, df to CSV files
X.to_csv("X.csv", index=False)
y.to_csv("y.csv", index=False)
df.to_csv("df.csv", index=False)

print(X.head())
print(y.head())
print(df.head())

df_no_dates = df.drop(columns=["Year-Month"])