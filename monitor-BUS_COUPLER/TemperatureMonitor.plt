reset; clear
#set encoding iso_8889_1#
# WSVGA Standard resolution:
set term wxt noraise noenhanced

cd "F:/Desktop/Python/aladdin"

set format y "% g"
set datafile missing '{{}}'
set grid
set format "% h"
set term wxt title "BUS_COUPLER-TemperatureMonitor"
set title "Project: BUS_COUPLER-TemperatureMonitor"
set key box outside

# --- TEMPERATURE ---- Monitors

unset logscale y
set yl "Temperature [°C]"
set xl "Iteration"
plot 'BUS_COUPLER.6.CORE_PCB.out' u 1:($2-273.15) w lp t '6.CORE_PCB', 'BUS_COUPLER.7.COMM_PCB.out' u 1:($2-273.15) w lp t '7.COMM_PCB',

pause 10
reread