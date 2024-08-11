import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Global variables for data
data = None
data2 = None
vaccine_data = None
df_vaccinations = None
df_summary = None
aggregated_data = None
top_10_data = None

# Function to load datasets
def load_datasets():
    global data, data2, vaccine_data, df_vaccinations, df_summary
    data_path = filedialog.askopenfilename(title="Select Transformed Data CSV")
    raw_data_path = filedialog.askopenfilename(title="Select Raw Data CSV")
    vaccine_data_path = filedialog.askopenfilename(title="Select Vaccine Data CSV")

    if data_path and raw_data_path and vaccine_data_path:
        data = pd.read_csv(data_path)
        data2 = pd.read_csv(raw_data_path)
        vaccine_data = pd.read_csv(vaccine_data_path)

        # Load additional data for vaccination analysis
        file_path1 = filedialog.askopenfilename(title="Select the vaccination data file")
        file_path2 = filedialog.askopenfilename(title="Select the vaccine summary file")
        if file_path1 and file_path2:
            df_vaccinations = pd.read_csv(file_path1)
            df_summary = pd.read_csv(file_path2)

        process_data()
    else:
        print("Datasets not loaded. Please select all required files.")

# Function to process data after loading
def process_data():
    global aggregated_data, top_10_data
    code = data["CODE"].unique().tolist()
    country = data["COUNTRY"].unique().tolist()
    hdi = []
    tc = []
    td = []
    sti = []
    population = data["POP"].unique().tolist()

    for i in country:
        hdi.append((data.loc[data["COUNTRY"] == i, "HDI"]).sum() / 294)
        tc.append((data2.loc[data2["location"] == i, "total_cases"]).sum())
        td.append((data2.loc[data2["location"] == i, "total_deaths"]).sum())
        sti.append((data.loc[data["COUNTRY"] == i, "STI"]).sum() / 294)
        population.append((data2.loc[data2["location"] == i, "population"]).sum() / 294)

    aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)),
                                   columns=["Country Code", "Country", "HDI",
                                            "Total Cases", "Total Deaths",
                                            "Stringency Index", "Population"])

    aggregated_data = aggregated_data.sort_values(by=["Total Cases"], ascending=False)
    top_10_data = aggregated_data.head(10)

# Function to clean the vaccination data
def clean_data(df):
    df['daily_vaccinations_raw'] = df['daily_vaccinations_raw'].fillna(df['daily_vaccinations'])
    df['total_vaccinations'] = df['total_vaccinations'].fillna(0)
    df['people_vaccinated'] = df['people_vaccinated'].fillna(0)
    df['people_fully_vaccinated'] = df['people_fully_vaccinated'].fillna(0)
    df['daily_vaccinations_raw'] = df['daily_vaccinations_raw'].fillna(0)
    df['daily_vaccinations'] = df['daily_vaccinations'].fillna(0)
    return df

# Function to expand the vaccines column into individual rows
def expand_vaccines(df):
    df = df.assign(vaccines=df['vaccines'].str.split(', ')).explode('vaccines')
    return df

# Function to map the death rate based on the summary file
def map_death_rate(vaccine, summary_df):
    death_rate_mapping = {
        "Pfizer/BioNTech": 0.00002,  # Example value
        "Moderna": 0.00003,  # Example value
        "Oxford/AstraZeneca": 0.00004,  # Example value
        "Johnson&Johnson": 0.00005,  # Example value
        # Add more mappings as necessary
    }

    return death_rate_mapping.get(vaccine, 0)

# Function to predict death rates
def predict_death_rates(df, summary_df):
    df['death_rate'] = df['vaccines'].apply(lambda x: map_death_rate(x, summary_df))
    return df

# Function to create a bubble map
def create_bubble_map(df):
    df_grouped = df.groupby(['country', 'iso_code']).agg({
        'total_vaccinations': 'sum',
        'people_vaccinated': 'sum',
        'death_rate': 'mean'
    }).reset_index()

    fig = px.scatter_geo(
        df_grouped,
        locations="iso_code",
        color="death_rate",
        hover_name="country",
        size="people_vaccinated",
        projection="natural earth",
        color_continuous_scale="Reds",
        size_max=100,
        title="Global Vaccinations and Death Rates"
    )

    fig.update_layout(
        title="Global Vaccinations and Death Rates",
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
    )

    fig.show()

