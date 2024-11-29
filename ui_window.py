import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from style import set_style

def create_ui():
    # Initialize the main window
    app = ttk.Window(themename="solar")
    app.title("Team Generator Tool")
    app.geometry("400x350")
    # style = set_style()

    # Create and place the buttons
    directions_button = ttk.Button(app, text="See Directions", bootstyle=PRIMARY, width = 20, command=lambda: print("Directions"))
    directions_button.pack(pady=(80,10))

    download_template_button = ttk.Button(app, text="Download Excel Template", bootstyle=SUCCESS, width = 20, command=lambda: print("Downloading Template"))
    download_template_button.pack(pady=10)

    generate_teams_button = ttk.Button(app, text="Generate Teams", bootstyle=WARNING, width = 20, command=lambda: print("Generating Teams"))
    generate_teams_button.pack(pady=10)

    # Add an info button in the top-right corner
    info_button = ttk.Button(app, text="ℹ️", bootstyle=SECONDARY, command=lambda: print("Info"))
    info_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    # Run the application
    app.mainloop()