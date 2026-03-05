# Import the relevant packages
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read from the data file
df = pd.read_csv(
    "../Data/resale_price_index.csv"
)

# Make a new column called "year" based off the quarter column
df_year = df.copy()
df_year["year"] = df_year["quarter"].str[:4].astype(int) # Extract the first 4 characters, which gives the year

# Group the years together
df_grouped = df_year.copy()
df_grouped = df_grouped.groupby(["year"])["index"].mean().reset_index()

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

# Filter the data based off the minimum year
df_filter_pt_1 = df_grouped.copy()
df_filter_pt_1 = df_filter_pt_1[df_filter_pt_1["year"] >= input_minimum_year]

# Filter the data based off the maximum year
df_filter_pt_2 = df_filter_pt_1.copy()
df_filter_pt_2 = df_filter_pt_2[df_filter_pt_2["year"] <= input_maximum_year]

fig, ax = plt.subplots(
    figsize = (11, 7)
)

# Add a line chart using Seaborn with the x-axis as the year and the y-axis as the index
sns.lineplot(
    data = df_filter_pt_2,
    x = "year",
    y = "index",
    ax = ax
)

# Make a NumPy array for the x-axis ticks based off the minimum and maximum year inputted by the user
x_axis_ticks = np.arange(
    input_minimum_year,
    (input_maximum_year + 1),
    1
)

# Set the x-axis ticks to the NumPy array of years and rotate the ticks by 90 degrees
ax.set_xticks(x_axis_ticks)
ax.tick_params(
    axis = "x",
    rotation = 90
)

# Set the title of the chart
ax.set_title(
    f"Average resale price index from {input_minimum_year} to {input_maximum_year}",
    fontweight = "bold"
)

# Set the label of the x-axis
ax.set_xlabel(
    "Year",
    fontweight = "bold"
)

# Set the label of the y-axis
ax.set_ylabel(
    "Average resale price index",
    fontweight = "bold"
)

# Add a horizontal dashed red line at y = 100 to indicate the base index
ax.axhline(
    100,
    color = "red",
    dashes = (3, 3, 3)
)

# Check if the Charts folder exists; If not, create it
if not os.path.exists("../Charts"):
    os.makedirs("../Charts")

# Save the figure as a PNG file in the Charts folder
fig.savefig("../Charts/resale_price_indexes_over_time.png")

# Show the figure
plt.show()