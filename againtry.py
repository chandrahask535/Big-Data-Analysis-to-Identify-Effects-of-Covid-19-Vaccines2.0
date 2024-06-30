import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the datasets
vaccination_data_path = r"C:\Users\ASUS\PycharmProjects\vaccine_pro\pythonProject1\data\country_vaccinations.csv"
manufacturer_data_path = r"C:\Users\ASUS\PycharmProjects\vaccine_pro\pythonProject1\data\country_vaccinations_by_manufacturer.xlsx"

vaccination_data = pd.read_csv(vaccination_data_path)
manufacturer_data = pd.read_excel(manufacturer_data_path)

# Summarize the manufacturer data by country and vaccine type
summary = manufacturer_data.groupby(['location', 'vaccine']).agg({'total_vaccinations': 'sum'}).reset_index()

# Summarize the number of countries using each vaccine type
vaccine_country_count = summary.groupby('vaccine')['location'].nunique().reset_index()
vaccine_country_count.columns = ['vaccine', 'country_count']


# Create a pie chart
def create_pie_chart():
    plt.figure(figsize=(8, 8))
    plt.pie(vaccine_country_count['country_count'], labels=vaccine_country_count['vaccine'], autopct='%1.1f%%',
            startangle=140)
    plt.title('Distribution of Vaccines by Country Count')
    plt.show()


# Tkinter GUI
def show_vaccine_info(vaccine_type):
    info = summary[summary['vaccine'] == vaccine_type].groupby('location')['total_vaccinations'].sum().reset_index()
    info = info.sort_values(by='total_vaccinations', ascending=False)
    info_str = "\n".join([f"{row['location']}: {row['total_vaccinations']}" for index, row in info.iterrows()])
    messagebox.showinfo("Vaccine Info", f"Information about {vaccine_type}:\n\n{info_str}")


def create_pie_chart_in_gui():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(vaccine_country_count['country_count'], labels=vaccine_country_count['vaccine'], autopct='%1.1f%%',
           startangle=140)
    ax.set_title('Distribution of Vaccines by Country Count')

    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


root = tk.Tk()
root.title("Vaccine Analysis")
root.geometry("800x600")

style = ttk.Style()
style.theme_use('clam')  # Use a modern theme

# Define a style for the buttons
style.configure('TButton', font=('Helvetica', 10), padding=10)
style.configure('TFrame', background='#f0f0f0')

# Create a main frame
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(fill='both', expand=True)

# Create a frame for the pie chart button
button_frame = ttk.Frame(main_frame, padding="10 10 10 10")
button_frame.pack(side='top', fill='x', expand=False)

# Add a button to show the pie chart in the GUI
pie_chart_btn = ttk.Button(button_frame, text="Show Vaccine Distribution Pie Chart", command=create_pie_chart_in_gui)
pie_chart_btn.pack(pady=10)

# Create a frame for the pie chart
pie_chart_frame = ttk.Frame(main_frame, padding="10 10 10 10", borderwidth=2, relief='groove')
pie_chart_frame.pack(side='top', fill='both', expand=True)

# Add buttons for each vaccine type
vaccine_types = summary['vaccine'].unique()
for vaccine in vaccine_types:
    btn = ttk.Button(main_frame, text=vaccine, command=lambda v=vaccine: show_vaccine_info(v))
    btn.pack(pady=5, padx=10, fill='x', expand=False)

root.mainloop()
