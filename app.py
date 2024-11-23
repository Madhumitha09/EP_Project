from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
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

# Function to generate a single chart for selected columns
def generate_chart(country1, country2, column):
    # Filter data for the selected countries
    data_country1 = df[df["Country"].str.strip() == country1]
    data_country2 = df[df["Country"].str.strip() == country2]

    plt.figure(figsize=(20, 12))
    plt.plot(data_country1["Year"], data_country1[column], marker='o', label=country1, color='blue')
    plt.plot(data_country2["Year"], data_country2[column], marker='o', label=country2, color='red')
    plt.title(f"{column} in {country1} and {country2}", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel(column, fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)

    # Save the chart to the static directory
    chart_path = os.path.join(CHARTS_DIR, f"{country1}_{country2}_{column}_comparison.png")
    plt.savefig(chart_path)
    plt.close()
    return f"charts/{country1}_{country2}_{column}_comparison.png"

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
