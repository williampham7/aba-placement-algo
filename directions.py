import ttkbootstrap as tb
from tkinter import ttk

def directions_page(self):
    """
    Creates a scrollable directions page in a new window.
    """

    # Create a canvas for the scrollable frame
    canvas = tb.Canvas(self.app, highlightthickness=0)

    # Create a frame inside the canvas that will hold the content
    scrollable_frame = tb.Frame(canvas)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = ttk.Scrollbar(self.app, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, pady = (50,0), padx = 20)
    scrollbar.pack(side="right", fill="y")

    # Add the scrollable frame inside the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure scrolling behavior
    # Configure scrolling behavior
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    def _on_mouse_wheel(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")

    # Enable scrolling with the mouse wheel (adjusted for macOS touchpad)
    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)  # Windows and Linux
    canvas.bind_all("<Button-4>", _on_mouse_wheel)    # macOS (older systems)
    canvas.bind_all("<Button-5>", _on_mouse_wheel)    # macOS (older systems)
    canvas.bind_all("<Shift-MouseWheel>", lambda e: "break")  # Prevent horizontal scrolling


    # Directions Header
    header_label = tb.Label(
        scrollable_frame,
        text="Directions for Using the Team Generator Tool",
        font=("Microsoft YaHei UI", 20, "bold"),
        bootstyle="primary"
    )
    header_label.pack(pady=10)

    # Instructions List
    directions = [
        "1. Click 'Download Template & Example' to download the csv files.",
        "2. Fill out the Excel template with team member details. Refer to the example for guidance.",
        "3. Save the template in a location you can easily access.",
        "4. Click 'Generate Teams' and select the filled-out spreadsheet file.",
        "5. Change weights if desired (default is OK). Click Generate Teams.",
        "6. Wait for the tool to generate optimized teams based on the input data.",
        "7. Review the generated teams and export them if desired.",
        "8. If something is not working, call Will.",
    ]

    # Insert each instruction as a label inside the scrollable frame
    for step in directions:
        tb.Label(
            scrollable_frame,
            text=step,
            font=("Microsoft YaHei UI", 14),
            wraplength=640,
            justify="left",
            bootstyle="dark"
        ).pack(anchor="w", pady=5, padx=20)

def on_mouse_scroll(event, canvas):
    """Handle mouse wheel scroll events for macOS touchpad."""
    # On macOS, event.delta is a large number, and positive means scrolling up.
    # The factor -1 is used to invert the direction correctly for macOS.
    scroll_amount = -1 if event.delta > 0 else 1
    canvas.yview_scroll(scroll_amount, "units")