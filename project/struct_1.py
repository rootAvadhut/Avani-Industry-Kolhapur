import os

def create_project_structure(project_root="project_root"):
    """Creates the directory structure for the Python GUI project."""

    folders = {
        "screens": [
            "home_screen.py", 
            "delete_screen.py",
            "import_screen.py", 
            "backup_screen.py"
        ],
        "utils": [
            "create_treeview.py",
            "db_connection.py",
            "db.py",
            "update_box.py",
            "imports.py"
        ]
    }

    # Create the main project directory if it doesn't exist
    os.makedirs(project_root, exist_ok=True)

    # Create the main script file
    with open(os.path.join(project_root, "main.py"), "w") as f:
        f.write("# Your main application code will go here")

    # Create subfolders and their files
    for folder_name, files in folders.items():
        folder_path = os.path.join(project_root, folder_name)
        os.makedirs(folder_path, exist_ok=True)  
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as f:
                f.write(f"# Code for {file_name} will go here")

if __name__ == "__main__":
    create_project_structure()
