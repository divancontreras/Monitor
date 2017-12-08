import os
import shutil
import tkinter
from tkinter import filedialog
from monitorClass.py import *
from pyfiglet import figlet_format

# Get current path
CURR_DIR_PATH = os.getcwd()

# Get clear function
clear = lambda: os.system('cls')

# Initialize the tupple for the multiple.
global monitor

def createAMonitor():
    filepath = getFilePath()
    # Erase everything before the last slash:  /ab/bc/tu.out > tu.out
    filename = filepath.split("/")[-1]
    print(f"Project {filename} selected")
    filename = filename[:filename.find(".")]
    current_monitor = Monitor(filename)
    filepath = os.path.dirname(filepath)
    current_monitor = getGraphsFromFiles(filename, filepath, current_monitor)
    deployMonitor(filename, current_monitor)

def makeMonitorFolders(filename):
    print(CURR_DIR_PATH)
    input()
    os.makedirs(CURR_DIR_PATH+f"/monitor-{filename}")
    shutil.copyfile(CURR_DIR_PATH+"/in/VelocityMonitor.plt", CURR_DIR_PATH+f"/monitor-{filename}")
    shutil.copyfile(CURR_DIR_PATH+"/in/TemperatureMonitor.plt", CURR_DIR_PATH+f"/monitor-{filename}")
    shutil.copyfile(CURR_DIR_PATH+"/in/residuals.plt", CURR_DIR_PATH+f"/monitor-{filename}")
    shutil.copyfile(CURR_DIR_PATH+"/in/PressureMonitor.plt", CURR_DIR_PATH+f"/monitor-{filename}")
    shutil.copyfile(CURR_DIR_PATH+"/in/continuosMonitor.plt", CURR_DIR_PATH+f"/monitor-{filename}")
    return CURR_DIR_PATH+f"/monitor-{filename}"

def deployMonitor(filename, current_monitor):
    target_folder_path = makeMonitorFolders(filename)
    for file in target_folder_path:
        for window in monitor.existingGraphs():
            exit()


def closeMonitor(monitor):
    for window in monitor.existingGraphs():
        os.popen(f"taskkill /F /FI \"WindowTitle {monitor.name} - {window}\" /T")


def getGraphsFromFiles(filename, filepath, current_monitor):
    for file in os.listdir(filepath):
        if file.endswith(".out"):
            # Recognize if ".out" or ".res" file is from the same project
            if filename in file:
                print(filepath+"/"+filename)
                if 'Temperature' in open(filepath,'r'):
                    current_monitor.setTemperatureMonitor(file, filename)
                elif 'Pressure' in open(filepath,'r'):
                    current_monitor.setPressureMonitor(file, filename)
                elif 'Velocity' in open(filepath,'r'):
                    current_monitor.setVelocityMonitor(file, filename)
            elif file.endswith(".res"):
                if filename in file:
                    current_monitor.setResiduals(file, filename)
    monitors.append(current_monitor)
    return current_monitor


def getFilePath():
    root = tkinter.Tk()
    root.withdraw() 
    filepath = filedialog.askopenfilename(parent=root, initialdir=CURR_DIR_PATH, title='Please select a directory')
    if len(filepath) > 0:
        return filepath
    else:
        print("No project selected")
        exit()


def summonFreshLogo():
    print(figlet_format('KRIPSY', font='starwars'))


def main():
    monitor = []
    while True:
        # clear()
        summonFreshLogo()
        print("1.- Create a new monitor")
        print("2.- Close a monitor")
        print("9.- Exit program (Closes all monitors)")
        userinput = int(input("Select an option:"))
        if userinput == 1:
            createAMonitor()
        elif userinput == 2:
            # clear()
            summonFreshLogo()
            counter = 0
            for monitor in monitors:
                print(f"{counter}.- {monitor.name}")
                counter += 1
            monitornumber = input("Select the monitor to close. (Non-numerical input to cancel)")
            try:
                closeMonitor(monitors[int(monitornumber)])
            except:
                print("Error on input")

        elif userinput == 5:
            for monitor in monitors:
                closeMonitor(monitor)



if __name__ == "__main__":
    main()
