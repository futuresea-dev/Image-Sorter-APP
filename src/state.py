class AppState:
    def __init__(self):
        self.zoom_factor = 1.0
        self.drag_enabled = False
        self.brush_enabled = False
        # ... other state variables ...

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
