import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
students = db["students"]

# GUI Window
root = tk.Tk()
root.title("Student Management System - MongoDB CRUD")
root.geometry("650x450")

# Labels & Entries
tk.Label(root, text="Roll No").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Age").grid(row=2, column=0, padx=10, pady=5)

roll_entry = tk.Entry(root)
name_entry = tk.Entry(root)
age_entry = tk.Entry(root)

roll_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
age_entry.grid(row=2, column=1)

# Treeview (Table)
tree = ttk.Treeview(root, columns=("Roll", "Name", "Age"), show="headings")
tree.heading("Roll", text="Roll No")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.column("Roll", width=100)
tree.column("Name", width=200)
tree.column("Age", width=100)
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=20)


# Functions
def add_student():
    roll = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()

    if roll and name and age:
        students.insert_one({"roll": roll, "name": name, "age": age})
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
        load_data()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

def read_student():
    roll = roll_entry.get()
    student = students.find_one({"roll": roll})
    if student:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, student["name"])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, student["age"])
    else:
        messagebox.showerror("Not Found", "No student found with that Roll No.")

def update_student():
    roll = roll_entry.get()
    new_name = name_entry.get()
    new_age = age_entry.get()

    result = students.update_one(
        {"roll": roll}, {"$set": {"name": new_name, "age": new_age}}
    )
    if result.modified_count > 0:
        messagebox.showinfo("Success", "Student updated successfully!")
        clear_entries()
        load_data()
    else:
        messagebox.showerror("Error", "No student found with that Roll No.")

def delete_student():
    roll = roll_entry.get()
    result = students.delete_one({"roll": roll})
    if result.deleted_count > 0:
        messagebox.showinfo("Deleted", "Student deleted successfully!")
        clear_entries()
        load_data()
    else:
        messagebox.showerror("Error", "No student found with that Roll No.")

def load_data():
    # Clear table
    for row in tree.get_children():
        tree.delete(row)
    # Fetch data from MongoDB
    for student in students.find():
        tree.insert("", tk.END, values=(student["roll"], student["name"], student["age"]))

def clear_entries():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)


# Buttons
tk.Button(root, text="Add", command=add_student).grid(row=3, column=0, pady=10)
tk.Button(root, text="Read", command=read_student).grid(row=3, column=1, pady=10)
tk.Button(root, text="Update", command=update_student).grid(row=4, column=0, pady=10)
tk.Button(root, text="Delete", command=delete_student).grid(row=4, column=1, pady=10)
tk.Button(root, text="Refresh Table", command=load_data).grid(row=5, column=0, columnspan=2, pady=10)

# Load initial data
load_data()

root.mainloop()
