# Import the relevant packages
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Get the data
df = pd.read_csv(
    "../Data/resale_and_rental_applications.csv"
)

# Get the unique years in the dataset
unique_years_ndarray = df["financial_year"].unique()

# Join the years into a string with a comma and a space
unique_years_str = ", ".join(
    map(
        str,
        unique_years_ndarray.tolist()
    )
)
print(f"Years in dataset: {unique_years_str}")

# Dynamically get the minimum year in the dataset
data_minimum_year = df["financial_year"].min()

# Dynamically get the maximum year in the dataset
data_maximum_year = df["financial_year"].max()

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
df_filter_pt_1 = df.copy()
df_filter_pt_1 = df_filter_pt_1[df_filter_pt_1["financial_year"] >= input_minimum_year]

# Filter the data based off the maximum year
df_filter_pt_2 = df_filter_pt_1.copy()
df_filter_pt_2 = df_filter_pt_2[df_filter_pt_2["financial_year"] <= input_maximum_year]

# Add a new column calculating the total applications registered for each financial year
df_total = df_filter_pt_2.copy()
df_total["year_total"] = df_total.groupby("financial_year")["applications_registered"].transform("sum")

# Add a new column calculating the percentage of applications registered for each financial year
df_percentage = df_total.copy()
df_percentage["percentage"] = (df_percentage["applications_registered"] / df_percentage["year_total"]) * 100

df_final = df_percentage.copy()

# Pivot the data to get the percentage of applications registered for each financial year and type
df_final = df_final.pivot(
    index = "financial_year",
    columns = "type",
    values = "percentage"
)

# Plot the data
fig, ax = plt.subplots(
    figsize = (11, 7)
)

# Make it a stacked bar chart
df_final.plot(
    kind = "bar",
    stacked = True,
    ax = ax
)

# Make an array of y-ticks from 0 to 100 with a step of 10
y_tick_array = np.arange(0, 110, 10)

# Set the y-ticks to the array that was just created
ax.set_yticks(y_tick_array)

# Set the title of the chart
ax.set_title(
    f"Rental & resale applicants from {input_minimum_year} to {input_maximum_year}",
    fontweight = "bold"
)

# Set the label of the x-axis
ax.set_xlabel(
    "Year",
    fontweight = "bold"
)

# Set the label of the y-axis
ax.set_ylabel(
    "Percentage",
    fontweight = "bold"
)

# Create a legend
ax.legend(
    df_final.columns,
    bbox_to_anchor = (1, 1)
)

# Check if the Charts folder exists; If not, create it
if not os.path.exists("../Charts"):
    os.makedirs("../Charts")

# Save the figure as a PNG file in the Charts folder
plt.savefig("../Charts/applications_registered.png")

# Show the figure
plt.show()