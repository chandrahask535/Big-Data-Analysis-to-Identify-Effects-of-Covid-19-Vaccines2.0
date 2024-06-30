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
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(vaccine_country_count['country_count'], labels=vaccine_country_count['vaccine'], autopct='%1.1f%%',
           startangle=140)
    ax.set_title('Distribution of Vaccines by Country Count')

    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Tkinter GUI
def show_vaccine_info(vaccine_type):
    info_frame.pack_forget()
    vaccine_info_frame.pack(fill='both', expand=True)

    info = summary[summary['vaccine'] == vaccine_type].groupby('location')['total_vaccinations'].sum().reset_index()
    info = info.sort_values(by='total_vaccinations', ascending=False)
    info_str = "\n".join([f"{row['location']}: {row['total_vaccinations']}" for index, row in info.iterrows()])

    vaccine_info_label.config(text=f"Information about {vaccine_type}:\n\n{info_str}")


def show_main_menu():
    vaccine_info_frame.pack_forget()
    info_frame.pack(fill='both', expand=True)


root = tk.Tk()
root.title("Vaccine Analysis")
root.geometry("800x600")

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 12), padding=10, background='#ffcccb')
style.configure('TFrame', background='#f0f8ff')
style.configure('TLabel', font=('Helvetica', 14), background='#f0f8ff')
style.configure('TNotebook.Tab', background='#ffcccb')

# Main Frame
main_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
main_frame.pack(fill='both', expand=True)

# Info Frame
info_frame = ttk.Frame(main_frame, padding="10 10 10 10", style='TFrame')
info_frame.pack(fill='both', expand=True)

# Vaccine Info Frame
vaccine_info_frame = ttk.Frame(main_frame, padding="10 10 10 10", style='TFrame')

# Pie Chart Frame
pie_chart_frame = ttk.Frame(info_frame, padding="10 10 10 10", style='TFrame')
pie_chart_frame.pack(side='top', fill='both', expand=True)

# Add a button to show the pie chart in the GUI
pie_chart_btn = ttk.Button(info_frame, text="Show Vaccine Distribution Pie Chart", command=create_pie_chart)
pie_chart_btn.pack(pady=10)

# Add buttons for each vaccine type
vaccine_types = summary['vaccine'].unique()
for vaccine in vaccine_types:
    btn = ttk.Button(info_frame, text=vaccine, command=lambda v=vaccine: show_vaccine_info(v))
    btn.pack(pady=5, padx=10, fill='x')

# Vaccine Info Label
vaccine_info_label = ttk.Label(vaccine_info_frame, text="", style='TLabel', anchor='center')
vaccine_info_label.pack(pady=20, padx=20)

# Back Button
back_btn = ttk.Button(vaccine_info_frame, text="Back to Main Menu", command=show_main_menu)
back_btn.pack(pady=10)

root.mainloop()
