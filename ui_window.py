import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from algo import TeamAssignmentOptimizer
import os

from style import set_style

class TeamGenerator:
    def __init__(self):
        # Initialize the main application window
        self.app = ttk.Window(themename="litera")
        self.app.title("Team Generator Tool")
        self.app.geometry("600x450")
        style = ttk.Style()
        #set_style(style)

        self.input_path = ''

        # Create the home page
        self.home_page()

    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def home_page(self):
        self.clear_window()

        """Creates the home page UI components."""
        # Directions button
        directions_button = ttk.Button(
            self.app,
            text="See Directions",
            bootstyle=PRIMARY,
            width=20,
            command=self.show_directions
        )
        directions_button.pack(pady=(120, 10))

        # Download template button
        download_template_button = ttk.Button(
            self.app,
            text="Download Excel Template",
            bootstyle=SUCCESS,
            width=20,
            command=self.download_template
        )
        download_template_button.pack(pady=10)

        # Generate teams button
        generate_teams_button = ttk.Button(
            self.app,
            text="Generate Teams",
            bootstyle=DANGER,
            width=20,
            command=self.generate_teams
        )
        generate_teams_button.pack(pady=10)

        # Info button (top-right corner)
        info_button = ttk.Button(
            self.app,
            text="\u2139",  # Unicode for info symbol
            bootstyle=SECONDARY,
            command=self.show_info
        )
        info_button.place(relx=1.0, x=-10, y=10, anchor="ne")

    def show_directions(self):
        """Placeholder function for showing directions."""
        print("Directions")

    def download_template(self):
        """Placeholder function for downloading the Excel template."""
        print("Downloading Template")

    def generate_teams(self):
        self.clear_window()

        # Back button (top-left corner)
        back_button = ttk.Button(
            self.app,
            text="Back",  # Unicode for info symbol
            bootstyle=SECONDARY,
            command=self.home_page
        )
        back_button.place(relx=0.0, x=10, y=10, anchor="nw")

        """Creates the home page UI components."""
        # Directions button
        upload_data_button = ttk.Button(
            self.app,
            text="Upload Data",
            bootstyle=WARNING,
            width=20,
            command=self.upload_data
        )
        upload_data_button.pack(pady=(140, 10))

        self.input_status_label = ttk.Label(self.app, text="Select Input File...", bootstyle=INFO)
        self.input_status_label.pack(pady=10)

        solve_button = ttk.Button(
            self.app,
            text="Generate Teams",
            bootstyle=DANGER,
            width=20,
            command = lambda: self.solve_lp()
        )
        solve_button.pack(pady=(40, 10))

        # Status Label
        self.process_status_label = ttk.Label(self.app, text="", bootstyle=INFO)
        self.process_status_label.pack(pady=10)

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Spreadsheet Files", "*.xlsx *.csv")])
        if file_path:
            self.input_path = file_path
            self.input_status_label.config(text=f"Selected Input File: {os.path.basename(file_path)}")

    def solve_lp(self):
        if self.input_path:
            self.process_status_label.config(text="Processing...")
            solver = TeamAssignmentOptimizer(self.input_path)
            results = solver.solve([])
        else:
            self.process_status_label.config(text="No file selected")


    def show_results(self):
        pass

    def show_info(self):
        """Placeholder function for showing info."""
        print("Info")

    def run(self):
        """Runs the application."""
        self.app.mainloop()