# Import the relevant packages
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read from the CSV file which contains all resale data
df = pd.read_csv(
    "../Data/resale_prices_2012-03_to_present.csv",
    usecols = [ # Only read the relevant columns
        "month",
        "flat_type",
        "resale_price"
    ]
)

# Make a new column for the years only
df_year = df.copy()
df_year["year"] = df_year["month"].str[:4].astype(int) # Extract the first 4 characters, which gives the year

# Group the data based off the year and flat type and get the mean/median resale price for each year and flat type
df_grouped = df_year.copy()

# Summary statistic input
while True:
    input_summary_statistic = input("Enter the way you want to summarize the data ('mean' or 'median'): ")

    # Mean
    if (input_summary_statistic.lower() == "mean"):
        df_grouped = df_grouped.groupby(["year", "flat_type"])["resale_price"].mean().reset_index(name = "resale_price_summarized")
        break

    # Median
    elif (input_summary_statistic.lower() == "median"):
        df_grouped = df_grouped.groupby(["year", "flat_type"])["resale_price"].median().reset_index(name = "resale_price_summarized")
        break

    # Any other input
    else:
        print("Invalid summary statistic entered. Please choose either 'mean' or 'median'.")

unique_years_ndarray = df_grouped["year"].unique() # Get the unique years in the dataset
unique_years_str = ", ".join(
    map(
        str,
        unique_years_ndarray.tolist()
    )
) # Join the years into a string with a comma and a space

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

unique_flat_types = df_grouped["flat_type"].unique()

print(f"Flat types in dataset: {", ".join(unique_flat_types)}")

# Flat type inputs
while True:
    input_flat_type = input("Enter the flat types you would like to see separated by commas, or type 'all': ")

    if input_flat_type.lower() == "all":
        selected_flat_types = unique_flat_types
        break

    selected_flat_types = [flat_type.strip() for flat_type in input_flat_type.split(", ")]

    # Validate input
    if all(flat_type in unique_flat_types for flat_type in selected_flat_types):
        break
    else:
        print("Invalid flat type entered. Please choose from the list above.")

# Filter the data based off the minimum year
df_filter_pt_1 = df_grouped.copy()
df_filter_pt_1 = df_filter_pt_1[df_filter_pt_1["year"] >= input_minimum_year]

# Filter the data based off the maximum year
df_filter_pt_2 = df_filter_pt_1.copy()
df_filter_pt_2 = df_filter_pt_2[df_filter_pt_2["year"] <= input_maximum_year]

# Filter the data based off the selected flat types
df_filter_pt_3 = df_filter_pt_2.copy()
df_filter_pt_3 = df_filter_pt_3[df_filter_pt_3["flat_type"].isin(selected_flat_types)]

fig, ax = plt.subplots(
    figsize = (17, 10)
)

# Add a line chart using Seaborn with the x-axis as the year and the y-axis as the average resale price
sns.lineplot(
    data = df_filter_pt_3,
    x = "year",
    y = "resale_price_summarized",
    hue = "flat_type"
)

# Make a NumPy array for the x-axis ticks based off the minimum and maximum year inputted by the user
x_axis_ticks = np.arange(
    input_minimum_year,
    (input_maximum_year + 1),
    1
)

# Set the x-axis ticks to the NumPy array of years
ax.set_xticks(x_axis_ticks)

# Set the title of the chart
ax.set_title(
    f"{input_summary_statistic.title()} resale price for {(', '.join(selected_flat_types)).title()} flats from {input_minimum_year} to {input_maximum_year}",
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

unique_flat_type_count = len(unique_flat_types)

# Create a legend
ax.legend(
    loc = "lower center",
    bbox_to_anchor = (0.5, -0.15),
    ncols = unique_flat_type_count
)

# Check if the Charts folder exists; If not, create it
if not os.path.exists("../Charts"):
    os.makedirs("../Charts")

# Save the figure as a PNG file in the Charts folder
plt.savefig("../Charts/resale_price_by_flat_type.png")

plt.show()