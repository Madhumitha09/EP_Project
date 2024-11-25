import matplotlib
matplotlib.use('Agg')  # Ensure the backend is set to Agg first
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Path to save chart images
CHARTS_DIR = "static/charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

# Load the dataset
file_path = 'quality-of-life-indices.csv'
df = pd.read_csv(file_path)

# List of unique countries
countries = df["Country"].str.strip().unique()

# Function to generate a more enhanced chart for selected columns
def generate_chart(country1, country2, column):
    # Filter data for the selected countries
    data_country1 = df[df["Country"].str.strip() == country1]
    data_country2 = df[df["Country"].str.strip() == country2]

    # Make sure the data is sorted by year
    data_country1 = data_country1.sort_values(by="Year")
    data_country2 = data_country2.sort_values(by="Year")

    # Create the plot
    plt.figure(figsize=(12, 7))
    
    # Plot data for country 1
    plt.plot(
        data_country1["Year"], 
        data_country1[column], 
        marker='o', 
        linestyle='-', 
        color='royalblue', 
        label=country1,
        markersize=8
    )
    
    # Plot data for country 2
    plt.plot(
        data_country2["Year"], 
        data_country2[column], 
        marker='s', 
        linestyle='--', 
        color='darkorange', 
        label=country2,
        markersize=8
    )

    # Add annotations for max values for both countries
    max_val1 = data_country1[column].max()
    max_year1 = data_country1[data_country1[column] == max_val1]["Year"].iloc[0]
    plt.annotate(
        f'Max: {max_val1}',
        xy=(max_year1, max_val1),
        xytext=(max_year1, max_val1 + 2),
        arrowprops=dict(facecolor='black', arrowstyle='->'),
        fontsize=10,
        color='royalblue'
    )

    max_val2 = data_country2[column].max()
    max_year2 = data_country2[data_country2[column] == max_val2]["Year"].iloc[0]
    plt.annotate(
        f'Max: {max_val2}',
        xy=(max_year2, max_val2),
        xytext=(max_year2, max_val2 + 2),
        arrowprops=dict(facecolor='black', arrowstyle='->'),
        fontsize=10,
        color='darkorange'
    )

    # Chart title and labels with styling
    plt.title(f"{column} Comparison\n{country1} vs {country2}", fontsize=16, fontweight='bold', color='darkslategray')
    plt.xlabel("Year", fontsize=14, fontweight='bold', color='teal')
    plt.ylabel(column, fontsize=14, fontweight='bold', color='teal')

    # Add gridlines
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Adjust legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2, fontsize=12)

    # Set y-axis limits for better visuals
    plt.ylim(bottom=0)

    # Adjust the x-axis labels to prevent overlap
    plt.xticks(rotation=45, ha='right')

    # Save the chart to the static directory
    chart_filename = f"{country1}_{country2}_{column}_comparison.png"
    chart_path = os.path.join(CHARTS_DIR, chart_filename)
    plt.savefig(chart_path, bbox_inches='tight', dpi=300)
    plt.close()

    # Return the relative path that Flask can serve
    return f"charts/{chart_filename}"

@app.route('/')
def index():
    # Pass both the list of countries and the dataset column names to the template
    columns_to_compare = df.columns[3:]  # Extract column names to compare
    return render_template('index.html', countries=countries, columns=columns_to_compare)

@app.route('/get_chart', methods=['POST'])
def get_chart():
    data = request.json
    country1 = data['country1']
    country2 = data['country2']
    column = data['column']

    # Generate the chart
    chart_path = generate_chart(country1, country2, column)
    return jsonify({'chart_path': chart_path})

if __name__ == '__main__':
    app.run(debug=True)