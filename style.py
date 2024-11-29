import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas

def set_style():
    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=1, focusthickness=3, focuscolor="none", relief="solid", padding=5, bordercolor="gray", font=("Helvetica", 12))
    style.map("Rounded.TButton",
                relief=[("pressed", "groove"), ("!pressed", "solid")],
                bordercolor=[("hover", "darkblue"), ("!hover", "gray")])
    
    return style