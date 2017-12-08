@ECHO OFF 
if exist TemperatureMonitor.plt (
    del TemperatureMonitor.plt
)
if exist PressureMonitor.plt (
    del PressureMonitor.plt
)
if exist VelocityMonitor.plt (
    del VelocityMonitor.plt
)
if exist residuals.plt (
    del residuals.plt
)

cd dist
main.exe

echo Press any key to open Monitor files generated. . . 
pause >nul
cd..
if exist residuals.plt (
    start residuals.plt
)
if exist TemperatureMonitor.plt (
    start TemperatureMonitor.plt
)
if exist PressureMonitor.plt (
    start PressureMonitor.plt
)
if exist VelocityMonitor.plt (
    start VelocityMonitor.plt
)

