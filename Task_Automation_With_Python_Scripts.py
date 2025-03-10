import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# File categories
file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", " .docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".cpp", ".java", ".html", ".css", ".js", ".json"],
    "Executables": [".exe", ".bat", ".sh", ".msi"],
    "Others": []
}

# Function to organize files
def organize_files():
    folder_selected = folder_var.get()
    if not folder_selected or not os.path.exists(folder_selected):
        messagebox.showerror("Error", "Please select a valid folder!")
        return

    progress_bar["value"] = 0
    root.update_idletasks()

    for folder in file_categories.keys():
        folder_path = os.path.join(folder_selected, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    files = os.listdir(folder_selected)
    total_files = len(files)
    
    if total_files == 0:
        messagebox.showinfo("Info", "No files found to organize!")
        return

    count = 0
    for file in files:
        file_path = os.path.join(folder_selected, file)
        
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()
            
            moved = False
            for category, extensions in file_categories.items():
                if file_ext in extensions:
                    shutil.move(file_path, os.path.join(folder_selected, category, file))
                    moved = True
                    break

            if not moved:
                shutil.move(file_path, os.path.join(folder_selected, "Others", file))
        
        count += 1
        progress_bar["value"] = (count / total_files) * 100
        root.update_idletasks()

    auto_delete_empty_folders(folder_selected)
    messagebox.showinfo("Success", "🎉 Files organized successfully!")

# Function to delete empty folders
def auto_delete_empty_folders(folder_selected):
    for root_dir, dirs, _ in os.walk(folder_selected, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root_dir, dir_name)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

# Function to select folder
def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_var.set(folder_selected)

# Function to toggle dark mode
def toggle_theme():
    if dark_mode.get():
        root.configure(bg="#222")
        label.configure(bg="#222", fg="white")
        entry.configure(bg="#333", fg="white", insertbackground="white")
        btn_select.configure(bg="#444", fg="white")
        btn_organize.configure(bg="#555", fg="white")
        theme_switch.configure(bg="#222", fg="white")
    else:
        root.configure(bg="#f4f4f4")
        label.configure(bg="#f4f4f4", fg="black")
        entry.configure(bg="white", fg="black", insertbackground="black")
        btn_select.configure(bg="#008CBA", fg="white")
        btn_organize.configure(bg="#007B5E", fg="white")
        theme_switch.configure(bg="#f4f4f4", fg="black")

# GUI Setup
root = tk.Tk()
root.title("✨ Smart File Organizer")
root.state("zoomed")  # Open in full screen
root.configure(bg="#f4f4f4")

# Centering frame
main_frame = tk.Frame(root, bg="#f4f4f4")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Folder Selection Variable
folder_var = tk.StringVar()

# Heading Label
label = tk.Label(main_frame, text="📂 Smart File Organizer", font=("Arial", 16, "bold"), bg="#f4f4f4", fg="black")
label.pack(pady=10)

# Folder Selection Entry & Button
frame = tk.Frame(main_frame, bg="#f4f4f4")
frame.pack(pady=5)
entry = tk.Entry(frame, textvariable=folder_var, width=35, font=("Arial", 12))
entry.pack(side="left", padx=5)
btn_select = tk.Button(frame, text="📁 Browse", command=select_folder, font=("Arial", 12), bg="#008CBA", fg="white", padx=10)
btn_select.pack(side="left")

# Organize Button
btn_organize = tk.Button(main_frame, text="🚀 Organize Files", command=organize_files, font=("Arial", 12), bg="#007B5E", fg="white", padx=10, pady=5)
btn_organize.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Dark Mode Toggle
dark_mode = tk.BooleanVar()
theme_switch = tk.Checkbutton(main_frame, text="🌙 Dark Mode", variable=dark_mode, command=toggle_theme, font=("Arial", 10), bg="#f4f4f4", fg="black")
theme_switch.pack(pady=5)

root.mainloop()