# Copy Files and Matching Directories GUI Tool

A Python-based GUI tool that allows users to copy specific files and matching directories from a source directory to a destination directory, based on a provided text file. The tool includes a progress bar that tracks the copy process and allows for multiple operations without restarting the app.

## Features
- GUI for easy user interaction using Tkinter.
- Progress bar to track the copy process.
- Supports copying specific files and directories listed in a text file.
- Resets the progress bar once the copy process is complete.
- Allows for multiple copy operations without restarting the app.

## How it Works
1. The user is prompted to select:
   - A text file containing the list of files and directories to be copied.
   - A source directory where the files and directories are located.
   - A destination directory where the files and directories will be copied.
   
2. The tool processes the text file line by line:
   - It checks if each line corresponds to a file or a directory (based on the full name or directory name) in the source directory.
   - If a file is found, it is copied to the destination directory.
   - If a directory (with the same name as the file, without the extension) is found, the entire directory is copied to the destination directory.
   
3. The progress bar is updated as each file or directory is processed.

4. Once the process is complete, a message is displayed to the user, and after acknowledging the prompt, the progress bar resets to allow for another copy process.

## Installation and Running Instructions

### Prerequisites
- Python 3.x must be installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- The `tkinter` and `shutil` libraries are part of the Python standard library, so no additional installation is required.

### Instructions for Windows

1. **Install Python**:
   - Download and install Python from the [official Python website](https://www.python.org/downloads/). Ensure that you select the option to "Add Python to PATH" during installation.

2. **Clone or Download the Repository**:
   - You can download this project from GitHub by clicking on the **Code** button and selecting **Download ZIP**.
   - Alternatively, if you are familiar with Git, you can clone the repository:
     ```bash
     git clone  {{ site.github.repository_name }}
     cd copy-files-gui
     ```

3. **Run the Script**:
   - Open a Command Prompt and navigate to the folder where the script (`copy_files_gui.py`) is located.
   - Run the script by typing:
     ```bash
     python copy_files_gui.py
     ```

4. **Follow the Prompts**:
   - A window will open where you can select the text file to parse, the source directory, and the destination directory.

### Instructions for macOS

1. **Install Python**:
   - macOS comes with Python 2 pre-installed, but you will need Python 3. You can install it using Homebrew:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     brew install python
     ```

2. **Clone or Download the Repository**:
   - You can download this project from GitHub by clicking on the **Code** button and selecting **Download ZIP**.
   - Alternatively, clone the repository if you are familiar with Git:
     ```bash
     git clone https://github.com/yourusername/copy-files-gui.git
     cd copy-files-gui
     ```

3. **Run the Script**:
   - Open the Terminal and navigate to the folder where the script (`copy_files_gui.py`) is located.
   - Run the script by typing:
     ```bash
     python3 copy_files_gui.py
     ```

4. **Follow the Prompts**:
   - A window will open where you can select the text file to parse, the source directory, and the destination directory.

### Text File Format
The text file used to specify which files and directories to copy should have the following format:

- Each line should contain the exact file or directory name.
- For files, include the extension (e.g., `example.txt`).
- For directories, omit the extension (e.g., `example_folder`).

Example of a valid text file:

example_file.txt example_folder another_file.zip another_folder

markdown


### Common Issues

- **Tkinter Not Found**: If `tkinter` is not found on macOS, you might need to install it:
  ```bash
  brew install python-tk

    Permissions Issues: On macOS, you may need to grant the Terminal full disk access in your Security & Privacy settings if you encounter permissions errors when selecting directories.
    
