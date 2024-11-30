import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

def logo(logo_path='files/aba_logo.jpg', width=70, height=70):
    logo = Image.open(logo_path)
    resized_logo = logo.resize((width, height), Image.LANCZOS)
    tk_logo = ImageTk.PhotoImage(resized_logo)
    return tk_logo
