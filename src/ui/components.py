import tkinter as tk
from tkinter import ttk


def create_ui(self):
    class Tooltip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tooltip_window = None
            self.id = None
            self.bind_events()

        def bind_events(self):
            self.widget.bind("<Enter>", self.show_tooltip)
            self.widget.bind("<Leave>", self.hide_tooltip)

        def show_tooltip(self, event=None):
            if self.tooltip_window is not None:
                return
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            self.tooltip_window = tk.Toplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip_window, text=self.text, background="gray", borderwidth=1, relief="solid")
            label.pack()

        def hide_tooltip(self, event=None):
            if self.tooltip_window:
                self.tooltip_window.destroy()
                self.tooltip_window = None

    style = ttk.Style()
    style.theme_use('clam')

    # Configure styles
    style.configure('TButton', padding=5, font=('Helvetica', 10))
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
    style.configure('TScale', background='#f0f0f0')

    # Main frame
    main_frame = ttk.Frame(self.master, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create canvas
    self.canvas = tk.Canvas(main_frame, bg="#ffffff", highlightthickness=0)
    self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Bind mouse wheel for zooming (CTRL + Scroll)
    self.master.bind("<Control-MouseWheel>", self.on_mouse_wheel)

    # Control frame
    control_frame = ttk.Frame(main_frame, padding="5")
    control_frame.pack(fill=tk.X, pady=10)

    # Navigation and Category frame
    nav_cat_frame = ttk.Frame(control_frame)
    nav_cat_frame.pack(side=tk.LEFT, padx=5)

    ttk.Button(nav_cat_frame, text="◀", command=self.prev_image, width=3).pack(side=tk.LEFT)
    ttk.Button(nav_cat_frame, text="▶", command=self.next_image, width=3).pack(side=tk.LEFT)

    categories = ["Delete", "Leave", "Good", "Medium"]
    for i, category in enumerate(categories):
        btn = ttk.Button(nav_cat_frame, text=category, command=lambda c=category: self.categorize(c))
        btn.pack(side=tk.LEFT)
        Tooltip(btn, f"{i + 1}")  # Add tooltip
        self.master.bind(str(i + 1), lambda e, c=category: self.categorize(c))

    # Undo Move Button
    btn = ttk.Button(nav_cat_frame, text="Undo Move", command=self.undo_move)
    btn.pack(side=tk.LEFT)
    Tooltip(btn, "Ctrl + U")  # Add tooltip
    self.master.bind('<Control-u>', lambda e: self.undo_move())

    # Zoom and Toggle Drag frame
    zoom_drag_frame = ttk.Frame(control_frame)
    zoom_drag_frame.pack(side=tk.LEFT, padx=5)

    zoom_in_btn = ttk.Button(zoom_drag_frame, text="🔍+", command=self.zoom_in, width=3)
    zoom_in_btn.pack(side=tk.LEFT)
    Tooltip(zoom_in_btn, "+")  # Tooltip for zoom in
    self.master.bind('+', lambda e: self.zoom_in())

    zoom_out_btn = ttk.Button(zoom_drag_frame, text="🔍-", command=self.zoom_out, width=3)
    zoom_out_btn.pack(side=tk.LEFT)
    Tooltip(zoom_out_btn, "-")  # Tooltip for zoom out
    self.master.bind('-', lambda e: self.zoom_out())

    toggle_drag_btn = ttk.Button(zoom_drag_frame, text="✋", command=self.toggle_drag, width=3)
    toggle_drag_btn.pack(side=tk.LEFT)
    Tooltip(toggle_drag_btn, "Ctrl + D")  # Tooltip for toggle drag
    self.master.bind('<Control-d>', lambda e: self.toggle_drag())

    # Action frame
    action_frame = ttk.Frame(control_frame)
    action_frame.pack(side=tk.LEFT, padx=5)

    load_images_btn = ttk.Button(action_frame, text="Load Images", command=self.load_images)
    load_images_btn.pack(side=tk.LEFT)
    Tooltip(load_images_btn, "Ctrl + L")  # Tooltip for load images
    self.master.bind('<Control-l>', lambda e: self.load_images())

    # Brush Control frame
    brush_frame = ttk.Frame(main_frame, padding="5")
    brush_frame.pack(fill=tk.X, pady=10)

    self.brush_size_var = tk.IntVar(value=5)
    ttk.Scale(brush_frame, from_=1, to=60, orient=tk.HORIZONTAL, variable=self.brush_size_var,
              command=self.update_brush_size, length=100).pack(side=tk.LEFT)
    ttk.Label(brush_frame, text="Brush Size").pack(side=tk.LEFT)

    black_brush_btn = ttk.Button(brush_frame, text="⚫", command=lambda: self.toggle_brush("black"), width=3)
    black_brush_btn.pack(side=tk.LEFT)
    Tooltip(black_brush_btn, "Ctrl + B")  # Tooltip for black brush
    self.master.bind('<Control-b>', lambda e: self.toggle_brush("black"))

    white_brush_btn = ttk.Button(brush_frame, text="⚪", command=lambda: self.toggle_brush("white"), width=3)
    white_brush_btn.pack(side=tk.LEFT)
    Tooltip(white_brush_btn, "Ctrl + W")  # Tooltip for white brush
    self.master.bind('<Control-w>', lambda e: self.toggle_brush("white"))

    undo_edit_btn = ttk.Button(brush_frame, text="Undo Edit", command=self.undo_brush)
    undo_edit_btn.pack(side=tk.LEFT)
    Tooltip(undo_edit_btn, "Ctrl + Z")  # Tooltip for undo edit
    self.master.bind('<Control-z>', lambda e: self.undo_brush())

    redo_edit_btn = ttk.Button(brush_frame, text="Redo Edit", command=self.redo_brush)
    redo_edit_btn.pack(side=tk.LEFT)
    Tooltip(redo_edit_btn, "Ctrl + Y")  # Tooltip for redo edit
    self.master.bind('<Control-y>', lambda e: self.redo_brush())

    remove_color_btn = ttk.Button(brush_frame, text="Remove Color", command=self.remove_color)
    remove_color_btn.pack(side=tk.LEFT, padx=(5, 0))
    Tooltip(remove_color_btn, "Ctrl + DELETE")  # Tooltip for remove color
    self.master.bind('<Control-Delete>', lambda e: self.remove_color())

    save_btn = ttk.Button(brush_frame, text="Save", command=self.save_image)
    save_btn.pack(side=tk.LEFT, padx=(5, 0))
    Tooltip(save_btn, "Ctrl + S")  # Tooltip for save image
    self.master.bind('<Control-s>', lambda e: self.save_image())

    # Bind canvas events
    self.canvas.bind("<ButtonPress-1>", self.start_paint)
    self.canvas.bind("<B1-Motion>", self.paint)
    self.canvas.bind("<ButtonRelease-1>", self.stop_paint)
    self.canvas.bind("<Motion>", self.show_brush_cursor)
    self.canvas.bind("<Leave>", lambda e: self.hide_brush_cursor())

    # Status bar
    self.status_var = tk.StringVar()
    status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(fill=tk.X, pady=(5, 0))

    # Update status bar
    self.update_status()


def update_status(self):
    if self.images:
        status = f"Image {self.current_index + 1} of {len(self.images)} | Zoom: {self.zoom_factor:.2f}x"
        if self.drag_enabled:
            status += " | Drag: On"
        if self.brush_enabled:
            status += f" | Brush: On (Size: {self.brush_size}, Color: {self.brush_color})"
    else:
        status = "No images loaded"
    self.status_var.set(status)

