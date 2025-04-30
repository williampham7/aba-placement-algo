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
        self.center_window(700, 520)
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

        self.title = ttk.Label(self.top_frame, text="Team Optimizer", foreground="black", font=("Microsoft YaHei UI", 32, "bold"))
        self.title.pack(side=LEFT, padx=10)  # Place the title next to the logo with padding

        # Directions button
        directions_button = ttk.Button(
            self.app,
            text="Directions & Info",
            bootstyle=PRIMARY,
            width=30,
            command=self.show_directions
        )
        directions_button.pack(pady=10)

        # Download template button
        download_template_button = ttk.Button(
            self.app,
            text="Download Template & Example",
            bootstyle=SUCCESS,
            width=30,
            command=self.download_template_and_example
        )
        download_template_button.pack(pady=10)

        # Generate teams button
        generate_teams_button = ttk.Button(
            self.app,
            text="Generate Teams",
            bootstyle=DANGER,
            width=30,
            command=self.generate_teams
        )
        generate_teams_button.pack(pady=10)

    def show_directions(self):
        self.start_new_window()
        directions_page(self)

    def download_template_and_example(self):
        files_to_download = [
            ('files/candidates_template.csv', 'candidates_template.csv'),
            ('files/EXAMPLE_DATA-Spring2025.csv', 'EXAMPLE_DATA-Spring2025.csv')
        ]

        for template_path, default_name in files_to_download:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=default_name,
                title=f"Save {default_name}"
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
            width=30,
            command=self.upload_data
        )
        upload_data_button.grid(row=0, column=0, padx=10, pady=5)  # Placed at (0, 0)

        # Input status label
        self.input_status_label = ttk.Label(
            top_frame,
            text="Select Input File...",
            bootstyle=INFO
        )
        self.input_status_label.grid(row=1, column=0, padx=10, pady=3)  # Placed at (0, 1)

        solve_button = ttk.Button(
            top_frame,
            text="Generate Teams",
            bootstyle=DANGER,
            width=30,
            command = lambda: self.solve_lp()
        )
        solve_button.grid(row=0, column=1, padx=10, pady=5)

        # Status Label
        self.process_status_label = ttk.Label(top_frame, text="", bootstyle=INFO)
        self.process_status_label.grid(row=1, column=1, padx=10, pady=5)

        # Sliders
        self.slider_frame = ttk.Frame(self.app)
        self.slider_frame.pack(pady=5)
        
        # Add a title to the slider frame
        weights_title = ttk.Label(
            self.slider_frame,
            text="Weights",
            font=("Helvetica", 12, "bold"),
            anchor="center"
        )
        weights_title.pack()  # Add padding above and below the title

        # Initialize variables controlled by sliders
        # self.var1 = ttk.IntVar(value=3)  # Default value set to 3
        self.var2 = ttk.IntVar(value=3)
        self.var3 = ttk.IntVar(value=3)
        # self.var4 = ttk.IntVar(value=3)
        # self.var5 = ttk.IntVar(value=3)

        # Create sliders and labels
        # self.create_slider("Score", self.var1)
        self.create_slider("Team Preference", self.var2)
        self.create_slider("Role Preference", self.var3)
        # self.create_slider("ABA Semester", self.var4)
        # self.create_slider("School Year", self.var5)

    def create_results_buttons(self):

        bottom_frame = ttk.Frame(self.app)
        bottom_frame.pack(side = TOP, pady = 20)

        view_results_button = ttk.Button(
            bottom_frame,
            text="View Results",
            bootstyle=INFO,
            width=30,
            command = lambda: self.call_display()
        )
        view_results_button.grid(row=0, column=0, padx=10, pady=5)  # Placed at (0, 0)

        save_results_button = ttk.Button(
            bottom_frame,
            text="Save Results",
            bootstyle=SUCCESS,
            width=30,
            command = lambda: self.save_results(self.results)
        )
        save_results_button.grid(row=0, column=1, padx=10, pady=5)

    def create_slider(self, label_text, variable):
        """Helper to create an integer slider with a label."""
        label = ttk.Label(self.slider_frame, text=label_text, font=("Helvetica", 12))
        label.pack(anchor=W, pady=(0, 5))  # Align to the left and add spacing

        # Frame to hold the slider and its value
        slider_container = ttk.Frame(self.slider_frame)
        slider_container.pack(fill=X, pady=(0, 10))  # Add spacing below the slider

        slider = ttk.Scale(
            slider_container,
            from_=1,  # Minimum value
            to=5,     # Maximum value
            variable=variable,
            bootstyle=INFO,  # Custom ttkbootstrap style
            orient=HORIZONTAL,  # Horizontal slider
            length=300,
            command=lambda val: variable.set(round(float(val)))  # Snap to integers
        )
        slider.pack(side=LEFT, fill=X, expand=True)  # Align slider to the left
        slider.set(variable.get())  # Set the initial value

# Label to display the slider value
        value_label = ttk.Label(slider_container, text=str(variable.get()), font=("Helvetica", 12))
        value_label.pack(side=LEFT, padx=10)  # Place the value label to the right of the slider

# Update the value label dynamically
        def update_value_label(val):
            value_label.config(text=str(round(float(val))))

        slider.config(command=update_value_label)

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Spreadsheet Files", "*.xlsx *.csv")])
        if file_path:
            self.input_path = file_path
            self.input_status_label.config(text=f"Selected Input File: {os.path.basename(file_path)}")

    def solve_lp(self):
        if self.input_path:
            try:
                self.process_status_label.config(text="Processing...")
                solver = TeamAssignmentOptimizer(self.input_path, self.var2.get(), self.var3.get())
                self.results = solver.solve([])
                self.process_status_label.config(text="Finished ✅")
                self.create_results_buttons()
            except Exception as e:
                self.process_status_label.config(text="Error occurred ❌")
                messagebox.showerror("Error", f"An error occurred while processing:\n{str(e)}")
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