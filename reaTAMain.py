import time
from UIMonitorClass import *
from monitorClass import *
from tkinter import *
from pyfiglet import figlet_format
import shutil
import subprocess
import os
from tkinter import filedialog
# Get current path

CURR_DIR_PATH = str(os.getcwd()).replace("\\", "/")

# Get clear function
clear = lambda: os.system('cls')

# Initialize the tuple for the multiple.
global UIAPP


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
        os.popen(f"start {files_location}/{file}")


def assertDirCreation(filename, copy=0):
    while True:
        try:
            if copy == 0:
                name = filename
                os.makedirs(CURR_DIR_PATH+"/monitor-"+name)
                return name
            else:
                name = f"{filename}({copy})"
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
    for monitor_type in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        monitor_type = monitor_type[:monitor_type.find(".")]
        try:
            os.popen(f"taskkill /F /FI \"WindowTitle eq {monitor_name}-{monitor_type}\"")
        except:
            pass
def deleteFolderByName(monitor_name):
    shutil.rmtree(f"{CURR_DIR_PATH}/monitor-{monitor_name}")

def deleteMonitor(monitor_name, folderExists=True):
    while folderExists:
        killMonitorTask(monitor_name)
        time.sleep(.1)
        try:
            deleteFolderByName(monitor_name)
            folderExists=False
        except:
            pass
def hideAllMonitors():
    os.popen(f"taskkill /F /IM wgnuplot.exe")


def showAMonitor(monitor_name):
    for file in os.listdir(f"{CURR_DIR_PATH}/monitor-{monitor_name}"):
        os.popen(f"start {CURR_DIR_PATH}/monitor-{monitor_name}/{file}")

def hideAMonitor(monitor_name):
    killMonitorTask(monitor_name)

def getMonitorsFromFiles(filename, filepath, current_monitor):
    for file in os.listdir(filepath):
        filename_complete = file[file.find(".") + 1:file.rfind(".")]
        if file.endswith(".out"):
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
                if filename in file:
                    current_monitor.setResiduals(file, filename_complete)
    return current_monitor

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
