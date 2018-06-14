import os
from cx_Freeze import setup, Executable

base = None

os.environ['TK_LIBRARY'] = r"C:\Users\sesa467855\AppData\Local\Programs\Python\Python36\tcl\tk8.6"
os.environ['TCL_LIBRARY'] = r"C:\Users\sesa467855\AppData\Local\Programs\Python\Python36\tcl\tcl8.6"

executables = [Executable("Monitors.py", base="Win32GUI", icon="resources\monitor_icon.ico")]
includefiles = ['in','monitorClass.py',"Monitors.py", 'UIMonitorClass.py', 'resources']

packages = ["tkinter", "time", "shutil", "os", "tkinter.filedialog", "threading", "datetime", "ctypes"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files': includefiles,
    },

}

setup(
    name = "Monitors",
    options = options,
    version = "1.0",
    description = 'Python program with UI that plots simulation outputs on real time, to observe converging values overtime.',
    executables = executables,
)