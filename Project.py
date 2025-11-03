import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="Ujjwalrana003",        
        database="hospital_db"
    )

def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = combo_gender.get()
    disease = entry_disease.get()

    if name == "" or age == "" or gender == "" or disease == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)", 
                (name, age, gender, disease))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Patient added successfully!")
    clear_entries()

def view_patients():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_patient():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a patient to delete!")
        return
    values = tree.item(selected, 'values')
    patient_id = values[0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Patient record deleted!")
    view_patients()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_disease.delete(0, tk.END)
    combo_gender.set("")

# -------------------- Doctor Functions --------------------

def add_doctor():
    name = entry_doc_name.get()
    specialization = entry_doc_spec.get()

    if name == "" or specialization == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO doctors (name, specialization) VALUES (%s, %s)", 
                (name, specialization))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Doctor added successfully!")
    entry_doc_name.delete(0, tk.END)
    entry_doc_spec.delete(0, tk.END)

def view_doctors():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    rows = cur.fetchall()
    conn.close()

    text_doctors.delete(1.0, tk.END)
    for row in rows:
        text_doctors.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Specialization: {row[2]}\n")
    

def delete_doctor():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a doctor to delete!")
        return
    
    values = tree.item(selected_item, "values")
    doctor_id = values[0]  

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Doctor ID {doctor_id}?")
    if confirm:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))
        conn.commit()
        conn.close()

        tree.delete(selected_item)
        messagebox.showinfo("Deleted", f"Doctor ID {doctor_id} deleted successfully!")

# -------------------- Data Visualization --------------------

def show_age_distribution():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT age FROM patients")
    ages = [row[0] for row in cur.fetchall()]
    conn.close()

    if not ages:
        messagebox.showerror("Error", "No patient data available!")
        return

    ages = np.array(ages)
    plt.hist(ages, bins=range(0, 100, 10), edgecolor='black')
    plt.title("Patient Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number of Patients")
    plt.show()

# -------------------- Tkinter GUI --------------------

root = tk.Tk()
root.title("🏥 Hospital Management System")
root.geometry("950x600")
root.config(bg="#e3f2fd")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frame_patient = ttk.Frame(notebook)
notebook.add(frame_patient, text="Patient Management")

tk.Label(frame_patient, text="Name").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame_patient)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_patient, text="Age").grid(row=1, column=0, padx=10, pady=5)
entry_age = tk.Entry(frame_patient)
entry_age.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_patient, text="Gender").grid(row=2, column=0, padx=10, pady=5)
combo_gender = ttk.Combobox(frame_patient, values=["Male", "Female", "Other"])
combo_gender.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_patient, text="Disease").grid(row=3, column=0, padx=10, pady=5)
entry_disease = tk.Entry(frame_patient)
entry_disease.grid(row=3, column=1, padx=10, pady=5)

tk.Button(frame_patient, text="Add Patient", command=add_patient, bg="#81c784").grid(row=4, column=0, pady=10)
tk.Button(frame_patient, text="View Patients", command=view_patients, bg="#64b5f6").grid(row=4, column=1, pady=10)
tk.Button(frame_patient, text="Delete Patient", command=delete_patient, bg="#e57373").grid(row=4, column=2, pady=10)
tk.Button(frame_patient, text="Show Age Chart", command=show_age_distribution, bg="#ba68c8").grid(row=4, column=3, pady=10)

cols = ("ID", "Name", "Age", "Gender", "Disease")
tree = ttk.Treeview(frame_patient, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

frame_doctor = ttk.Frame(notebook)
notebook.add(frame_doctor, text="Doctor Management")

tk.Label(frame_doctor, text="Name").grid(row=0, column=0, padx=10, pady=5)
entry_doc_name = tk.Entry(frame_doctor)
entry_doc_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_doctor, text="Specialization").grid(row=1, column=0, padx=10, pady=5)
entry_doc_spec = tk.Entry(frame_doctor)
entry_doc_spec.grid(row=1, column=1, padx=10, pady=5)

tk.Button(frame_doctor, text="Add Doctor", command=add_doctor, bg="#81c784").grid(row=2, column=0, pady=10)
tk.Button(frame_doctor, text="View Doctors", command=view_doctors, bg="#64b5f6").grid(row=2, column=1, pady=10)

text_doctors = tk.Text(frame_doctor, width=60, height=15)
text_doctors.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
