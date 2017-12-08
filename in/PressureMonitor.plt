reset; clear
#set encoding iso_8889_1#
# WSVGA Standard resolution:
set term wxt noraise noenhanced

cd "{0}"

set format y "% g"
set datafile missing '{{}}'
set grid
set format "% h"
set title "Project: {1}"
set key box outside

# --- PRESSURE ---- Monitors

unset logscale y
set yl "Pressure [Pa]"
set xl "Iteration"
{2}

pause 10
reread