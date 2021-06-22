from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.constants import *
from tkinter.scrolledtext import ScrolledText


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.image_folder_path = 'img/'
        self.image_file_extensions = {'.jpg', '.png'}
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.show_btn = tk.Button(self.root, text='Show Images', command=self.show_images)
        self.show_btn.grid(row=1, column=0)

        self.text = ScrolledText(self.root, wrap=WORD)
        self.text.grid(row=2, column=0, padx=10, pady=10)

        self.text.image_filenames = []
        self.text.images = []

    def show_images(self):
        ''' Create and display a list of the images the in folder that have one
            of the specified extensions. '''
        self.text.image_filenames.clear()
        for filepath in Path(self.image_folder_path).iterdir():
            if filepath.suffix in self.image_file_extensions:
                self.text.image_filenames.append(filepath)

        ''' Show the listed image names along with the images themselves. '''
        self.text.delete('1.0', END)  # Clear current contents.
        self.text.images.clear()
        # Display images in Text widget.
        for image_path in self.text.image_filenames:
            img = Image.open(image_path).resize((64, 64), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            self.text.insert(INSERT, image_path.name+'\n')
            self.text.image_create(INSERT, padx=5, pady=5, image=img)
            self.text.images.append(img)  # Keep a reference.
            self.text.insert(INSERT, '\n')

App()