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

    def name(self):
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

    def existingMonitors(self):
        self.existing = []
        if self.continuosMonitor != "plot":
            self.existing.append("continuosMonitor")
        if self.PressureMonitor != "plot":
            self.existing.append("PressureMonitor")
        if self.residuals != "plot":
            self.existing.append("residuals")
        if self.TemperatureMonitor != "plot":
            self.existing.append("TemperatureMonitor")
        if self.VelocityMonitor != "plot":
            self.existing.append("VelocityMonitor")
        return self.existing

