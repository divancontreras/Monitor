reset; clear
#set encoding iso_8889_1#
# WSVGA Standard resolution:
set term wxt noraise noenhanced

cd "{0}"

set format y "% g"
set logscale y
set yl "Residuals"
set xl "Iteration"
set datafile missing '{{}}'
set grid
set term wxt title "{1}"
set title "Project: {1}"
set key box outside
 plot "{1}.res" u 1:3 t "continuity" w lp,'' u 1:5 t 'x-velocity' w lp,'' u 1:7 t 'y-velocity' w lp,\
'' u 1:9 t 'z-velocity' w lp,'' u 1:11 t 'energy' w lp,'' u 1:3 t 'k' w lp,'' u 1:5 t 'ω or ε' w lp 

pause 10
reread




