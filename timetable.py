import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys
from tkcalendar import Calendar

# Database connection
conn = sqlite3.connect("rms.db")
cursor = conn.cursor()


def edit_timetable_window(parent=None):
    """UI for editing the timetable (HOD Role)."""
    def fetch_classes():
        """Fetch classes from the Classes table."""
        cursor.execute("SELECT class_name FROM Classes")
        return [row[0] for row in cursor.fetchall()]

    def fetch_subjects(class_name):
        """Fetch subjects for the selected class."""
        cursor.execute("""
        SELECT s.subject_name 
        FROM Subjects s 
        INNER JOIN Classes c ON s.class_id = c.class_id
        WHERE c.class_name = ?""", (class_name,))
        return [row[0] for row in cursor.fetchall()]

    def update_subjects(event):
        """Update ComboBoxes and subject-teacher labels when a class is selected."""
        selected_class = class_combobox.get()
        if not selected_class:
            messagebox.showerror("Error", "Please select a class!",parent=root)
            return

        # Update subjects for the selected class
        global subjects
        subjects = fetch_subjects(selected_class)

        if not subjects:
            messagebox.showerror("Error", f"No subjects found for the class: {selected_class}",parent=root)
            return

        # Update all timetable ComboBoxes
        for row in timetable_rows:
            for combo in row:
                combo["values"] = subjects
                combo.set("")  # Clear current value

        # Update subject-teacher section
        for i, subject_label in enumerate(subject_labels):
            if i < len(subjects):
                subject_label.config(text=subjects[i])
            else:
                subject_label.config(text="")

    def save_timetable():
        """Save the timetable data and teacher assignments into the Timetable table."""
        selected_class = class_combobox.get()
        if not selected_class:
            messagebox.showerror("Error", "Please select a class!", parent=root)
            return

        # Fetch the class_id for the selected class
        cursor.execute("SELECT class_id FROM Classes WHERE class_name = ?", (selected_class,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", f"Class '{selected_class}' not found!", parent=root)
            return
        class_id = result[0]

        # Validate timetable inputs
        timetable_data = []
        for row_index, row in enumerate(timetable_rows):
            if row_index >= len(times):  # Ensure valid time index
                continue
            time = times[row_index]
            for col_index, combo in enumerate(row):
                if col_index >= len(days):  # Ensure valid day index
                    continue
                day = days[col_index]
                subject = combo.get()
                if not subject:
                    messagebox.showerror("Error", "Please fill in all timetable fields!", parent=root)
                    return
                teacher_name = teacher_entries[subjects.index(subject)].get()
                if not teacher_name:
                    messagebox.showerror("Error", f"Please assign a teacher to the subject: {subject}", parent=root)
                    return
                timetable_data.append((class_id, day, time, subject, teacher_name))
        
        dialog = open_calendar_dialog()
        dialog.wait_window()

        if not selected_date.strip():
            messagebox.showerror("Error", f"Please Enter w.e.f Date", parent=root)
            return
        # Save data to the database
        try:
            cursor.execute("delete from timetable where class_id = ?",(class_id,))
            conn.commit()
            data_to_insert = [
            (class_id, day, time, subject, teacher_name, selected_date)
            for (class_id, day, time, subject, teacher_name) in timetable_data]
            cursor.executemany("""
            INSERT INTO Timetable (class_id, day, time, subject_name, teacher_name, wef_date  ) 
            VALUES (?, ?, ?, ?, ?,?)""",data_to_insert )
            conn.commit()
            messagebox.showinfo("Success", "Timetable saved successfully!", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save timetable: {e}", parent=root)

    def open_calendar_dialog():
    # Create a Toplevel window as a dialog
        dialog = tk.Toplevel(root)
        dialog.title(" ")
        dialog.transient(root)  # Make the dialog modal
        dialog.grab_set()  # Prevent interaction with the main window
        x=620
        y=270
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="Enter W.E.F Date of Timetable",font=("Arial",12,"bold"),foreground="Red").place(relx=0.5,y=15,anchor="center")
        # Create a calendar widget
        cal = Calendar(dialog, showweeknumbers = False,selectmode="day", year=2023, month=10, day=5)
        cal.pack(pady=(40,10), padx=20)

        # Function to handle date selection
        def on_date_select():
            nonlocal selected_date
            selected_date = cal.get_date()
            dialog.destroy()  # Close the dialog

        # Add a button to confirm the date selection
        select_button = tk.Button(dialog, text="Select Date",font=("Arial",12,"bold"),background="lightblue", command=on_date_select)
        select_button.pack(pady=5)
        return dialog

    # Main window
    root = tk.Toplevel(parent) if parent else tk.Tk()
    root.title("Timetable Management - Edit Timetable")
    #root.state("zoomed")  # Maximize window on launch
    root.configure(bg="#f5f5f5")

    # Title
    title_label = tk.Label(
        root,
        text="Edit Timetable",
        font=("Georgia", 20, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5
    )
    title_label.pack(fill=tk.X)
    selected_date = ""
    
    tk.Label(root, text="Select Class:", font=("Segoe UI", 15, "bold")).place(relx=0.48,y=80,anchor="e")
    class_combobox = ttk.Combobox(root, values=fetch_classes(), state="readonly", font=("Arial", 12), width=13)
    class_combobox.place(relx=0.5,y=80,anchor="w")
    class_combobox.bind("<<ComboboxSelected>>", update_subjects)

    # Timetable headers and rows
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    times = ["11:00", "12:00", "13:00", "14:00", "15:00"]

    table_frame = tk.Frame(root, bg="white", relief=tk.RAISED)
    table_frame.pack(pady=(80,260), padx=(200), fill=tk.BOTH, expand=True)

    # Headers
    tk.Label(
        table_frame, text="Timings", font=("Arial", 14, "bold"),
        bg="#4CAF50", fg="white", borderwidth=1, relief="solid", width=15, height=2
    ).grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
    for col, day in enumerate(days):
        tk.Label(
            table_frame, text=day, font=("Arial", 14, "bold"),
            bg="#4CAF50", fg="white", borderwidth=1, relief="solid", width=15, height=2
        ).grid(row=0, column=col + 1, padx=2, pady=2, sticky="nsew")

    # Timetable rows
    timetable_rows = []
    for row_index, time in enumerate(times):
        tk.Label(
            table_frame, text=time, font=("Arial", 15,"bold"),
            bg="#E0E0E0", borderwidth=1, relief="solid", width=15, height=2
        ).grid(row=row_index + 1, column=0, padx=2, pady=2, sticky="nsew")
        row = []
        for col_index in range(len(days)):
            combo = ttk.Combobox(table_frame, state="readonly", width=12, font=("Arial", 11),justify='center')
            combo.grid(row=row_index + 1, column=col_index + 1, padx=2, pady=2, sticky="nsew")
            row.append(combo)
        timetable_rows.append(row)

    # Teacher assignment section
    teacher_frame = tk.Frame(root, bg="white", relief=tk.RAISED)
    teacher_frame.place(relx=0.65,rely=0.71)
    tk.Label(teacher_frame, text="Subjects", font=("Segoe UI", 13, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(teacher_frame, text="Teachers", font=("Segoe UI", 13, "bold"), bg="white").grid(row=0, column=1, padx=5, pady=5)

    subject_labels = []
    teacher_entries = []
    for i in range(4):  # Maximum 5 subjects
        subject_label = tk.Label(teacher_frame, text="", font=("Arial", 12), bg="white", width=15, anchor="w")
        subject_label.grid(row=i + 1, column=0, padx=5, pady=5)
        subject_labels.append(subject_label)

        teacher_entry = ttk.Entry(teacher_frame, font=("Arial", 11), width=30)
        teacher_entry.grid(row=i + 1, column=1, padx=5, pady=5)
        teacher_entries.append(teacher_entry)

    # Save Button
    save_button = tk.Button(root, text="Save Timetable", command=save_timetable, font=("georgia", 14, "bold"), bg="#4CAF50", fg="white")
    save_button.place(relx=0.5,rely=0.8,anchor="center")

    # Configure table responsiveness
    table_frame.grid_columnconfigure(0, weight=1)  # Timings column
    for col in range(1, len(days) + 1):  # Days columns
        table_frame.grid_columnconfigure(col, weight=1)
    for row in range(1, len(times) + 1):  # Rows for time slots
        table_frame.grid_rowconfigure(row, weight=1)

    root.mainloop()



def view_timetable_window(class_name,parent=None):
    """UI for viewing the timetable (Teacher/Student Role)."""
    def fetch_timetable():
        """Fetch timetable for the given class."""
        cursor.execute("""
        SELECT day, time, subject_name, teacher_name
        FROM Timetable
        INNER JOIN Classes ON Timetable.class_id = Classes.class_id
        WHERE class_name = ?
        ORDER BY day, time""", (class_name,))
        return cursor.fetchall()

    # Main window
    root = tk.Toplevel(parent) if parent else tk.Tk()
    #root.title(f"Timetable for {class_name}") # Maximize the window on launch
    root.configure(bg="#f5f5f5")
    root.resizable(True, True)  # Allow resizing

    # Title
    title_label = tk.Label(
        root,
        text=f"Timetable for {class_name}",
        font=("Georgia", 20, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5, width=10, height=2
    )
    title_label.pack(fill=tk.X)

    # Fetch timetable data
    timetable = fetch_timetable()

    if not timetable:
        messagebox.showinfo("Info", f"No timetable found for the class: {class_name}")
        root.destroy()
        return

    # Table frame
    table_frame = tk.Frame(root, bg="white", relief=tk.RAISED, borderwidth=2)
    table_frame.pack(pady=(80,150), padx=150, fill=tk.BOTH, expand=True)

    # Days and Times
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    times = sorted(set(row[1] for row in timetable))  # Extract unique times from the timetable

    # Headers
    tk.Label(
        table_frame, text="Timings", font=("Arial", 13, "bold"),
        bg="#4CAF50", fg="white", borderwidth=1, relief="solid",height=2, width=15
    ).grid(row=0, column=0, padx=2, pady=1, ipady=2, sticky="nsew")
    for col, day in enumerate(days):
        tk.Label(
            table_frame, text=day, font=("Arial", 13, "bold"),
            bg="#4CAF50", fg="white", borderwidth=1, relief="solid", width=15
        ).grid(row=0, column=col + 1, padx=2, pady=1, ipady=2, sticky="nsew")
    
    # Timetable Rows
    for row_index, time in enumerate(times):
        tk.Label(
            table_frame, text=time, font=("Arial", 11, "bold"),
            bg="#E0E0E0", borderwidth=1, relief="solid", width=15
        ).grid(row=row_index + 1, column=0, padx=2, pady=1, ipady=2, sticky="nsew")
        for col_index, day in enumerate(days):
            cell_frame = tk.Frame(table_frame, bg="white", relief="solid", borderwidth=1, width=80, height=40)
            cell_frame.grid_propagate(False)
            cell_frame.grid(row=row_index + 1, column=col_index + 1, padx=1, pady=1, sticky="nsew")
    
            # Filter timetable data for the specific time and day
            cell_data = [row for row in timetable if row[0] == day and row[1] == time]
            if cell_data:
                subject = cell_data[0][2]
                teacher = cell_data[0][3]
                subject_label = tk.Label(cell_frame, text=subject, font=("Arial", 12), bg="white", anchor="center")
                teacher_label = tk.Label(cell_frame, text=f"({teacher})", font=("Arial", 10), bg="white", fg="#555555", anchor="center")
                subject_label.pack(pady=1,anchor="center")  # Adjust content padding
                teacher_label.pack(pady=1,anchor="center")  # Adjust content padding

    # Set column and row configurations for responsiveness
    table_frame.grid_columnconfigure(0, weight=1)  # Timings column
    for col in range(1, len(days) + 1):  # Days columns
        table_frame.grid_columnconfigure(col, weight=1)
    for row in range(1, len(times) + 1):  # Rows for time slots
        table_frame.grid_rowconfigure(row, weight=1)

    root.mainloop()