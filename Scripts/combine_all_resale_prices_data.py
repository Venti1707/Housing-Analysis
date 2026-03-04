# Import the relevant packages
import pandas as pd

# Get the data files
resale_1 = pd.read_csv(
    "../Data/resale_prices_from_2012-03_to_2014-12.csv"
)

resale_2 = pd.read_csv(
    "../Data/resale_prices_from_2015-01_to_2016-12.csv"
)

resale_3 = pd.read_csv(
    "../Data/resale_prices_from_2017-01_to_present.csv"
)

# Concat them into a singular dataframe
resale_all = pd.concat(
    [resale_1, resale_2, resale_3],
    ignore_index = True,
)

# Fill the values that are NaN with "No data"
resale_all_na_filled = resale_all.fillna("No data")

# Export it into a new CSV file
resale_all_na_filled.to_csv(
    "../Data/resale_prices_2012-03_to_present.csv",
    index = False
)