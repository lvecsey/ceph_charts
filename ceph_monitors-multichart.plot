
set terminal png size 1920,1080

set output ARG2

set xdata time

set timefmt "%s"

start_ts=ARG3

num_days=ARG4

set format x "%m/%d\n%H:%M"

set xlabel "Date"

set title "Ceph Monitors response time"

set multiplot layout 2, 1

zoomfactor_ping=1.0
zoomfactor_prot=1.0

conv_seconds2ms=1000

set title "Ceph Monitors (Ping response)"

unset xtics
unset xlabel

set xrange [(start_ts - 86400*num_days) : (start_ts + 300)]
set yrange [-0.5:2.0]

plot ARG1 using 1:($2 * conv_seconds2ms * zoomfactor_ping) w l lc rgb "#FF6666" title "mon.mon1 Ping (ms)" \
 ,'' using 1:($3 * conv_seconds2ms * zoomfactor_ping) w l lc rgb "#66FF66" title "mon.mon2 Ping (ms)" \
 ,'' using 1:($4 * conv_seconds2ms * zoomfactor_ping) w l lc rgb "#6666FF" title "mon.mon3 Ping (ms)"

set title "Ceph Monitors (v2 Protocol response)"

set xtics
set xlabel "Date"

set yrange [0.5:3.0]

plot ARG1 using 1:($5 * conv_seconds2ms * zoomfactor_prot) w l lc rgb "#AA3333" title "mon.mon1 v2 Protocol (ms)" \
 ,'' using 1:($6 * conv_seconds2ms * zoomfactor_prot) w l lc rgb "#33AA33" title "mon.mon2 v2 Protocol (ms)" \
 ,'' using 1:($7 * conv_seconds2ms * zoomfactor_prot) w l lc rgb "#3333AA" title "mon.mon3 v2 Protocol (ms)"

# Exit multiplot mode
unset multiplot

