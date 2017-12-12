from tkinter import *
from reaTAMain import *
import os

CURR_DIR_PATH = str(os.getcwd()).replace("\\", "/")


class UIApp:
    def __init__(self):
        self.window = Tk()
        self.existing_monitors = []
        self.listbox = Listbox(self.window)
        self.init_ui()
        self.window.mainloop()

    def init_ui(self):
        Label(self.window, text="ReaTA Monitor").pack()
        self.window.geometry("400x235")
        self.window.resizable(width=False, height=False)
        self.window.title("ReaTA")
        self.window.iconbitmap(r"graph-line-screen.ico")
        self.listbox.pack(fill=BOTH, expand=2)
        self.listbox.pack()
        Button(self.window, text='Hide All', command=self.invokehideAll).pack(side=RIGHT, anchor=W, fill=BOTH, expand=YES)
        Button(self.window, text='Quit', command=self.window.quit).pack(side=BOTTOM, anchor=W, fill=X, expand=YES)
        Button(self.window, text='Add', command=self.invokeCreateMonitor).pack(side=LEFT, anchor=W, fill=X, expand=YES)
        Button(self.window, text='Delete', command=self.invokeDeleteMonitor).pack(side=LEFT, anchor=W, fill=X, expand=YES)
        Button(self.window, text='Show', command=self.invokeShowMonitor).pack(side=LEFT, anchor=W, fill=X, expand=YES)
        Button(self.window, text='Hide', command=self.invokeHideMonitor).pack(side=LEFT, anchor=W, fill=X, expand=YES)
        self.update()

    def invokehideAll(self):
        hideAllMonitors()
        self.update()

    def invokeCreateMonitor(self):
        createAMonitor()
        self.update()

    def invokeHideMonitor(self):
        hideAMonitor(self.listbox.get(ACTIVE))
        self.update()

    def invokeShowMonitor(self):
        showAMonitor(self.listbox.get(ACTIVE))
        self.update()

    def invokeDeleteMonitor(self):
        deleteMonitor(self.listbox.get(ACTIVE))
        self.update()

    def update(self):
        monitors = []
        self.listbox.delete(0, END)
        for file in os.listdir(CURR_DIR_PATH):
            if 'monitor-' in file:
                filename = file[file.find("-") + 1:]
                monitors.append(filename)
                self.listbox.insert(END, filename)
        self.existing_monitors = monitors

