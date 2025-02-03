import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os 
import re
from PIL import Image, ImageDraw, ImageFont
import math

def getFileNames(path):
    bmp_files = [file for file in os.listdir(path) if file.endswith('.bmp')]
    return bmp_files
    
def letter_to_index(letter):
    return ord(letter.lower()) - ord('a') + 1

def parseFileNames(names, antigen, plt):
    filedata = {}
    pattern = r"([a-zA-Z]+)-([0-9]+)([a-zA-Z])([0-9]+)"
    for name in names:
        match = re.search(pattern, name)
        if match: 
            Ag = match.group(1)
            plate = int(match.group(2))
            if (Ag == antigen) and (plate == plt):
                filename = name
                v_i = letter_to_index(match.group(3)) - 1
                h_i = int(match.group(4)) - 1
                filedata[filename] = (v_i,h_i)
    return filedata

def buildGraph(namesNPos,w,h,d):
    ltr_n = max(values[0] for values in namesNPos.values())
    num_n = max(values[1] for values in namesNPos.values())

    canvas = Image.new("RGB", (w, h), "white")

    w_marg = 30
    h_marg = 30
    
    font_size = 15 
    font = ImageFont.truetype("arial.ttf", font_size)


    hpp = math.floor((h-h_marg)/(ltr_n+1))
    wpp = math.floor((w-w_marg)/(num_n+1))
    for name,pos in namesNPos.items():
        img = Image.open(d+"\\"+name)
        resized_img = img.resize((wpp,hpp))
        canvas.paste(resized_img, (w_marg+pos[1]*wpp,h_marg+pos[0]*hpp))

        draw = ImageDraw.Draw(canvas)
        num_txt = str(pos[1]+1)

        

        x_position = w_marg+pos[1]*wpp+wpp/2 - font_size/2 # Specify the width (horizontal position)
        y_position = math.floor(h_marg/2 - font_size/2)  # Specify the height (vertical position)
        draw.text((x_position, y_position), num_txt, fill=(0, 0, 0), font=font)  # Black text
        ltr_txt = chr(65 + pos[0])
        x_position = math.floor(w_marg/2 - font_size/2) # Specify the width (horizontal position)
        y_position = h_marg+pos[0]*hpp+hpp/2 - font_size/2  # Specify the height (vertical position)
        draw.text((x_position, y_position), ltr_txt, fill=(0, 0, 0), font=font)  # Black text
    return canvas


def main(d,a,p,w,h,o):
    names = parseFileNames(getFileNames(d),a,p)
    buildGraph(names,w,h,d).save(o, format="PNG")


#
#
"""GUI Part"""
#
#

def browse_file(entry):
    """Open file dialog and set the selected file path in the entry widget."""
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def browse_directory(entry):
    """Open directory dialog and set the selected directory path in the entry widget."""
    dirpath = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dirpath)

def on_launch_button_click():
    """Wrapper to check fields and call run_script with arguments."""
    file_path = file_path_entry.get()
    dir_path = dir_path_entry.get()
    plate = int(plate_entry.get())
    antigen = antigen_entry.get()
    width = int(width_entry.get())
    height = int(height_entry.get())

    # Check if all fields are filled
    if not all([file_path, dir_path, plate, antigen, width, height]):
        messagebox.showerror("Error", "All fields must be filled!")
        return

    # Call the script with the collected arguments
    main(dir_path, antigen, plate, width, height, file_path)

# Create the main window
root = tk.Tk()
root.title("Script Launcher")
root.geometry("400x600")

# File Path
file_path_label = tk.Label(root, text="File Path:")
file_path_label.pack(pady=5)
file_path_entry = tk.Entry(root, width=40)
file_path_entry.pack(pady=5)
file_path_browse = tk.Button(root, text="Browse", command=lambda: browse_file(file_path_entry))
file_path_browse.pack(pady=5)

# Directory Path
dir_path_label = tk.Label(root, text="Directory Path:")
dir_path_label.pack(pady=5)
dir_path_entry = tk.Entry(root, width=40)
dir_path_entry.pack(pady=5)
dir_path_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(dir_path_entry))
dir_path_browse.pack(pady=5)

# Name 1
plate_label = tk.Label(root, text="Plate:")
plate_label.pack(pady=5)
plate_entry = tk.Entry(root, width=40)
plate_entry.pack(pady=5)

# Name 2
antigen_label = tk.Label(root, text="Antigen:")
antigen_label.pack(pady=5)
antigen_entry = tk.Entry(root, width=40)
antigen_entry.pack(pady=5)

# Number 1
width_label = tk.Label(root, text="width:")
width_label.pack(pady=5)
width_entry = tk.Entry(root, width=40)
width_entry.pack(pady=5)

# Number 2
height_label = tk.Label(root, text="height:")
height_label.pack(pady=5)
height_entry = tk.Entry(root, width=40)
height_entry.pack(pady=5)

# Launch Button
launch_button = tk.Button(root, text="Launch Script", command=on_launch_button_click)
launch_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()









