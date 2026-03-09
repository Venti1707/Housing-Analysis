# Import the relevant packages
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data file which contains all resale data
df = pd.read_csv(
    "../Data/resale_prices_2012-03_to_present.csv",
    usecols = [
        "month",
        "town",
        "resale_price"
    ]
)

# Separate the various towns into their respective regions with a boilerplate code
# 1. It reads in a multi-lined string containing various towns
# 2. Then, it capitalizes all letters using .upper() within to match with the values inside the dataset
# 3. Afterwards, it converts the string into a list by splitting it with .split() and the line-break character, \n
# 4. To end off, the list is converted into a NumPy array
# Do note that the last line must not be an empty string or the NumPy array would contain an empty value for the last element
# This information is taken from https://www.hdb.gov.sg/about-us/history/hdb-towns-your-home

north_towns = """Sembawang
Woodlands
Yishun"""

north_towns_array = np.array(
    north_towns
    .upper()
    .split("\n")
)

north_east_towns = """Ang Mo Kio
Hougang
Punggol
Sengkang
Serangoon"""

north_east_towns_array = np.array(
    north_east_towns
    .upper()
    .split("\n")
)

east_towns = """Bedok
Pasir Ris
Tampines"""

east_towns_array = np.array(
    east_towns
    .upper()
    .split("\n")
)

west_towns = """Bukit Batok
Bukit Panjang
Choa Chu Kang
Clementi
Jurong East
Jurong West
Tengah"""

west_towns_array = np.array(
    west_towns
    .upper()
    .split("\n")
)

central_towns = """Bishan
Bukit Merah
Bukit Timah
Central Area
Geylang
Kallang/Whampoa
Marine Parade
Queenstown
Toa Payoh"""

central_towns_array = np.array(
    central_towns
    .upper()
    .split("\n")
)

# Make an empty NumPy array which is the size of the original DataFrame
np_array_empty = np.zeros(
    len(df),
    dtype = [
        ("month", "datetime64[M]"), # The months are in the "YYYY-MM" format
        ("region", "U20"), # The region is a string which can either be any of the above regions
        ("resale_price", "i8") # The resale price is an integer
    ]
)

# Make a NumPy array to store the months from the original DataFrame in the empty DataFrame
np_array_months = np_array_empty.copy()
np_array_months["month"] = df["month"].to_numpy()

# Make a NumPy array to store the resale prices from the previous NumPy array
np_array_resale_prices = np_array_months.copy()
np_array_resale_prices["resale_price"] = df["resale_price"].to_numpy()

# Make a NumPy array which stores the towns in the original DataSet
np_array_towns = df["town"]

# Make a NumPy array with the size of the original DataFrame and has a default value of North
regions_filler_north = np.full(
    len(df),
    "North",
    dtype = "U20"
)

# Make a NumPy array to find towns in the North East region and replace them in the previous NumPy array with the isin method
regions_filler_north_east = regions_filler_north.copy()
regions_filler_north_east[np.isin(np_array_towns, north_east_towns_array)] = "North East"

# Make a NumPy array to find towns in the East region and replace them in the previous NumPy array with the isin method
regions_filler_east = regions_filler_north_east.copy()
regions_filler_east[np.isin(np_array_towns, east_towns_array)] = "East"

# Make a NumPy array to find towns in the West region and replace them in the previous NumPy array with the isin method
regions_filler_west = regions_filler_east.copy()
regions_filler_west[np.isin(np_array_towns, west_towns_array)] = "West"

# Make a NumPy array to find towns in the Central region and replace them in the previous NumPy array with the isin method
regions_filler_central = regions_filler_west.copy()
regions_filler_central[np.isin(np_array_towns, central_towns_array)] = "Central"

# Make a NumPy Array with the final regions
np_array_regions = regions_filler_central.copy()

# Place the finalized regions into the NumPy array from line 104
np_array_final = np_array_resale_prices.copy()
np_array_final["region"] = np_array_regions

# Convert the final NumPy array into a Pandas DataFrame
df_region = pd.DataFrame(np_array_final)

# Make a new DataFrame containing the various years
df_year = df_region.copy()
df_year["year"] = df_year["month"].dt.year

# Group the data based off the region and year, summarized by the median of the resale prices
df_grouped = df_year.copy()

fig, ax = plt.subplots(
    figsize = (16, 9)
)

# Summary statistic input
while True:
    input_summary_statistic = input("Enter the way you want to summarize the data ('mean' or 'median'): ")

    # Mean
    if (input_summary_statistic.lower() == "mean"):
        df_grouped = df_grouped.groupby(["year", "region"])["resale_price"].mean().reset_index(name = "resale_price_summarized")
        break

    # Median
    elif (input_summary_statistic.lower() == "median"):
        df_grouped = df_grouped.groupby(["year", "region"])["resale_price"].median().reset_index(name = "resale_price_summarized")
        break

    # Any other input
    else:
        print("Invalid summary statistic entered. Please choose either 'mean' or 'median'.")

