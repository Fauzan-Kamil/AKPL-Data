#Library
import sys
from PIL import ImageTk, Image
from threading import Thread
import tkinter as tk
from tkinter import filedialog, ttk

x = 600
y = 600


#Start Frame
class DataImage(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.init_ui()

    def init_ui(self):
        self.pack()
        self.label = tk.Label(self, text='Data Wajah', font=('Helvetica', 25))
        self.label.pack()
        self.openbtn = tk.Button(self, text='Open Image', command=self.open_image)
        self.openbtn.pack()
#        self.renamebtn = tk.Button(self, text='Rename', command=self.rename)
#        self.renamebtn.pack()
        self.imageframe = tk.LabelFrame(self, text='Image View')
        self.imageframe.pack()
        self.labelimage = tk.Label(self.imageframe, width=100, height=30)
        self.labelimage.pack()

#End Frame

#Start Open Image
    def open_image(self):
        self.filename = filedialog.askopenfilename()
        self.image = Image.open(self.filename)
        self.image = self.image.resize((x, y))
        self.imagetk = ImageTk.PhotoImage(self.image)
        self.labelimage.configure(image=self.imagetk, width=x, height=y)
#End Open Image

#Start Rename
#    def rename(self):
#        self.filename = filedialog.askopenfilename()
#        self.image = Image.open(self.filename)
#        self.image = self.image.resize((x, y))
#        self.imagetk = ImageTk.PhotoImage(self.image)
#        self.labelimage.configure(image=self.imagetk, width=x, height=y)
#End Rename

#Config
window = tk.Tk()
gui = DataImage(window)
window.geometry(f'{x}x{y}')
window.title("Data Presensi")
window.mainloop()