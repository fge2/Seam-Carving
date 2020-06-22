import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Seam Carving")

        btn = tk.Button(self, text='open image', command=self.open_image)
        btn.pack()

        w = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=0, command=self.get_slider)
        w.set(100)
        w.pack(side='bottom')

        percentage = ''
        self.label = tk.Label(text=percentage)
        self.label.pack()

    def open_image(self):
        x = self.open_filename()
        print(x)
        img = Image.open(x)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self, image=img)
        panel.image = img
        panel.pack()

    def open_filename(self):
        filename = tk.filedialog.askopenfilename(title='"pen')
        return filename

    def get_slider(self, val):
        self.label["text"] = str(val) + '%'

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
