import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Function to update the progress bar and copy files and directories
def copy_files_and_directories():
    file_to_parse = filedialog.askopenfilename(title="Select file to parse", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if not file_to_parse:
        messagebox.showwarning("Input Required", "Please select a file to parse.")
        return

    source_dir = filedialog.askdirectory(title="Select source directory")
    if not source_dir:
        messagebox.showwarning("Input Required", "Please select the source directory.")
        return

    destination_dir = filedialog.askdirectory(title="Select destination directory")
    if not destination_dir:
        messagebox.showwarning("Input Required", "Please select the destination directory.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    try:
        with open(file_to_parse, 'r') as file_list:
            lines = file_list.readlines()

            # Configure the progress bar based on the number of files/directories to be copied
            progress_bar["maximum"] = len(lines)
            progress_bar["value"] = 0

            for i, line in enumerate(lines):
                filename = line.strip()  # Get the filename from the line, stripping any extra spaces or newlines
                source_file_path = os.path.join(source_dir, filename)

                # Check if it's a file and copy it
                if os.path.isfile(source_file_path):
                    shutil.copy2(source_file_path, os.path.join(destination_dir, filename))
                    print(f"Copied file: {filename} to {destination_dir}")

                # Check if a directory with the same name as the file (minus extension) exists
                file_basename, _ = os.path.splitext(filename)  # Extract the filename without extension
                source_dir_path = os.path.join(source_dir, file_basename)

                if os.path.isdir(source_dir_path):  # Check if the directory exists
                    destination_dir_path = os.path.join(destination_dir, file_basename)
                    shutil.copytree(source_dir_path, destination_dir_path, dirs_exist_ok=True)
                    print(f"Copied directory: {file_basename} to {destination_dir}")

                # Update the progress bar
                progress_bar["value"] = i + 1
                root.update_idletasks()

        # Show a prompt to let the user know the process is complete
        messagebox.showinfo("Process Complete", "Files and directories copied successfully.")

        # Reset the progress bar after user acknowledges the completion
        progress_bar["value"] = 0

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Copy Files and Directories")
root.geometry("400x250")

# Create and pack a label and a button
label = tk.Label(root, text="Click the button to copy files and directories")
label.pack(pady=20)

button = tk.Button(root, text="Start Copy Process", command=copy_files_and_directories)
button.pack(pady=10)

# Create and pack a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
