import tkinter as tk
from tkinter import ttk


def create_ui(self):
    style = ttk.Style()
    style.theme_use('clam')  # You can try other themes like 'alt', 'default', 'classic'

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
        ttk.Button(nav_cat_frame, text=category, command=lambda c=category: self.categorize(c)).pack(side=tk.LEFT)
        self.master.bind(str(i + 1), lambda e, c=category: self.categorize(c))

    ttk.Button(nav_cat_frame, text="Undo Move", command=self.undo_move).pack(side=tk.LEFT)

    # Zoom and Toggle Drag frame
    zoom_drag_frame = ttk.Frame(control_frame)
    zoom_drag_frame.pack(side=tk.LEFT, padx=5)

    ttk.Button(zoom_drag_frame, text="🔍+", command=self.zoom_in, width=3).pack(side=tk.LEFT)
    ttk.Button(zoom_drag_frame, text="🔍-", command=self.zoom_out, width=3).pack(side=tk.LEFT)
    ttk.Button(zoom_drag_frame, text="✋", command=self.toggle_drag, width=3).pack(side=tk.LEFT)

    # Action frame
    action_frame = ttk.Frame(control_frame)
    action_frame.pack(side=tk.LEFT, padx=5)

    ttk.Button(action_frame, text="Load Images", command=self.load_images).pack(side=tk.LEFT)

    # Brush Control frame
    brush_frame = ttk.Frame(main_frame, padding="5")
    brush_frame.pack(fill=tk.X, pady=10)

    self.brush_size_var = tk.IntVar(value=5)
    ttk.Scale(brush_frame, from_=1, to=60, orient=tk.HORIZONTAL, variable=self.brush_size_var,
              command=self.update_brush_size, length=100).pack(side=tk.LEFT)
    ttk.Label(brush_frame, text="Brush Size").pack(side=tk.LEFT)

    ttk.Button(brush_frame, text="⚫", command=lambda: self.toggle_brush("black"), width=3).pack(side=tk.LEFT)
    ttk.Button(brush_frame, text="⚪", command=lambda: self.toggle_brush("white"), width=3).pack(side=tk.LEFT)
    ttk.Button(brush_frame, text="Undo Edit", command=self.undo_brush).pack(
        side=tk.LEFT)  # Changed from "Undo Brush" to "Undo Edit"
    ttk.Button(brush_frame, text="Remove Color", command=self.remove_color).pack(side=tk.LEFT, padx=(5, 0))
    ttk.Button(brush_frame, text="Save", command=self.save_image).pack(side=tk.LEFT, padx=(5, 0))

    # Bind canvas events
    self.canvas.bind("<ButtonPress-1>", self.start_paint)
    self.canvas.bind("<B1-Motion>", self.paint)
    self.canvas.bind("<ButtonRelease-1>", self.stop_paint)  # Change this line
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
