import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas

def set_style(style):
    style.configure("Rounded.TButton", borderwidth=1, bordercolor="#ccc", focusthickness=0, borderradius=15)