reset; clear
#set encoding iso_8889_1#
# WSVGA Standard resolution:
set term wxt noraise noenhanced

cd "{0}"

set format y "% g"
set datafile missing '{{}}'
set grid
set format "% h"
set term wxt title "{1}"
set title "Project: {1}"
set key box outside

# --- VELOCITY ---- Monitors

unset logscale y
set yl "Velocity [m/s]"
set xl "Iteration"
{2}

pause 10
reread