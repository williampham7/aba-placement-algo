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

    # Enable scrolling with the mouse wheel (adjust for macOS)
    scrollable_frame.bind_all("<MouseWheel>", lambda e: on_mouse_scroll(e, canvas))
    scrollable_frame.bind_all("<Shift-MouseWheel>", lambda e: on_shift_scroll(e, canvas))

    # Directions Header
    header_label = tb.Label(
        scrollable_frame,
        text="Directions for Using the Team Generator Tool",
        font=("Helvetica", 20, "bold"),
        bootstyle="primary"
    )
    header_label.pack(pady=10)

    # Instructions List
    directions = [
        "1. Click 'Download Excel Template' to download the required input file.",
        "2. Fill out the Excel template with team member details.",
        "3. Save the template in a location you can easily access.",
        "4. Click 'Generate Teams' and select the filled-out Excel file.",
        "5. Wait for the tool to generate optimized teams based on the input data.",
        "6. Review the generated teams and export them if needed.",
        "7. If you need further assistance, click 'See Directions' for guidance.",
        "1. Click 'Download Excel Template' to download the required input file.",
        "2. Fill out the Excel template with team member details.",
        "3. Save the template in a location you can easily access.",
        "4. Click 'Generate Teams' and select the filled-out Excel file.",
        "5. Wait for the tool to generate optimized teams based on the input data.",
        "6. Review the generated teams and export them if needed.",
        "7. If you need further assistance, click 'See Directions' for guidance.",
        "1. Click 'Download Excel Template' to download the required input file.",
        "2. Fill out the Excel template with team member details.",
        "3. Save the template in a location you can easily access.",
        "4. Click 'Generate Teams' and select the filled-out Excel file.",
        "5. Wait for the tool to generate optimized teams based on the input data.",
        "6. Review the generated teams and export them if needed.",
        "7. If you need further assistance, click 'See Directions' for guidance."
    ]

    # Insert each instruction as a label inside the scrollable frame
    for step in directions:
        tb.Label(
            scrollable_frame,
            text=step,
            font=("Arial", 14),
            wraplength=550,
            justify="left",
            bootstyle="dark"
        ).pack(anchor="w", pady=5, padx=20)

def on_mouse_scroll(event, canvas):
    """Handle mouse wheel scroll events for macOS and other platforms."""
    if event.state == 0:  # Vertical scrolling
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    elif event.state == 1:  # Horizontal scrolling (Shift key pressed)
        canvas.xview_scroll(-1 * (event.delta // 120), "units")


def on_shift_scroll(event, canvas):
    """Handle shift + mouse wheel events for horizontal scrolling."""
    canvas.xview_scroll(-1 * (event.delta // 120), "units")