import tkinter as tk
import os
import shutil
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import for the progress bar

# Global variable to store selected folder path
selected_folder_path = ""

def select_path():
    global selected_folder_path
    selected_folder_path = filedialog.askdirectory()
    path_label.config(text=selected_folder_path)  # Update the label with the selected path
    return selected_folder_path

def create_subfolder_if_needed(folder_path, subfolder_name):
    subfolder_path = os.path.join(folder_path, subfolder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    return subfolder_path

def clean_folder():
    global selected_folder_path
    folder_path = selected_folder_path
    if not folder_path:
        print("No folder selected!")
        path_label.config(text="No folder selected! Please select a folder.")
        return

    # Ask for confirmation before cleaning
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to clean the folder?")
    if not confirm:
        path_label.config(text="Cleaning cancelled by user.")
        print("Cleaning cancelled by user.")
        return

    # Get the list of files to process
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)

    if total_files == 0:
        path_label.config(text="No files found to clean.")
        return

    # Reset and configure the progress bar
    progress_bar['value'] = 0
    progress_bar['maximum'] = total_files

    # Clean the selected folder and update the progress bar
    for index, file_name in enumerate(files):
        file_extension = file_name.split(".")[-1].lower()
        if file_extension:
            subfolder_name = f"{file_extension.upper()} Files"
            subfolder_path = create_subfolder_if_needed(folder_path, subfolder_name)
            file_path = os.path.join(folder_path, file_name)
            new_location = os.path.join(subfolder_path, file_name)
            if not os.path.exists(new_location):
                shutil.move(file_path, subfolder_path)
                print(f"Moved: {file_name} -> {subfolder_name}/")
                path_label.config(text=f"Moved: {file_name} -> {subfolder_name}/")
            else:
                print(f"Skipped: {file_name} already exists in {subfolder_name}/")
                path_label.config(text=f"Skipped: {file_name} already exists in {subfolder_name}/")

        # Update progress bar after each file
        progress_bar['value'] = index + 1
        root.update_idletasks()  # Update the UI

    path_label.config(text="Cleaning completed!")
    print("Cleaning completed!")
    show_completion_popup()


def show_completion_popup():
    # Pop-up showing "Done!" and options to select another folder or exit
    result = messagebox.askquestion("Done!", "Cleaning is complete!\nWould you like to clean another directory?")

    if result == "yes":
        select_path()  # Let the user select another directory
    else:
        root.quit()  # Close the application

########### GUI ##########

root = tk.Tk()
root.geometry("400x400")
root.title("DirCleaner")

info_label = tk.Label(text="Choose the directory you would like to clean", font=("Arial", 18))
info_label.pack(padx=10, pady=10)

path_label = tk.Label(text="No directory selected", font=("Arial", 18), wraplength=350)
path_label.pack(padx=10, pady=10)

# Button to select directory
select_button = tk.Button(root, text="Select Directory", command=select_path, width=20)
select_button.pack(padx=10, pady=10)

# Button to start cleaning the folder
clean_button = tk.Button(root, text="Start cleaning", command=clean_folder, width=20)
clean_button.pack(padx=10, pady=10)

# Progress bar for cleaning
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(padx=10, pady=10)

root.mainloop()
