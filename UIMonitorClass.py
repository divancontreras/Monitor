from tkinter import ttk
import tkinter
import threading
from Monitors import *
import os, time
from ctypes import windll
import ctypes
from ctypes import wintypes

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

user32 = ctypes.WinDLL('user32', use_last_error=True)

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,    # _In_ hWnd
    wintypes.LPARAM,) # _In_ lParam

CURR_DIR_PATH = str(os.getcwd()).replace("\\", "/")


class UIApp:
    def __init__(self):
        self.window = Tk()
        threading.Thread(target=self.checkRunningProjects).start()
        self.running_picto = PhotoImage(file="resources\on_screen.png")
        self.not_running_picto = PhotoImage(file="resources\off_screen.png")
        self.count_active_projects = 0
        self.existing_monitors = []
        self.top = None
        self.strin = None
        self.original_value = 10
        self.close_img = PhotoImage(file=r'resources\close_button.png')
        self.open_img = PhotoImage(file=r'resources\open_button.png')
        self.close_all_img = PhotoImage(file=r'resources\close_all_button.png')
        self.add_img = PhotoImage(file=r'resources\add_button.png')
        self.delete_img = PhotoImage(file=r'resources\delete_button.png')
        self.init_ui()
        self.window.overrideredirect(1)
        self.window.after(10, lambda: self.set_appwindow(self.window))
        self.window.mainloop()


    def init_ui(self):
        header_frame = Frame(self.window, width=820, height=100, bg="#3dcd58")
        header_frame.pack(fill=BOTH)
        body_frame = Frame(self.window, width=820, height=324, bg="#FFFFFF")
        body_frame.pack(fill=BOTH)
        top_frame = Frame(body_frame, width=820, height=200, bg="#FFFFFF")
        top_frame.pack(side=TOP,fill=BOTH, padx=(20, 20), pady=(20, 20))
        bot_frame = Frame(body_frame, width=820, height=32, bg="#FFFFFF")
        bot_frame.pack(side=BOTTOM, fill=Y)
        bottom_frame = Frame(self.window, width=820, height=50, bg="#FFFFFF")
        bottom_frame.pack(fill=BOTH, expand=True)
        img = PhotoImage(file=r'resources\LIO_SE_logo_100px.png')
        icon_frame = Label(bottom_frame, height=40, width=195, bg="#FFFFFF", image=img, highlightthickness=0, borderwidth=0)
        icon_frame.photo = img
        icon_frame.pack(side=RIGHT, fill=BOTH, padx=(0, 20))
        lefty_bottom = Frame(bottom_frame, width=820, height=30, bg="#FFFFFF")
        lefty_bottom.pack(side=LEFT, fill=BOTH, expand=True)


        header_uppper_frame = Frame(header_frame, width=820, height=64, bg="#FFFFFF")
        header_bottom_frame = Frame(header_frame, width=820, height=32)

        header_uppper_frame.pack(side=TOP, fill=BOTH)
        header_bottom_frame.pack(side=BOTTOM, fill=BOTH)

        img = PhotoImage(file=r'resources\Main.png')
        icon_frame_1 = Label(header_uppper_frame, height=64, width=780, image=img, highlightthickness=0, borderwidth=0)
        icon_frame_1.photo = img
        img = PhotoImage(file=r'resources\exit.png')
        exit_button = Label(header_uppper_frame, height=64, width=40, image=img, bg="#FFFFFF",
                            highlightthickness=0, borderwidth=0)
        exit_button.photo = img
        exit_button.bind('<Button-1>', exit_window)
        exit_button.pack(side=RIGHT, fill=BOTH, padx=(0, 10))
        icon_frame_1.pack(side=LEFT, fill=BOTH)


        img = PhotoImage(file=r'resources\projects.png')
        icon_frame = Label(header_bottom_frame, height=32, width=820, image=img, highlightthickness=0, borderwidth=0)
        icon_frame.photo = img
        icon_frame.pack(fill=BOTH)


        self.window.bind("<ButtonPress-1>", self.start_move)
        self.window.bind('<ButtonRelease-1>', self.stop_move)
        self.window.bind("<B1-Motion>", self.on_motion)
        self.window.geometry("820x580")
        self.window.resizable(width=False, height=False)
        self.window.title("Monitors")
        self.window.iconbitmap(r"resources\monitor_icon.ico")
        self.listbox = ttk.Treeview(top_frame, columns=("Project Name", "Added Date"))
        self.listbox.heading('#0', text='Status', anchor="center")
        self.listbox.heading('#1', text='Project Name', anchor='center')
        self.listbox.heading('#2', text='Added Date', anchor='center')
        self.listbox.column("#0", width=20)
        self.listbox.column('#1', width=400)
        self.listbox.column('#2',width=50)
        style = ttk.Style()
        self.listbox.pack(fill=BOTH)
        style.layout("Treeview.Item",
                     [('Treeitem.padding', {'sticky': 'nswe', 'children':
                         [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                          ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                          # ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [
                          ('Treeitem.text', {'side': 'left', 'sticky': ''}),
                          # ]})
                          ],
                                            })]
                     )
        style.configure('Treeview', rowheight=25)
        self.popup_menu = tkinter.Menu(self.listbox, tearoff=0)
        self.listbox.bind("<Button-3>", self.popup) # Button-2 on Aqua
        self.listbox.bind('<FocusOut>', lambda e: self.listbox.selection_clear())

        self.cbutton_add = Button(bot_frame)
        self.cbutton_add.config(image=self.add_img,
                            bd=0, width="141",
                            height="41",
                            command=lambda: self.button_add())
        self.cbutton_add.pack(padx=(20,8), side=LEFT)

        self.cbutton_delete = Button(bot_frame)
        self.cbutton_delete.config(image=self.delete_img,
                            bd=0, width="141",
                            height="41",
                            command=lambda: self.button_delete())

        self.cbutton_delete.pack(padx=(8,8), side=LEFT)
        self.cbutton_open = Button(bot_frame)
        self.cbutton_open.config(image=self.open_img,
                            bd=0, width="141",
                            height="41",
                            command=lambda: self.button_open())
        self.cbutton_open.pack(padx=(8,8), side=LEFT)

        self.cbutton_close = Button(bot_frame)
        self.cbutton_close.config(image=self.close_img,
                            bd=0, width="141",
                            height="41",
                            command=lambda: self.button_close())
        self.cbutton_close.pack(padx=(8,8), side=LEFT)

        self.cbutton_close_all = Button(bot_frame)
        self.cbutton_close_all.config(image=self.close_all_img,
                            bd=0, width="141",
                            height="41",
                            command=lambda: self.button_close_all())
        self.cbutton_close_all.pack(padx=(8,20), side=LEFT)

        self.popup_menu.add_command(label="Pause", command=self.button_pause)
        self.popup_menu.add_command(label="Unpause", command=self.button_unpause)
        self.popup_menu.add_command(label="Refresh time", command=self.button_refresh_time)
        self.popup_menu.add_command(label="Open folder", command=self.button_open_folder)
        self.popup_menu.add_command(label="Delete", command=self.button_delete)
        self.popup_menu.add_command(label="Update list", command=self.refresh)
        threading.Thread(target=self.checkOnButtons).start()
        self.refresh()

    def set_appwindow(self, root):
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())

    def start_move(self, event):
        self.window.x = event.x
        self.window.y = event.y

    def stop_move(self, event):
        self.window.x = None
        self.window.y = None

    def on_motion(self, event):
        delta_x = event.x - self.window.x
        delta_y = event.y - self.window.y
        x = self.window.winfo_x() + delta_x
        y = self.window.winfo_y() + delta_y
        self.window.geometry("+%s+%s" % (x, y))

    def button_add(self):
        threading.Thread(target=self.invokeCreateMonitor).start()

    def button_delete(self):
        threading.Thread(target=self.invokeDeleteMonitor).start()

    def button_open(self):
        threading.Thread(target=self.invokeOpenMonitor).start()

    def button_close(self):
        threading.Thread(target=self.invokeCloseMonitor).start()

    def button_close_all(self):
        threading.Thread(target=self.invokeCloseAll).start()

    def button_pause(self):
        threading.Thread(target=self.pauseMonitor).start()

    def button_unpause(self):
        threading.Thread(target=self.unpauseMonitor).start()

    def button_refresh_time(self):
        threading.Thread(target=self.openWindowStopStime).start()

    def button_open_folder(self):
        threading.Thread(target=self.openFolder).start()

    def refresh(self):
        threading.Thread(target=self.update).start()

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()


    def unpauseMonitor(self, event=None):
        if event:
            item = self.listbox.identify('item', event.x, event.y)
            element = self.listbox.item(item)['values'][0]
        else:
            item = self.listbox.selection()
            element = self.listbox.item(item)['values'][0]
        unpauseMonitor(element, 5)
        self.update()

    def pauseMonitor(self, event=None):
        if event:
            item = self.listbox.identify('item', event.x, event.y)
            element = self.listbox.item(item)['values'][0]
        else:
            item = self.listbox.selection()
            element = self.listbox.item(item)['values'][0]
        self.original_value = getStopTimeValue(element)
        pauseAMonitor(element, getStopTimeValue(element))
        self.update()

    def openWindowStopStime(self, event=None):
        if event:
            item = self.listbox.identify('item', event.x, event.y)
            element = self.listbox.item(item)['values'][0]
        else:
            item = self.listbox.selection()
            element = self.listbox.item(item)['values'][0]
        self.strin = StringVar()
        self.top = Toplevel(self.window)
        self.top.geometry("350x75")
        self.top.resizable(width=False, height=False)
        Label(self.top, text=f"Set a time step value for project: {element}",font=("Helvetica", 8)).pack()
        self.original_value = getStopTimeValue(element)
        self.top.title("Stop Time")
        entry_top = Entry(self.top, textvariable = self.strin)
        entry_top.pack()
        self.strin.set(str(self.original_value))
        button_apply = Button(self.top, text="Apply", command=self.changeStopTime)
        button_destroy = Button(self.top, text="Cancel", command=self.top.destroy)
        button_destroy.pack(side=LEFT, anchor=W, fill=X, expand=YES)
        button_apply.pack(side=LEFT, anchor=W, fill=X, expand=YES)


    def changeStopTime(self, event=None):
        if event:
            item = self.listbox.identify('item', event.x, event.y)
            element = self.listbox.item(item)['values'][0]
        else:
            item = self.listbox.selection()
            element = self.listbox.item(item)['values'][0]
        if self.strin.get().isdigit():
            setStopTimeValue(element, self.strin.get(), self.original_value)
            self.original_value = self.strin.get()
        self.top.destroy()
        self.update()

    def invokeCloseAll(self):
        closeAllMonitors()
        self.update()

    def invokeCreateMonitor(self):
        createAMonitor()
        self.update()

    def invokeCloseMonitor(self, event=None):
        try:
            if event:
                item = self.listbox.identify('item', event.x, event.y)
                element = self.listbox.item(item)['values'][0]
            else:
                item = self.listbox.selection()
                element = self.listbox.item(item)['values'][0]
            killMonitorTask(element)
        except:
            for item in self.listbox.selection():
                element = self.listbox.item(item)['values'][0]
                killMonitorTask(element)
        self.update()

    def openFolder(self, event=None):
        if event:
            item = self.listbox.identify('item', event.x, event.y)
            element = self.listbox.item(item)['values'][0]
        else:
            item = self.listbox.selection()
            element = self.listbox.item(item)['values'][0]
        openMonitorFolder(element)
        self.update()

    def invokeOpenMonitor(self, event=None):
        try:
            if event:
                item = self.listbox.identify('item', event.x, event.y)
                element = self.listbox.item(item)['values'][0]
            else:
                item = self.listbox.selection()
                element = self.listbox.item(item)['values'][0]
            openAMonitor(element)
        except:
            for item in self.listbox.selection():
                element = self.listbox.item(item)['values'][0]
                openAMonitor(element)
        self.update()

    def invokeDeleteMonitor(self, event=None):
        try:
            if event:
                item = self.listbox.identify('item', event.x, event.y)
                element = self.listbox.item(item)['values'][0]
            else:
                item = self.listbox.selection()
                element = self.listbox.item(item)['values'][0]
            deleteMonitor(element)
        except:
            for item in self.listbox.selection():
                element = self.listbox.item(item)['values'][0]
                deleteMonitor(element)
        time.sleep(.1)
        self.update()

    def update(self):
        monitors = []
        for item in self.listbox.get_children():
            self.listbox.delete(item)
        running_projects = list_windows()
        self.count_active_projects = 0
        for file in os.listdir(CURR_DIR_PATH):
            if 'monitor-' in file:
                filename = file[file.find("-") + 1:]
                monitors.append(filename)
                if filename in running_projects:
                    self.listbox.insert('', 'end',image=self.running_picto, values=(filename, time.ctime(os.path.getctime(CURR_DIR_PATH+"/"+file))))
                    self.count_active_projects += 1
                else:
                    self.listbox.insert('', 'end',image=self.not_running_picto, values=(filename, time.ctime(os.path.getctime(CURR_DIR_PATH+"/"+file))))

        self.existing_monitors = monitors

    def checkRunningProjects(self):
        aux = [x for x in list_windows()]
        while True:
            time.sleep(.5)
            if aux != list_windows():
                self.update()
                aux = [x for x in list_windows()]

    def checkOnButtons(self):
        while True:
            if len(self.listbox.selection()) == 0:
                self.cbutton_open.config(state="disable")
                self.cbutton_close.config(state="disable")
            else:
                self.cbutton_open.config(state="normal")
                self.cbutton_close.config(state="normal")
            if self.count_active_projects == 0:
                self.cbutton_close_all.config(state="disable")
            else:
                self.cbutton_close_all.config(state="normal")
            time.sleep(.05)

def list_windows():
    '''Return a sorted list of visible windows.'''
    result = []
    @WNDENUMPROC
    def enum_proc(hWnd, lParam):
        if user32.IsWindowVisible(hWnd):
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            if title.value:
                try:
                    result.append(title.value[:title.value.rfind('-')])
                except:
                    pass
        return True
    user32.EnumWindows(enum_proc, 0)
    return result


def exit_window(e):
    os._exit(0)
