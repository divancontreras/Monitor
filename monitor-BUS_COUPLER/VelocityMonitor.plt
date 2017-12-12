reset; clear
#set encoding iso_8889_1#
# WSVGA Standard resolution:
set term wxt noraise noenhanced

cd "F:/Desktop/Python/aladdin"

set format y "% g"
set datafile missing '{{}}'
set grid
set format "% h"
set term wxt title "BUS_COUPLER-VelocityMonitor"
set title "Project: BUS_COUPLER-VelocityMonitor"
set key box outside

# --- VELOCITY ---- Monitors

unset logscale y
set yl "Velocity [m/s]"
set xl "Iteration"
plot 'BUS_COUPLER.10.grille.1.out' u 1:2 w lp t '10.grille.1', 'BUS_COUPLER.11.grille.12.out' u 1:2 w lp t '11.grille.12', 'BUS_COUPLER.12.grille.2.out' u 1:2 w lp t '12.grille.2', 'BUS_COUPLER.13.grille.3.out' u 1:2 w lp t '13.grille.3', 'BUS_COUPLER.14.grille.4.out' u 1:2 w lp t '14.grille.4', 'BUS_COUPLER.15.grille.5.out' u 1:2 w lp t '15.grille.5', 'BUS_COUPLER.16.grille.6.out' u 1:2 w lp t '16.grille.6', 'BUS_COUPLER.17.grille.7.out' u 1:2 w lp t '17.grille.7', 'BUS_COUPLER.18.grille.8.out' u 1:2 w lp t '18.grille.8', 'BUS_COUPLER.19.grille.9.out' u 1:2 w lp t '19.grille.9', 'BUS_COUPLER.20.grille.10.out' u 1:2 w lp t '20.grille.10', 'BUS_COUPLER.21.grille.11.out' u 1:2 w lp t '21.grille.11',

pause 10
reread