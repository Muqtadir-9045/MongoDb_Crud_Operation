import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# ----------------- MongoDB Connection -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["car_database"]
collection = db["spare_parts"]

# ----------------- Colors & Styles -----------------
BG_COLOR = "#1e1e2f"
FG_COLOR = "#ffffff"
BTN_COLOR = "#3498db"
BTN_HOVER = "#2980b9"
ENTRY_BG = "#2e2e3f"
FONT = ("Segoe UI", 10)

# ----------------- Functions -----------------
def create_part():
    part = get_form_data()
    if not all(part.values()):
        messagebox.showerror("Error", "All fields are required.")
        return
    if collection.find_one({"part_id": part["part_id"]}):
        messagebox.showerror("Error", "Part with this ID already exists.")
        return
    try:
        part["price"] = float(part["price"])
        part["stock"] = int(part["stock"])
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Stock must be an integer.")
        return

    collection.insert_one(part)
    messagebox.showinfo("Success", "Spare part added successfully!")
    clear_entries()
    read_parts()

def read_parts():
    listbox.delete(0, tk.END)
    for part in collection.find():
        listbox.insert(tk.END, f"{part['part_id']} | {part['name']} | {part['car_model']} | Rs.{part['price']} | Stock: {part['stock']}")

def update_part():
    part_id = entry_id.get()
    if not part_id:
        messagebox.showerror("Error", "Part ID is required for update.")
        return

    updated = get_form_data()
    try:
        updated["price"] = float(updated["price"])
        updated["stock"] = int(updated["stock"])
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Stock must be an integer.")
        return

    result = collection.update_one({"part_id": part_id}, {"$set": updated})
    if result.modified_count > 0:
        messagebox.showinfo("Success", "Spare part updated successfully!")
    else:
        messagebox.showwarning("Warning", "No changes made or Part not found.")
    clear_entries()
    read_parts()

def delete_part():
    part_id = entry_id.get()
    if not part_id:
        messagebox.showerror("Error", "Part ID is required for deletion.")
        return
    result = collection.delete_one({"part_id": part_id})
    if result.deleted_count > 0:
        messagebox.showinfo("Success", "Spare part deleted successfully!")
    else:
        messagebox.showwarning("Warning", "Part not found.")
    clear_entries()
    read_parts()

def clear_entries():
    for entry in (entry_id, entry_name, entry_model, entry_price, entry_stock):
        entry.delete(0, tk.END)

def get_form_data():
    return {
        "part_id": entry_id.get().strip(),
        "name": entry_name.get().strip(),
        "car_model": entry_model.get().strip(),
        "price": entry_price.get().strip(),
        "stock": entry_stock.get().strip()
    }

def on_listbox_select(event):
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        data = listbox.get(index).split(" | ")
        clear_entries()
        entry_id.insert(0, data[0])
        entry_name.insert(0, data[1])
        entry_model.insert(0, data[2])
        entry_price.insert(0, data[3].replace("Rs.", ""))
        entry_stock.insert(0, data[4].replace("Stock: ", ""))

# ----------------- UI Setup -----------------
root = tk.Tk()
root.title("Car Spare Part Management")
root.geometry("650x550")
root.config(bg=BG_COLOR)

# Top label
top_label = tk.Label(root, text="Car Spare Part Management", bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 14, "bold"))
top_label.pack(anchor="center", pady=10)

# Form Frame
form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(anchor="w", padx=20)

def create_label_entry(text):
    label = tk.Label(form_frame, text=text, bg=BG_COLOR, fg=FG_COLOR, font=FONT)
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground="white", font=FONT, width=30)
    entry.pack(anchor="w", pady=4, ipady=3, ipadx=5)
    return entry

entry_id = create_label_entry("Part ID")
entry_name = create_label_entry("Part Name")
entry_model = create_label_entry("Compatible Car Model")
entry_price = create_label_entry("Price")
entry_stock = create_label_entry("Stock Quantity")

# Button Frame
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(anchor="w", padx=20, pady=10)

def create_button(text, command, color=BTN_COLOR):
    btn = tk.Button(btn_frame, text=text, command=command, bg=color, fg="white",
                    activebackground=BTN_HOVER, font=FONT, width=12)
    btn.pack(side=tk.LEFT, padx=5)
    return btn

create_button("Add", create_part)
create_button("View", read_parts)
create_button("Update", update_part)
create_button("Delete", delete_part)
create_button("Clear", clear_entries, "#e74c3c")

# Listbox
listbox = tk.Listbox(root, width=80, height=15, bg=ENTRY_BG, fg=FG_COLOR,
                     font=FONT, selectbackground="#5555aa")
listbox.pack(padx=20, pady=10)
listbox.bind("<<ListboxSelect>>", on_listbox_select)

# Initial Load
read_parts()

root.mainloop()