# Get the unique years in the dataset for a custom view
unique_years_ndarray = df_year["year"].unique()

# Join the years into a string with a comma and a space
unique_years_str = ", ".join(
    map(
        str,
        unique_years_ndarray.tolist()
    )
)

print(f"Years in dataset: {unique_years_str}")

# Dynamically get the minimum year in the dataset
data_minimum_year = unique_years_ndarray.min()

# Dynamically get the maximum year in the dataset
data_maximum_year = unique_years_ndarray.max()

# Year inputs
while True:
    try:
        input_minimum_year = int( # Get the minimum year the user wants to see
            input("Please enter the minimum year you would like to see: ")
        )
        input_maximum_year = int( # Get the maximum year the user wants to see
            input(
                "Please enter the maximum year you would like to see: "
            )
        )

        # If the minimum year inputted is not in the dataset, reject the input
        if not (data_minimum_year <= input_minimum_year <= data_maximum_year):
            print(f"Minimum year must be between {data_minimum_year} and {data_maximum_year}.")
            continue

        # If the maximum year inputted is not in the dataset, reject the input
        if not (data_minimum_year <= input_maximum_year <= data_maximum_year):
            print(f"Maximum year must be between {data_minimum_year} and {data_maximum_year}.")
            continue

        # If the maximum year inputted is lesser than or equal to the minimum year inputted, reject the input
        if input_maximum_year <= input_minimum_year:
            print("Maximum year must be greater than minimum year.")
            continue

        break

    # Check if the inputs are integers
    except ValueError:
        print("Please enter valid numeric years.")

# Get the unique region in the dataset for a custom view
unique_regions_ndarray = df_year["region"].unique()

print(f"Regions in dataset: {", ".join(unique_regions_ndarray)}")

# Region inputs
while True:
    input_region = input("Enter the regions you would like to see separated by commas, or type 'all': ")

    if input_region.lower() == "all":
        selected_regions = unique_regions_ndarray
        break

    selected_regions = [town.strip() for town in input_region.split(", ")]

    # Validate input
    if all(region in unique_regions_ndarray for region in selected_regions):
        break
    else:
        print("Invalid region entered. Please choose from the list above.")

# Filter the data based off the minimum year
df_filter_pt_1 = df_grouped.copy()
df_filter_pt_1 = df_filter_pt_1[df_filter_pt_1["year"] >= input_minimum_year]

# Filter the data based off the maximum year
df_filter_pt_2 = df_filter_pt_1.copy()
df_filter_pt_2 = df_filter_pt_2[df_filter_pt_2["year"] <= input_maximum_year]

# Filter the data based off the selected region
df_filter_pt_3 = df_filter_pt_2.copy()
df_filter_pt_3 = df_filter_pt_3[df_filter_pt_3["region"].isin(selected_regions)]

# Plotting logic (Uncomment when ready)
sns.lineplot(
    data = df_filter_pt_3,
    x = "year",
    y = "resale_price_summarized",
    hue = "region"
)

# Make a NumPy array of years based off the minimum and maximum year inputted by the user
x_axis_ticks = np.arange(
    input_minimum_year,
    (input_maximum_year + 1),
    1
)

# Set the x-axis ticks to the NumPy array of years
ax.set_xticks(x_axis_ticks)

# Set the title of the chart based off how many towns are selected
if (input_region.split(", ") == 1):
    ax.set_title(
        f"{input_summary_statistic.title()} resale price for flats in the {(', '.join(selected_regions)).title()} region from {input_minimum_year} to {input_maximum_year}",
        fontweight = "bold"
    )
else:
    ax.set_title(
        f"{input_summary_statistic.title()} resale price for flats in the {(', '.join(selected_regions)).title()} regions from {input_minimum_year} to {input_maximum_year}",
        fontweight = "bold"
    )

# Set the label of the x-axis
ax.set_xlabel(
    "Year",
    fontweight = "bold"
)

# Set the label of the y-axis
ax.set_ylabel(
    f"{input_summary_statistic.title()} resale price",
    fontweight = "bold"
)

unique_region_count = len(unique_regions_ndarray)

# Create a legend
ax.legend(
    loc = "lower center",
    bbox_to_anchor = (0.5, -0.15),
    ncols = unique_region_count
)

# Check if the Charts folder exists; If not, create it
if not os.path.exists("../Charts"):
    os.makedirs("../Charts")

# Save the figure as a PNG file in the Charts folder
plt.savefig("../Charts/resale_price_by_region.png")

plt.show()