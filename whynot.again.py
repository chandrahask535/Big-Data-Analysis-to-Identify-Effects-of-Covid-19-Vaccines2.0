import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
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

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    ok_button = ttk.Button(chart_window, text="OK", command=close_chart_window)
    ok_button.pack(pady=10)


def close_chart_window():
    chart_window.destroy()


# Tkinter GUI
def show_vaccine_info(vaccine_type):
    info_frame.pack_forget()
    vaccine_info_frame.pack(fill='both', expand=True)

    info = summary[summary['vaccine'] == vaccine_type].groupby('location')['total_vaccinations'].sum().reset_index()
    info = info.sort_values(by='total_vaccinations', ascending=False)
    info_str = "\n".join([f"{row['location']}: {row['total_vaccinations']}" for index, row in info.iterrows()])

    vaccine_info_label.config(text=f"Information about {vaccine_type}:\n\n{info_str}")

    ok_button = ttk.Button(vaccine_info_frame, text="OK", command=show_main_menu)
    ok_button.pack(pady=10)


def show_main_menu():
    vaccine_info_frame.pack_forget()
    info_frame.pack(fill='both', expand=True)


# Create the main window
root = tk.Tk()
root.title("Vaccine Analysis")
root.geometry("800x600")

# Load background image
background_image_path = r"C:\Users\ASUS\PycharmProjects\vaccine_pro\pythonProject1\data\vaccine-bottles.jpg"
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas and set the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill='both', expand=True)
canvas.create_image(0, 0, image=background_photo, anchor='nw')

# Main Frame
main_frame = ttk.Frame(canvas, padding="10 10 10 10", style='TFrame')
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
pie_chart_btn = tk.Button(info_frame, text="Show Vaccine Distribution Pie Chart", bg='blue', fg='white',
                          command=lambda: create_chart_window(root))
pie_chart_btn.pack(pady=10)

# Add buttons for each vaccine type
vaccine_types = summary['vaccine'].unique()
for vaccine in vaccine_types:
    btn = tk.Button(info_frame, text=vaccine, bg='green', fg='white', command=lambda v=vaccine: show_vaccine_info(v))
    btn.pack(pady=5, padx=10, fill='x')

# Vaccine Info Label
vaccine_info_label = ttk.Label(vaccine_info_frame, text="", style='TLabel', anchor='center')
vaccine_info_label.pack(pady=20, padx=20)

# Back Button
back_btn = ttk.Button(vaccine_info_frame, text="Back to Main Menu", command=show_main_menu)
back_btn.pack(pady=10)


# Function to create a new window for the pie chart
def create_chart_window(parent):
    global chart_window
    chart_window = tk.Toplevel(parent)
    chart_window.geometry("800x600")
    chart_window.title("Vaccine Distribution Pie Chart")
    create_pie_chart()


root.mainloop()
