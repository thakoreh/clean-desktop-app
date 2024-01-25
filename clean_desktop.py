import os
import shutil
import tkinter as tk
from tkinter import simpledialog, messagebox, StringVar, OptionMenu

def organize_desktop(categories):
    desktop_path = os.path.abspath(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
    misc_folder = "Misc"
    category_folders = set()

    # Create folders for default and new categories
    for category in categories:
        folder_path = os.path.join(desktop_path, category)
        category_folders.add(folder_path)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    # Create Misc folder
    misc_folder_path = os.path.join(desktop_path, misc_folder)
    category_folders.add(misc_folder_path)
    if not os.path.exists(misc_folder_path):
        os.mkdir(misc_folder_path)

    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)
        if item_path in category_folders or item.endswith('.exe'):
            continue

        if os.path.isfile(item_path):
            file_extension = os.path.splitext(item)[1].lower()
            moved = False
            for category, extensions in categories.items():
                if file_extension in extensions:
                    shutil.move(item_path, os.path.join(desktop_path, category))
                    moved = True
                    break
            if not moved:
                shutil.move(item_path, misc_folder_path)
        elif os.path.isdir(item_path) and item != misc_folder:
            shutil.move(item_path, misc_folder_path)

    messagebox.showinfo("Success", "Desktop organized successfully!")

def add_category():
    category_name = simpledialog.askstring("New Category", "Enter the name of the new category:")
    if category_name:
        file_extensions = simpledialog.askstring("File Extensions", "Enter the file extensions for this category (separated by commas):")
        if file_extensions:
            extensions_list = [ext.strip() for ext in file_extensions.split(',')]
            categories[category_name] = extensions_list
            update_category_options()

def delete_category():
    category_to_delete = category_var.get()
    if category_to_delete in categories:
        del categories[category_to_delete]
        update_category_options()
        messagebox.showinfo("Deleted", f"Category '{category_to_delete}' has been deleted.")
    else:
        messagebox.showerror("Error", "Please select a valid category to delete.")

def update_category_options():
    menu = category_option_menu["menu"]
    menu.delete(0, "end")
    for category in categories:
        menu.add_command(label=category, command=lambda value=category: category_var.set(value))
    category_var.set("")

root = tk.Tk()
root.title("Desktop Organizer")

categories = {
    'Exe': ['.exe'],
    'PDF': ['.pdf'],
    'Media': ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov'],
    'Shortcuts': ['.lnk']
}

organize_button = tk.Button(root, text="Organize Desktop", command=lambda: organize_desktop(categories))
organize_button.pack(pady=10)

add_category_button = tk.Button(root, text="Add New Category", command=add_category)
add_category_button.pack(pady=10)

category_var = StringVar(root)
category_option_menu = OptionMenu(root, category_var, *categories.keys())
category_option_menu.pack(pady=10)

delete_category_button = tk.Button(root, text="Delete Selected Category", command=delete_category)
delete_category_button.pack(pady=10)

root.mainloop()
