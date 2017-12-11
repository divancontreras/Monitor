import os
import shutil
from tkinter import filedialog
from tkinter import *
import time
from ClassMonitors import *
from pyfiglet import figlet_format

# Get current path


CURR_DIR_PATH = str(os.getcwd()).replace("\\", "/")

# Get clear function
clear = lambda: os.system('cls')

# Initialize the tuple for the multiple.
global monitors


def createAMonitor():
    filepath = getFilePath()
    if filepath is None:return  # Assert that the function returned a path
    filename = filepath.split("/")[-1]  # Erase everything before the last slash:  /ab/bc/tu.out > tu.out
    print(f"File \"{filename}\" selected")
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
                path = CURR_DIR_PATH + f"/monitor-{filename}"
                os.makedirs(path)
                return path
            else:
                path = CURR_DIR_PATH + f"/monitor-{filename}({copy})"
                os.makedirs(path)
                isCreating = False
                return path
        except:
            copy += 1


def configurePlotFiles(filename, current_monitor, filepath):
    target_folder_path = assertDirCreation(filename)
    for monitor in current_monitor.existingMonitors():
        with open(CURR_DIR_PATH + f"/in/{monitor}.plt", 'r') as file:
            infile = file.read()
            infile = infile.replace("{0}", filepath)
            infile = infile.replace("{1}", f"{filename} - {monitor}")
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
        with open(target_folder_path + "/" + f"{monitor}.plt", 'w') as outfile:
            outfile.write(infile)
    return target_folder_path

def closeMonitors(monitor):
    for window in monitor.existingGraphs():
        os.popen(f"taskkill /F /FI \"WindowTitle {monitor.name} - {window}\" /T")
    exit()

def deleteMonitor(monitor):
    shutil.rmtree()


def getMonitorsFromFiles(filename, filepath, current_monitor):
    for file in os.listdir(filepath):
        filename_complete = file[file.find(".") + 1:file.rfind(".")]
        if file.endswith(".out"):
            # Recognize if ".out" or ".res" file is from the same project
            if filename in file:
                print(filepath + "/" + file)
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
    monitors.append(current_monitor)
    return current_monitor


def getFilePath():
    root = Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(parent=root, initialdir=CURR_DIR_PATH, title='Please select a directory')
    if len(filepath) > 0:
        return filepath


# Just some utils
def assertValidInput():
    # Function to asset a valid numeric input
    try:
        userinput = int(input("Select an option:"))
        return userinput
    except:
        print("Only use numeric inputs")
        time.sleep(.5)


def summonFreshLogo():
    print(figlet_format('KRIPSY', font='starwars'))


# The main function

def main():
    global monitors
    monitors = []
    window = Tk()
    window.geometry()
    window.title("Program Monitors")
    listbox = Listbox(window)
    listbox.pack()

    listbox.insert(END, "a list entry")

    for item in ["one", "two", "three", "four"]:
        listbox.insert(END, item)

    window.mainloop()


def program():
    while True:
        clear()
        summonFreshLogo()
        print("""
         1.- Create a new monitor
         2.- Close a monitor
         9.- Exit program (Closes all monitors)
         """)
        userinput = assertValidInput();
        if userinput == 1:
            createAMonitor()
        elif userinput == 2:
            clear()
            summonFreshLogo()
            counter = 0
            for monitor in monitors:
                print("Any non-numerical to 'Cancel'")
                print(f"{counter}.- {monitor.name}")
                counter += 1
                monitornumber = assertValidInput()
                closeMonitors(monitors[monitornumber])

        elif userinput == 9:
            exit()
            for monitor in monitors:
                closeMonitors(monitor)

if __name__ == "__main__":
    main()
