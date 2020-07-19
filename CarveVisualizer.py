import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import ImageTk, Image
from SeamCarving import Picture
import datetime
import time
import math

# Visualization and interactive GUI using tkinter library and api
class App(tk.Frame):

    # Create master frame with buttons and default image
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Seam Carving")

        # button widgets for loading and saving images
        load_save = tk.Frame(self)
        open = tk.Button(load_save, text='open image', command=self.open_image)
        open.grid(row=0, column=0)
        save = tk.Button(load_save, text='save', command=self.save_image)
        save.grid(row=0, column=1, padx=5)
        load_save.grid(row=0)

        # slider widget to determine % resize
        slider_frame = tk.Frame(self)
        self.resize = tk.Scale(slider_frame, from_=0, to=10000, orient=tk.HORIZONTAL, showvalue=0, length=200)
        self.max = 10000
        self.resize['command'] = self.get_slider
        self.resize.grid(row=0)
        self.scalelabel = tk.Label(slider_frame, text="100.00%")
        self.scalelabel.grid(row=1)
        slider_frame.grid(row=2)
     
        # button widget to run seamcarving alg
        func = tk.Button(self, text='carve', command=self.carve)
        func.grid(row=3)

        self.panel = tk.Label(self)
        self.open_image('HJoceanSmall.png')
        self.panel.grid(row=1, pady=2)

    # open image and resize window to fit image
    def open_image(self, default=False):
        if default:
            x = default
        else:
            x = self.open_filename()
        if not x:
            return

        self.pic = Picture(x)
        self.init_width = self.pic.width
        self.update_im()

        self.master.geometry("%dx%d" % (self.pic.width, self.pic.height+100))
        self.master.resizable(False, False)
        self.resize.set(10000)

    # helper function for open_image
    def open_filename(self):
        filename = tk.filedialog.askopenfilename(title='"pen')
        return filename
            
    # save function
    def save_image(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if file:
            im = cv2.cvtColor(self.pic.im, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im)
            im.save(file)

    # helper function to update image in panel on loop update
    def update_im(self):
        im = cv2.cvtColor(self.pic.im, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        self.panel.config(image=im)
        self.panel.image = im

    # set slider % value on interface
    def get_slider(self, val):
        if float(val) > self.max:
            self.resize.set(self.max)
            val = self.max
        self.scalelabel["text"] = str(float(val)/100) + '%'
        self.new_width = int(float(val)/10000 * self.init_width)
        
    # highlight and remove images until desired size reached
    def carve(self):
        if self.pic.width < 3 or self.pic.width < self.new_width:
            self.update_im()
            return

        self.max = min(self.resize.get(), self.max)
        mask = self.pic.create_mask()
        self.pic.highlight(mask)
        self.update_im()
        self.after(1, self.pic.remove_seam(mask))
        self.after(1, self.carve)

# main method to create the GUI
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
