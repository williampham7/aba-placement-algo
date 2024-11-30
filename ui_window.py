import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from algo import TeamAssignmentOptimizer
from png import logo
import os, time, webbrowser
from datetime import datetime
from results_page import display_team_results

from style import set_style

class TeamGenerator:
    def __init__(self):
        # Initialize the main application window
        self.app = ttk.Window(themename="litera")
        self.app.title("Team Generator Tool")
        self.app.geometry("600x520")
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
            text="See Directions",
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
        upload_data_button.pack(pady=(40, 10))

        self.input_status_label = ttk.Label(self.app, text="Select Input File...", bootstyle=INFO)
        self.input_status_label.pack(pady=10)

        self.slider_frame = ttk.Frame(self.app)
        self.slider_frame.pack(pady=10)

        # Initialize variables controlled by sliders
        self.var1 = ttk.IntVar(value=50)
        self.var2 = ttk.IntVar(value=50)
        self.var3 = ttk.IntVar(value=50)
        self.var4 = ttk.IntVar(value=50)
        self.var5 = ttk.IntVar(value=50)

        # Create sliders and labels
        self.create_slider("Variable 1", self.var1)
        self.create_slider("Variable 2", self.var2)
        self.create_slider("Variable 3", self.var3)
        self.create_slider("Variable 4", self.var4)
        self.create_slider("Variable 5", self.var5)

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
            results = solver.solve([])
            
            time.sleep(1)
            self.process_status_label.config(text="Finished ✅")

            display_team_results(results)
            # self.save_results(results)

        else:
            self.process_status_label.config(text="No file selected")


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

    def show_info(self):
        """Placeholder function for showing info."""
        print("Info")

    def run(self):
        """Runs the application."""
        self.app.mainloop()