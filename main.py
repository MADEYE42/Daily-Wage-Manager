import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3
import pandas as pd

class EmployeeManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily wage management system ")

        self.create_database()

        self.employee_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.sex_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.hourly_pay_var = tk.StringVar()
        self.hours_worked_var = tk.StringVar()
        self.joining_date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.bonus_var = tk.StringVar()
        self.create_widgets()

    def create_database(self):
        self.conn = sqlite3.connect('employees.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS employees 
                          (employee_id TEXT, name TEXT, age TEXT, sex TEXT, address TEXT, 
                           hourly_pay REAL, hours_worked REAL, joining_date TEXT,category TEXT,bonus REAL)''')
        self.conn.commit()

    def create_widgets(self):
        # Employee Details Entry
        tk.Label(self.master, text="Employee ID").grid(row=0, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.employee_id_var).grid(row=0, column=1)

        tk.Label(self.master, text="Name").grid(row=1, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.name_var).grid(row=1, column=1)

        tk.Label(self.master, text="Age").grid(row=2, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.age_var).grid(row=2, column=1)

        tk.Label(self.master, text="Sex").grid(row=3, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.sex_var).grid(row=3, column=1)

        tk.Label(self.master, text="Address").grid(row=4, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.address_var).grid(row=4, column=1)

        tk.Label(self.master, text="Hourly Pay").grid(row=5, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.hourly_pay_var).grid(row=5, column=1)

        tk.Label(self.master, text="Hours Worked").grid(row=6, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.hours_worked_var).grid(row=6, column=1)

        tk.Label(self.master, text="Category ").grid(row=7, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.category_var).grid(row=7, column=1)

        tk.Label(self.master, text="Joining Date:").grid(row=8, column=0, sticky="w")
        tk.Button(self.master, text="Choose Date", command=self.choose_date).grid(row=8, column=1)
        self.joining_date_entry = tk.Entry(self.master, textvariable=self.joining_date_var, state='readonly')
        self.joining_date_entry.grid(row=8, column=2)

        tk.Button(self.master, text="Add Employee", command=self.add_employee).grid(row=9, column=0, columnspan=3)

        # Report Display
        self.report_tree = ttk.Treeview(self.master,
                                        columns=("Employee ID", "Name", "Amount to be Paid", "Hours Worked","Category", "Bonus"),
                                        show="headings")
        self.report_tree.heading("Employee ID", text="Employee ID")
        self.report_tree.heading("Name", text="Name")
        self.report_tree.heading("Amount to be Paid", text="Amount to be Paid")
        self.report_tree.heading("Hours Worked", text="Hours Worked")
        self.report_tree.heading("Category", text="Category")
        self.report_tree.heading("Bonus", text="Bonus")
        self.report_tree.grid(row=10, column=0, columnspan=3)

        self.report_tree.bind("<Double-1>", self.update_employee_details)

        # Load existing employees from database
        self.load_employees_from_db()

    def choose_date(self):
        top = tk.Toplevel(self.master)
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack()

        def set_date():
            self.joining_date_var.set(cal.get_date())
            top.destroy()

        tk.Button(top, text="Set Date", command=set_date).pack()

    def add_employee(self):
        employee_id = self.employee_id_var.get()
        name = self.name_var.get()
        age = self.age_var.get()
        sex = self.sex_var.get()
        address = self.address_var.get()
        hourly_pay = float(self.hourly_pay_var.get())
        hours_worked = float(self.hours_worked_var.get())
        joining_date = self.joining_date_var.get()
        category = self.category_var.get()

        amount_to_be_paid = hourly_pay * hours_worked
        bonus = 0
        if hours_worked > 8:
            bonus = 0.15 * amount_to_be_paid

        # Add to database
        self.c.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (employee_id, name, age, sex, address, hourly_pay, hours_worked, joining_date,category,bonus))
        self.conn.commit()

        self.report_tree.insert("", "end", values=(employee_id, name, amount_to_be_paid, hours_worked,category, bonus))

    def update_employee_details(self, event):
        item = self.report_tree.selection()
        values = self.report_tree.item(item, "values")

        employee_id = values[0]
        name = values[1]
        amount_to_be_paid = values[2]
        hours_worked = values[3]
        bonus = values[5]
        category = values[4]

        top = tk.Toplevel(self.master)

        tk.Label(top, text="Employee ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(top, textvariable=tk.StringVar(value=employee_id), state='readonly').grid(row=0, column=1)

        tk.Label(top, text="Name:").grid(row=1, column=0, sticky="w")
        name_entry = tk.Entry(top, textvariable=tk.StringVar(value=name))
        name_entry.grid(row=1, column=1)

        tk.Label(top, text="Salary:").grid(row=2, column=0, sticky="w")
        amount_entry = tk.Entry(top, textvariable=tk.StringVar(value=amount_to_be_paid))
        amount_entry.grid(row=2, column=1)

        tk.Label(top, text="Hours Worked:").grid(row=3, column=0, sticky="w")
        hours_entry = tk.Entry(top, textvariable=tk.StringVar(value=hours_worked))
        hours_entry.grid(row=3, column=1)

        tk.Label(top, text="Category :").grid(row=4, column=0, sticky="w")
        category_entry = tk.Entry(top, textvariable=tk.StringVar(value=category))
        category_entry.grid(row=4, column=1)

        tk.Label(top, text="Bonus:").grid(row=5, column=0, sticky="w")
        bonus_entry = tk.Entry(top, textvariable=tk.StringVar(value=bonus))
        bonus_entry.grid(row=5, column=1)

        def update_details():
            new_name = name_entry.get()
            new_amount_to_be_paid = amount_entry.get()
            new_hours_worked = hours_entry.get()
            new_bonus = bonus_entry.get()
            new_category = category_entry.get()

            self.c.execute("UPDATE employees SET name=?, hourly_pay=?, hours_worked=?, bonus =?,category=? WHERE employee_id=?",
                           (new_name, new_amount_to_be_paid, new_hours_worked,new_bonus,new_category, employee_id))
            self.conn.commit()

            self.report_tree.item(item,
                                  values=(employee_id, new_name, new_amount_to_be_paid, new_hours_worked, new_bonus,new_category))
            top.destroy()

        tk.Button(top, text="Update Details", command=update_details).grid(row=6, columnspan=2)

    def load_employees_from_db(self):
        self.c.execute("SELECT employee_id , name ,hourly_pay * hours_worked as Salary,hours_worked,bonus ,category FROM employees")
        rows = self.c.fetchall()
        for row in rows:
            self.report_tree.insert("", "end", values=row)


def main():
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()