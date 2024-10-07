from tkinter import Tk, messagebox

from PIL import Image

from src.image_sorter import ImageSorter


class CustomImageSorter(ImageSorter):
    def __init__(self, master):
        super().__init__(master)

    def remove_color(self):
        if hasattr(self, 'current_index') and self.current_index is not None and self.current_index < len(self.images):
            current_image_path = self.images[self.current_index]
            # Save the current state before removing color
            self.brush_history.append(self.original_image.copy())
            if len(self.brush_history) > self.max_history:
                self.brush_history.pop(0)
            self.convert_to_black_and_dark(current_image_path, current_image_path)
            self.display_image()  # Refresh the displayed image
        else:
            messagebox.showwarning("Warning", "No image is currently displayed.")

    def convert_to_black_and_dark(self, image_path, output_path, threshold=50):
        try:
            img = Image.open(image_path).convert('L')  # Convert to grayscale
            img = img.point(lambda p: p > threshold and 255)  # Adjust threshold for darkness
            img.save(output_path)
            # Removed the messagebox.showinfo line
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_image(self):
        super().display_image()
        # If any additional refresh is needed, add it here


if __name__ == "__main__":
    root = Tk()
    app = CustomImageSorter(root)
    root.mainloop()
