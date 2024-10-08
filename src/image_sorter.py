import os
import shutil
from tkinter import filedialog, messagebox, Button, Toplevel, Label
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk, ImageDraw

from .ui.components import create_ui, update_status



class ImageSorter:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Sorter")
        self.master.geometry("800x600")

        # Initialize variables
        self.images = []
        self.current_index = 0
        self.zoom_factor = 1.0
        self.drag_enabled = False
        self.brush_enabled = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.brush_size = 5
        self.brush_color = "black"
        self.last_move = None
        self.move_history = []
        self.brush_history = []
        self.redo_history = []
        self.max_history = 80  # Increase the limit to 80 steps
        self.is_painting = False
        self.image_position = [0, 0]  # Track image position
        self.canvas = None
        self.tk_image = None
        # Create UI elements
        create_ui(self)

        # Bind keyboard events
        self.master.bind("<Left>", self.prev_image)
        self.master.bind("<Right>", self.next_image)
        self.master.bind("<Up>", self.zoom_in)
        self.master.bind("<Down>", self.zoom_out)
        self.master.bind("1", lambda e: self.categorize("Delete"))
        self.master.bind("2", lambda e: self.categorize("Leave"))
        self.master.bind("3", lambda e: self.categorize("Good"))
        self.master.bind("4", lambda e: self.categorize("Medium"))

        self._cursor_image = None  # Add this line
        self.brush_cursor = None
        self.brush_outline = None
        self.last_x = None
        self.last_y = None

    def on_mouse_wheel(self, event):
        if event.delta > 0:  # Scroll up
            self.zoom_in()
        else:  # Scroll down
            self.zoom_out()

    def update_status(self):
        update_status(self)

    def load_images(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            if self.images:
                self.current_index = 0
                self.display_image()
            else:
                messagebox.showinfo("No Images", "No images found in the selected folder.")

    def display_image(self):
        if self.images:
            image_path = self.images[self.current_index]
            self.original_image = Image.open(image_path)
            self.zoom_factor = self.calculate_zoom_factor()
            self.display_zoomed_image()

    def display_zoomed_image(self):
        if hasattr(self, 'original_image'):
            zoomed_size = (int(self.original_image.width * self.zoom_factor),
                           int(self.original_image.height * self.zoom_factor))
            zoomed_image = self.original_image.resize(zoomed_size, Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(zoomed_image)

            self.canvas.delete("all")
            self.canvas.create_image(self.image_position[0], self.image_position[1],
                                     anchor="nw", image=self.tk_image)

            self.update_status()

    def calculate_zoom_factor(self):
        if hasattr(self, 'original_image'):
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width, image_height = self.original_image.size
            width_ratio = canvas_width / image_width
            height_ratio = canvas_height / image_height
            return min(width_ratio, height_ratio) * 0.9  # 90% of the fitting size for padding

    def prev_image(self, event=None):
        if self.images:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.display_image()

    def next_image(self, event=None):
        if self.images:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.display_image()

    def zoom_in(self, event=None):
        self.zoom_factor *= 1.1
        self.display_zoomed_image()

    def zoom_out(self, event=None):
        self.zoom_factor /= 1.1
        self.display_zoomed_image()

    def toggle_drag(self):
        self.drag_enabled = not self.drag_enabled
        self.brush_enabled = False  # Disable brush when drag is enabled
        if self.drag_enabled:
            self.canvas.config(cursor="fleur")
        else:
            self.canvas.config(cursor="")
        self.update_status()

    def start_drag(self, event):
        if self.drag_enabled:
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def drag(self, event):
        if self.drag_enabled:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.image_position[0] += dx
            self.image_position[1] += dy
            self.canvas.move("all", dx, dy)
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def stop_drag(self, event):
        pass

    def update_brush_size(self, value):
        self.brush_size = int(float(value))  # Convert to float first, then to int
        if self.brush_enabled:
            self.update_brush_cursor()
        self.update_status()

    def set_brush_color(self, color):
        self.brush_color = color
        self.update_status()

    def save_painted_image(self):
        if hasattr(self, 'original_image'):
            self.original_image.save(self.images[self.current_index])
            messagebox.showinfo("Saved", "Image saved successfully.")

    def categorize(self, category):
        if self.images:
            src = self.images[self.current_index]
            dst_folder = os.path.join(os.path.dirname(src), category)
            os.makedirs(dst_folder, exist_ok=True)
            dst = os.path.join(dst_folder, os.path.basename(src))
            shutil.move(src, dst)
            self.move_history.append((src, dst))  # Record the move
            self.images.pop(self.current_index)
            if self.images:
                self.current_index %= len(self.images)
                self.display_image()
            else:
                self.canvas.delete("all")
                messagebox.showinfo("Finished", "All images have been categorized.")
        self.update_status()

    def undo_move(self):
        if self.move_history:
            src, dst = self.move_history.pop()
            try:
                # Move the image back to its original location
                shutil.move(dst, src)
                # Add the image back to the list and update the current index
                self.images.insert(self.current_index, src)
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to undo move: {str(e)}")
        else:
            messagebox.showinfo("Undo", "No more moves to undo.")

    def create_undo_all_button(self, command):
        undo_all_button = Button(self.button_frame, text="Undo All Moves", command=command)
        undo_all_button.pack(side=tk.LEFT, padx=5)

    def move_image(self, destination):
        # ... (existing move_image code) ...
        image_path = self.images[self.current_index]
        self.move_history.append((image_path, self.current_folder, destination))
        # ... (rest of the existing move_image code) ...

    def toggle_brush(self, color):
        if self.brush_enabled and self.brush_color == color:
            self.brush_enabled = False
            self.hide_brush_cursor()
        else:
            self.brush_enabled = True
            self.brush_color = color
            self.show_brush_cursor()
        self.update_status()

    def show_brush_cursor(self, event=None):
        if self.brush_enabled:
            x, y = event.x if event else 0, event.y if event else 0
            self.update_brush_cursor(x, y)

    def hide_brush_cursor(self):
        if self.brush_cursor:
            self.canvas.delete(self.brush_cursor)
            self.brush_cursor = None
        if self.brush_outline:
            self.canvas.delete(self.brush_outline)
            self.brush_outline = None

    def update_brush_cursor(self, x=0, y=0):
        self.hide_brush_cursor()
        if self.brush_enabled:
            size = int(self.brush_size * self.zoom_factor)  # Adjust for zoom
            # Create the brush cursor with the exact size of the brush
            self.brush_cursor = self.canvas.create_oval(
                x - size // 2, y - size // 2,
                x + size // 2 - 1, y + size // 2 - 1,  # Subtract 1 to match exact size
                fill='', outline=self.brush_color
            )
            # Create a slightly larger outline for visibility
            outline_color = "white" if self.brush_color == "black" else "black"
            self.brush_outline = self.canvas.create_oval(
                x - size // 2 - 1, y - size // 2 - 1,
                x + size // 2, y + size // 2,
                outline=outline_color
            )

    def start_paint(self, event):
        if self.brush_enabled:
            self.is_painting = True
            self.brush_history.append(self.original_image.copy())
            if len(self.brush_history) > self.max_history:
                self.brush_history.pop(0)
            self.last_x = event.x
            self.last_y = event.y
            self.paint(event)
        elif self.drag_enabled:
            self.start_drag(event)

    def paint(self, event):
        if self.brush_enabled and hasattr(self, 'original_image') and self.is_painting:
            try:
                # Calculate the position relative to the image
                x = (event.x - self.image_position[0]) / self.zoom_factor
                y = (event.y - self.image_position[1]) / self.zoom_factor

                if 0 <= x < self.original_image.width and 0 <= y < self.original_image.height:
                    draw = ImageDraw.Draw(self.original_image)

                    if self.last_x is not None and self.last_y is not None:
                        last_x = (self.last_x - self.image_position[0]) / self.zoom_factor
                        last_y = (self.last_y - self.image_position[1]) / self.zoom_factor
                        self.draw_smooth_line(draw, last_x, last_y, x, y)
                    else:
                        draw.ellipse([x - self.brush_size // 2, y - self.brush_size // 2,
                                      x + self.brush_size // 2, y + self.brush_size // 2],
                                     fill=self.brush_color, outline=self.brush_color)

                    self.last_x = event.x
                    self.last_y = event.y

                    self.display_zoomed_image()
                    self.update_brush_cursor(event.x, event.y)
            except Exception as e:
                print(f"Error in paint method: {str(e)}")
        elif self.drag_enabled:
            self.drag(event)

    def draw_smooth_line(self, draw, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        distance = int((dx ** 2 + dy ** 2) ** 0.5)

        if distance == 0:
            draw.ellipse([x1 - self.brush_size // 2, y1 - self.brush_size // 2,
                          x1 + self.brush_size // 2, y1 + self.brush_size // 2],
                         fill=self.brush_color, outline=self.brush_color)
            return

        for i in range(distance + 1):
            t = i / distance
            x = x1 + t * dx
            y = y1 + t * dy
            draw.ellipse([x - self.brush_size // 2, y - self.brush_size // 2,
                          x + self.brush_size // 2, y + self.brush_size // 2],
                         fill=self.brush_color, outline=self.brush_color)

    def stop_paint(self, event):
        self.is_painting = False
        self.last_x = None
        self.last_y = None

    def undo_brush(self):
        if self.brush_history:
            last_brush_state = self.brush_history.pop()
            self.redo_history.append(last_brush_state)  # Save the state for redo
            self.original_image = self.brush_history[-1] if self.brush_history else last_brush_state
            self.display_zoomed_image()

            if not self.brush_history:
                messagebox.showinfo("Undo", "No more actions to undo.")
        else:
            messagebox.showinfo("Undo", "No actions to undo.")

    def redo_brush(self):
        if self.redo_history:
            self.brush_history.append(self.redo_history.pop())  # Restore the last undone state
            self.original_image = self.brush_history[-1]
            self.display_zoomed_image()
        else:
            messagebox.showinfo("Redo", "No actions to redo.")

    def save_image(self):
        if hasattr(self, 'original_image') and self.images:
            current_image_path = self.images[self.current_index]
            self.original_image.save(current_image_path)
            print(f"Image saved: {current_image_path}")
            self.show_temp_message("Image saved successfully")

    def show_temp_message(self, message):
        popup = Toplevel(self.master)
        popup.wm_overrideredirect(True)
        x = self.master.winfo_x() + self.master.winfo_width() // 2 - 100
        y = self.master.winfo_y() + self.master.winfo_height() - 50
        popup.geometry(f"200x30+{x}+{y}")
        Label(popup, text=message, bg='lightgreen', fg='black').pack(fill='both', expand=True)
        popup.after(2000, popup.destroy)

    def remove_color(self):
        if hasattr(self, 'original_image'):
            # Convert image to numpy array for faster processing
            img_array = np.array(self.original_image)

            # Calculate brightness using the luminance formula
            brightness = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]

            # Create a mask for pixels above the threshold
            threshold = 128  # Adjust this threshold as needed
            mask = brightness > threshold

            # Set pixels below the threshold to black
            img_array[~mask] = [0, 0, 0]

            # Convert the numpy array back to a PIL image
            self.original_image = Image.fromarray(img_array)
            self.display_zoomed_image()
            self.show_temp_message("Color removal applied")

    # Tooltip Class


