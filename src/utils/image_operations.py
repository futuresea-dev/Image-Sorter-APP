import os
from tkinter import filedialog, messagebox, NW

from PIL import Image, ImageTk


def load_images(self):
    folder_path = filedialog.askdirectory()
    if folder_path:
        self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if self.images:
            self.current_index = 0
            self.display_image()
        else:
            messagebox.showinfo("No Images", "No compatible images found in the selected folder.")


def display_image(self):
    if self.images:
        image_path = self.images[self.current_index]
        self.original_image = Image.open(image_path)
        self.display_zoomed_image()


def display_zoomed_image(self):
    if hasattr(self, 'original_image'):
        # Calculate new size
        new_width = int(self.original_image.width * self.zoom_factor)
        new_height = int(self.original_image.height * self.zoom_factor)

        # Resize image
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)

        # Convert to PhotoImage
        self.tk_image = ImageTk.PhotoImage(resized_image)

        # Clear canvas and display new image
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)
