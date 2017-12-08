reset; clear
#set encoding iso_8889_1#
# WSVGA Standard resolution:
set term wxt noraise noenhanced size 1024,600

cd "{0}"

{2}
set format y "% g"
set logscale y
set yl "Residuals"
set xl "Iteration"
set datafile missing '{{}}'
set grid
plot "{1}.res" u 1:3 t "continuity" w l,'' u 1:5 t 'x-velocity' w l, '' u 1:7 t 'y-velocity' w l,\
'' u 1:9 t 'z-velocity' w l, '' u 1:11 t 'energy' w l,'' u 1:3 t 'k' w l, '' u 1:5 t 'ω or ε' w l

set format "% h"
# TEMPERATURE Monitors
unset logscale y
set yl "Temperature [°C]"
set xl "Iteration"
{3}
# PRESSURE Monitors
unset logscale y
set yl "Pressure [Pa]"
set xl "Iteration"
{4}
# VELOCITY Monitors
unset logscale y
set yl "Velocity [m/s]"
set xl "Iteration"
{5}

unset multiplot
pause 10
reread
