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

# --- TEMPERATURE ---- Monitors

unset logscale y
set yl "Temperature [°C]"
set xl "Iteration"
set key box outside

{2}

pause 10
reread