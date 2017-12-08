class Monitor:
    def __init__(self, name):
        self.name = name
        self.continuosMonitor = "plot"
        self.PressureMonitor = "plot"
        self.residuals = "plot"
        self.TemperatureMonitor = "plot"
        self.VelocityMonitor = "plot"
        self.existing = []

    #getters and setters of the class.

    def name():
        return self.name

    def setContinuosMonitor(self, file, filename):
        self.continuosMonitor += f" '{file}' u 1:2 w lp t '{filename}',"

    def getContinuosMonitor(self):
        return self.continuosMonitor

    def setPressureMonitor(self, file, filename):
        self.PressureMonitor += f" '{file}' u 1:2 w lp t '{filename}',"

    def getPressureMonitor(self):
        return self.PressureMonitor

    def setResiduals(self, file, filename):
        self.residuals += f" '{file}' u 1:2 w lp t '{filename}',"

    def getResiduals(self):
        return self.residuals

    def setTemperatureMonitor(self, file, filename):
        self.TemperatureMonitor += f" '{file}' u 1:($2-273.15) w lp t '{filename}',"

    def getTemperatureMonitor(self):
        return self.TemperatureMonitor

    def setVelocityMonitor(self, file, filename):
        self.VelocityMonitor += f" '{file}' u 1:2 w lp t '{filename}',"

    def getVelocityMonitor(self):
        return self.VelocityMonitor

    def existingGraphs():
        self.exisitng = []
        if  self.continuosMonitor != "plot":
            self.existing("continuosMonitor")
        if self.PressureMonitor != "plot":
            self.exisitng("PressureMonitor")
        if self.residuals != "plot":
            self.exisitng("residuals")
        if self.TemperatureMonitor != "plot":
            self.exisitng("TemperatureMonitor")
        if self.VelocityMonitor != "plot":
            self.exisitng("VelocityMonitor")
            return self.exisitng