# Functions to create charts
def create_chart_window(parent, chart_func):
    chart_window = tk.Toplevel(parent)
    chart_window.geometry("800x600")
    chart_window.title("Chart Window")
    chart_func()

def create_bar_chart_total_cases():
    fig = px.bar(top_10_data, y='Total Cases', x='Country', title="Countries with Highest Covid Cases")
    fig.show()

def create_bar_chart_total_deaths():
    fig = px.bar(top_10_data, y='Total Deaths', x='Country', title="Countries with Highest Deaths")
    fig.show()

def create_grouped_bar_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_10_data["Country"],
        y=top_10_data["Total Cases"],
        name='Total Cases',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=top_10_data["Country"],
        y=top_10_data["Total Deaths"],
        name='Total Deaths',
        marker_color='lightsalmon'
    ))
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()

def create_pie_chart():
    cases = top_10_data["Total Cases"].sum()
    deceased = top_10_data["Total Deaths"].sum()
    labels = ["Total Cases", "Total Deaths"]
    values = [cases, deceased]
    fig = px.pie(top_10_data, values=values, names=labels, title='Percentage of Total Cases and Deaths', hole=0.5)
    fig.show()

def create_bar_chart_stringency():
    fig = px.bar(top_10_data, x='Country', y='Total Cases',
                 hover_data=['Population', 'Total Deaths'],
                 color='Stringency Index', height=400,
                 title="Stringency Index during Covid-19")
    fig.show()

def create_vaccine_choropleth():
    vaccine_map = px.choropleth(vaccine_data, locations='iso_code', color='vaccines')
    vaccine_map.update_layout(height=300, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    vaccine_map.show()

# Main function to integrate all functionalities
def main():
    if df_vaccinations is not None and df_summary is not None:
        df_vaccinations_cleaned = clean_data(df_vaccinations)
        df_vaccinations_expanded = expand_vaccines(df_vaccinations_cleaned)
        df_vaccinations_predicted = predict_death_rates(df_vaccinations_expanded, df_summary)
        create_bubble_map(df_vaccinations_predicted)
    else:
        print("Please load the datasets for vaccination analysis.")

# Create the main window
root = tk.Tk()
root.title("COVID-19 VACCINE ANALYSIS")
root.geometry("800x600")

# Load background image
background_image_path = r"C:\Users\ASUS\PycharmProjects\vaccine_pro\pythonProject1\data\vaccine-bottles.jpg"
try:
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((800, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
except Exception as e:
    print(f"Error loading image: {e}")
    background_photo = None

# Create a label to hold the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add a large title
title_label = tk.Label(background_label, text="ANALYSIS OF COVID-19 VACCINES", font=("Times new roman", 24, "bold"), bg='red', fg='black')
title_label.pack(pady=20)

# Add button to load datasets
tk.Button(background_label, text="Load Datasets", font=("Helvetica", 14), command=load_datasets).pack(pady=10)

# Add buttons to the main frame with larger font
tk.Button(background_label, text="Predict and Show Death Rates", font=("Helvetica", 14), command=main).pack(pady=10)
tk.Button(background_label, text="Show Countries with Highest Covid Cases", font=("Helvetica", 14),
          command=lambda: create_chart_window(root, create_bar_chart_total_cases)).pack(pady=10)
tk.Button(background_label, text="Show Countries with Highest Deaths", font=("Helvetica", 14),
          command=lambda: create_chart_window(root, create_bar_chart_total_deaths)).pack(pady=10)
tk.Button(background_label, text="Show Grouped Bar Chart of Cases and Deaths", font=("Helvetica", 14),
          command=lambda: create_chart_window(root, create_grouped_bar_chart)).pack(pady=10)
tk.Button(background_label, text="Show Percentage of Total Cases and Deaths", font=("Helvetica", 14),
          command=lambda: create_chart_window(root, create_pie_chart)).pack(pady=10)
tk.Button(background_label, text="Show Stringency Index during Covid-19", font=("Helvetica", 14),
          command=lambda: create_chart_window(root, create_bar_chart_stringency)).pack(pady=10)
tk.Button(background_label, text="Show Vaccine Distribution Choropleth", font=("Helvetica", 14),
          command=lambda: create_chart_window(root, create_vaccine_choropleth)).pack(pady=10)

root.mainloop()
