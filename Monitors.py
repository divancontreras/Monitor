import time
from UIMonitorClass import *
from monitorClass import *
from tkinter import *
import shutil
import os
from tkinter import filedialog

import ctypes
from ctypes import wintypes


user32 = ctypes.WinDLL('user32', use_last_error=True)

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,    # _In_ hWnd
    wintypes.LPARAM,) # _In_ lParam

# Get current path

CURR_DIR_PATH = str(os.getcwd()).replace("\\", "/")


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
                    result.append(title.value)
                except:
                    pass
        return True
    user32.EnumWindows(enum_proc, 0)
    return result

def createAMonitor():
    filepath = getFilePath()
    if filepath is None:return  # Assert that the function returned a path
    filename = filepath.split("/")[-1]  # Erase everything before the last slash:  /ab/bc/tu.out > tu.out
    filename = filename[:filename.find(".")]
    current_monitor = Monitor(filename)
    filepath = os.path.dirname(filepath)
    current_monitor = getMonitorsFromFiles(filename, filepath, current_monitor)
    files_location = configurePlotFiles(filename, current_monitor, filepath)
    deployMonitor(files_location)

def deployMonitor(files_location):
    for file in os.listdir(files_location):
        os.popen(f"{files_location}/{file}")


def assertDirCreation(filename, copy=0):
    while True:
        try:
            if copy == 0:
                name = filename
                os.makedirs(CURR_DIR_PATH+"/monitor-"+name)
                return name
            else:
                name = f"{filename}-{copy}"
                os.makedirs(CURR_DIR_PATH+"/monitor-"+name)
                return name
        except:
            copy += 1

def configurePlotFiles(filename, current_monitor, filepath):
    foldername = assertDirCreation(filename)
    for monitor in current_monitor.existingMonitors():
        with open(CURR_DIR_PATH + f"/in/{monitor}.plt", 'r') as file:
            infile = file.read()
            infile = infile.replace("{0}", filepath)
            infile = infile.replace("{1}", f"{foldername}-{monitor}")
            if monitor == "PressureMonitor":
                infile = infile.replace("{2}", current_monitor.getPressureMonitor())
            elif monitor == "continuosMonitor":
                infile = infile.replace("{2}", current_monitor.getContinuosMonitor())
            elif monitor == "residuals":
                infile = infile.replace("{2}", current_monitor.getResiduals())
            elif monitor == "TemperatureMonitor":
                infile = infile.replace("{2}", current_monitor.getTemperatureMonitor())
            elif monitor == "VelocityMonitor":
                infile = infile.replace("{2}", current_monitor.getVelocityMonitor())
        with open(f"{CURR_DIR_PATH}/monitor-{foldername}/{monitor}.plt", 'w') as outfile:
            outfile.write(infile)
    return f"{CURR_DIR_PATH}/monitor-{foldername}"

def killMonitorTask(monitor_name):
        for task in list_windows():
            if task[:task.rfind('-')] == monitor_name:
                try:
                    os.popen(f"taskkill /F /FI \"WindowTitle eq {task}\"")
                except:
                    pass

def deleteFolderByName(monitor_name):
    shutil.rmtree(f"{CURR_DIR_PATH}/monitor-{monitor_name}")

def deleteMonitor(monitor_name):
    killMonitorTask(monitor_name)
    while True:
        time.sleep(.1)
        if not os.path.exists("{CURR_DIR_PATH}/monitor-{monitor_name}"):
            try:
                deleteFolderByName(monitor_name)
                return
            except:
                pass

def closeAllMonitors():
    os.popen(f"taskkill /F /IM wgnuplot.exe")

def openMonitorFolder(monitor_name):
    if(len(monitor_name) > 0):
        for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
            with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'r') as doc:
                doc = str(doc.read()).split("\"")[1]
                doc = doc.replace("/", "\\")
                os.system(f"start \"\" \"{doc}\"")
                return

def openAMonitor(monitor_name):
    for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        os.popen(f"{CURR_DIR_PATH}/monitor-{monitor_name}/{file}")



def closeAMonitor(monitor_name):
    killMonitorTask(monitor_name)

def getMonitorsFromFiles(filename, filepath, current_monitor):
    current_monitor.setOriginalPath(filepath)
    for file in os.listdir(filepath):
        if file.endswith(".out"):
            filename_complete = file[file.find(".") + 1:file.rfind(".")]
            # Recognize if ".out" or ".res" file is from the same project
            if filename in file:
                current_file = open(filepath + "/" + file, 'r').read()
                if 'Temperature' in current_file:
                    current_monitor.setTemperatureMonitor(file, filename_complete)
                elif 'Pressure' in current_file:
                    current_monitor.setPressureMonitor(file, filename_complete)
                elif 'Velocity' in current_file:
                    current_monitor.setVelocityMonitor(file, filename_complete)
        elif file.endswith(".res"):
            filename_complete = file[:file.rfind(".")]
            if filename in file:
                current_monitor.setResiduals(filename_complete)
    return current_monitor

def getStopTimeValue(monitor_name):
    for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'r') as doc:
            data = doc.readlines()
            for line in data:
                if "pause" in line:
                    word = line.split(" ")[1]
                    return word

def pauseAMonitor(monitor_name, stop_value):
    closeAMonitor(monitor_name)
    for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'r') as indoc:
            data = indoc.read()
        if "pause -1" not in data:
            with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'w') as doc:
                data = data.replace(f"pause {stop_value}", "pause -1" + "\n" + "reread")
                doc.write(data)
        else:
            return
    openAMonitor(monitor_name)


def unpauseMonitor(monitor_name, stop_value):
    closeAMonitor(monitor_name)
    for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'r') as indoc:
            data = indoc.read()
        with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'w') as outdoc:
            data = data.replace(data[data.find("pause -1"):],f"pause {stop_value}" + "\n" + "reread")
            outdoc.write(data)
    openAMonitor(monitor_name)

def setStopTimeValue(monitor_name, new_value, current_value):
    closeAMonitor(monitor_name)
    new_value = int(new_value)
    current_value = int(current_value)
    for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'r') as indoc:
            data = indoc.read()
        with open(CURR_DIR_PATH + f"/monitor-{monitor_name}/{file}", 'w') as outdoc:
            data = data.replace(f"pause {current_value}", f"pause {new_value}")
            outdoc.write(data)
    openAMonitor(monitor_name)


def getFilePath():
    root = Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(parent=root, initialdir=CURR_DIR_PATH, title='Please select a directory')
    if len(filepath) > 0:
        return filepath

def main():
    global UIAPP
    global monitors
    UIAPP = UIApp()


if __name__ == "__main__":
    main()
