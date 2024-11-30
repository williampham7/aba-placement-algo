import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from algo import TeamAssignmentOptimizer
from png import logo
import os, time, webbrowser, shutil
from datetime import datetime
from results_page import display_team_results
from directions import directions_page

from style import set_style

class TeamGenerator:
    def __init__(self):
        # Initialize the main application window
        self.app = ttk.Window(themename="litera")
        self.app.title("Team Generator Tool")
        self.center_window(600, 520)
        style = ttk.Style()
        #set_style(style)

        self.input_path = ''

        # Create the home page
        self.home_page()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        # Calculate the position for the window to appear centered
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - int(height // 1.8)

        # Set the geometry with the new x, y positions
        self.app.geometry(f"{width}x{height}+{x}+{y}")

    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def home_page(self):
        self.clear_window()

        """Creates the home page UI components."""

        self.top_frame = ttk.Frame(self.app)
        self.top_frame.pack(side = TOP, pady = 60)

        tk_logo = logo()
        self.logo = ttk.Label(self.top_frame, image=tk_logo)
        self.logo.pack(side=LEFT, padx=10)  # Place the logo on the left with padding
        self.logo.image = tk_logo

        self.title = ttk.Label(self.top_frame, text="Team Optimizer", foreground="black", font=("Helevetica", 32, "bold"))
        self.title.pack(side=LEFT, padx=10)  # Place the title next to the logo with padding

        # Directions button
        directions_button = ttk.Button(
            self.app,
            text="Directions & Info",
            bootstyle=PRIMARY,
            width=20,
            command=self.show_directions
        )
        directions_button.pack(pady=10)

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

    def show_directions(self):
        self.start_new_window()
        directions_page(self)

    def download_template(self):
        template_path = 'files/candidates_template.csv'

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="candidates_template.csv",
            title="Save Template File"
        )

        if file_path:
            shutil.copyfile(template_path, file_path)

    def generate_teams(self):
        self.start_new_window()

        top_frame = ttk.Frame(self.app)
        top_frame.pack(side = TOP, pady = (55,10))

        upload_data_button = ttk.Button(
            top_frame,
            text="Upload Data",
            bootstyle=WARNING,
            width=20,
            command=self.upload_data
        )
        upload_data_button.grid(row=0, column=0, padx=10, pady=5)  # Placed at (0, 0)

        # Input status label
        self.input_status_label = ttk.Label(
            top_frame,
            text="Select Input File...",
            bootstyle=INFO
        )
        self.input_status_label.grid(row=1, column=0, padx=10, pady=5)  # Placed at (0, 1)

        solve_button = ttk.Button(
            top_frame,
            text="Generate Teams",
            bootstyle=DANGER,
            width=20,
            command = lambda: self.solve_lp()
        )
        solve_button.grid(row=0, column=1, padx=10, pady=5)

        # Status Label
        self.process_status_label = ttk.Label(top_frame, text="", bootstyle=INFO)
        self.process_status_label.grid(row=1, column=1, padx=10, pady=5)

        # Sliders
        self.slider_frame = ttk.Frame(self.app)
        self.slider_frame.pack(pady=10)

        # Initialize variables controlled by sliders
        self.var1 = ttk.IntVar(value=50)
        self.var2 = ttk.IntVar(value=50)
        #self.var3 = ttk.IntVar(value=50)
        #self.var4 = ttk.IntVar(value=50)
        #self.var5 = ttk.IntVar(value=50)

        # Create sliders and labels
        self.create_slider("Variable 1", self.var1)
        self.create_slider("Variable 2", self.var2)
        #self.create_slider("Variable 3", self.var3)
        #self.create_slider("Variable 4", self.var4)
        #self.create_slider("Variable 5", self.var5)

    def create_results_buttons(self):

        bottom_frame = ttk.Frame(self.app)
        bottom_frame.pack(side = TOP, pady = 20)

        view_results_button = ttk.Button(
            bottom_frame,
            text="View Results",
            bootstyle=INFO,
            width=20,
            command = lambda: self.call_display()
        )
        view_results_button.grid(row=0, column=0, padx=10, pady=5)  # Placed at (0, 0)

        save_results_button = ttk.Button(
            bottom_frame,
            text="Save Results",
            bootstyle=SUCCESS,
            width=20,
            command = lambda: self.save_results(self.results)
        )
        save_results_button.grid(row=0, column=1, padx=10, pady=5)

    def create_slider(self, label_text, variable):
            """Helper to create a slider with a label."""
            label = ttk.Label(self.slider_frame, text=label_text, font=("Helvetica", 12))
            label.pack(anchor=W, pady=(0, 5))  # Align to the left and add spacing

            slider = ttk.Scale(
                self.slider_frame,
                from_=0,  # Minimum value
                to=100,   # Maximum value
                variable=variable,
                bootstyle=INFO,  # Custom ttkbootstrap style
                orient=HORIZONTAL,  # Horizontal slider
                length=300
            )
            slider.pack(fill=X, pady=(0, 10))  # Fill the available space horizontally

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Spreadsheet Files", "*.xlsx *.csv")])
        if file_path:
            self.input_path = file_path
            self.input_status_label.config(text=f"Selected Input File: {os.path.basename(file_path)}")

    def solve_lp(self):
        if self.input_path:
            self.process_status_label.config(text="Processing...")
            solver = TeamAssignmentOptimizer(self.input_path)
            self.results = solver.solve([])
            self.process_status_label.config(text="Finished ✅")
            self.create_results_buttons()

        else:
            self.process_status_label.config(text="No file selected")

    def call_display(self):
        display_team_results(self.results)


    def save_results(self, results):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_file_name = f"Team_Assignments_{timestamp}.csv"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=default_file_name,
            title="Save File As"
        )

        if file_path:  # If the user selects a location
            # Save the DataFrame to the chosen location
            results.to_csv(file_path, index=False)
            print(f"Sorted assignments saved to {file_path}.")
            
            # Automatically open the CSV file in the default viewer
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS or Linux
                webbrowser.open(f"file://{file_path}")

    def start_new_window(self):
        self.clear_window()

        # Back button (top-left corner)
        back_button = ttk.Button(
            self.app,
            text="Back",  # Unicode for info symbol
            bootstyle=SECONDARY,
            command=self.home_page
        )
        back_button.place(relx=0.0, x=10, y=10, anchor="nw")

    def run(self):
        """Runs the application."""
        self.app.mainloop()