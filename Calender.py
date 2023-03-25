import calendar
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog


def create_calendar():
    global cal, current_date, month_label, table

    # First, destroy all the widgets in the table frame
    for widget in table.winfo_children():
        widget.destroy()

    cal = calendar.Calendar()
    current_date = cal.monthdatescalendar(year, month)

    month_label.config(
        text=f"{calendar.month_name[month]} {year}",
        font=("Exo", 18)
    )

    for week in current_date:
        row = tk.Frame(table)
        row.pack(side=tk.TOP)
        for day in week:
            if day.month != month:
                day_label = tk.Label(row, text="", width=5, height=2)
            else:
                day_label = tk.Button(
                    row,
                    text=str(day.day),
                    width=5,
                    height=2,
                    command=lambda day=day: select_date(day)
                )
                day_label.bind("<Button-3>", lambda event, day=day: set_reminder(event, day))
            day_label.pack(side=tk.LEFT)


def select_date(day):
    global year, month
    month_label.config(text=f"{calendar.month_name[day.month]} {day.year}")
    for widget in table.winfo_children():
        widget.destroy()
    year = day.year
    month = day.month
    create_calendar()

def set_month_year():
    global year, month
    selected_month = int(month_var.get())
    selected_year = int(year_var.get())
    if selected_year < 1900 or selected_year > 2099:
        messagebox.showerror("Error", "Invalid year! Enter year between 1900 and 2099.")
    else:
        year = selected_year
        month = selected_month
        create_calendar()

def set_reminder(event, day):
    reminder = tk.simpledialog.askstring("Reminder", "Enter a reminder for this day:")
    if reminder:
        messagebox.showinfo("Reminder Set", f"Reminder for {day.strftime('%B %d, %Y')}: {reminder}")

year = calendar.datetime.date.today().year
month = calendar.datetime.date.today().month


root = tk.Tk()
root.title("Calendar")
root.geometry("400x400")
root.resizable(False, False)

root.iconbitmap(False, 'icon.ico')

style = ttk.Style(root)
root.tk.call("source", "Tkinter-Excel-Interface/forest-light.tcl")
root.tk.call("source", "Tkinter-Excel-Interface/forest-dark.tcl")
style.theme_use("forest-dark")

cal = calendar.Calendar()
current_date = cal.monthdatescalendar(year, month)

month_year_frame = tk.Frame(root)
month_year_frame.pack(pady=10)

month_var = tk.StringVar()
month_dropdown = tk.OptionMenu(month_year_frame, month_var, *range(1, 13))
month_dropdown.config(width=5)
month_dropdown.pack(side=tk.LEFT)
month_var.set(month)

year_var = tk.StringVar()
year_entry = tk.Entry(month_year_frame, textvariable=year_var, width=6)
year_entry.pack(side=tk.LEFT)
year_var.set(year)

set_button = tk.Button(month_year_frame, text="Go", command=set_month_year)
set_button.pack(side=tk.LEFT, padx=10)

table = tk.Frame(root)
table.pack(pady=10)

month_label = tk.Label(root)
month_label.pack(pady=10)

create_calendar()

root.mainloop()
