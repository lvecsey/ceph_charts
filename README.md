
*Overview*

A python program which can check the health of your Ceph monitor servers.

I use the default (recommended) 3 ceph monitors in my storage cluster, so the generated graphs have 3 individual *ping responses*, as host level checks. In addition a lower level (TCP) ceph monitor check is made to check that the individual *monitor services* are listening for requests.

Use together with 'ceph status', 'ceph health detail', and 'ceph mon stat' to better understand your storage cluster availability.

*Python Virtual Environment*

Based on the /usr/share/doc/python3.13/README.venv file:

```console
mkdir -p ~/.venvs/ceph_charts
python3 -m venv ~/.venvs/ceph_charts
~/.venvs/ceph_charts/bin/python -m pip install pyyaml icmplib
```

*Configuring*

Copy the template yml file, and edit to define the monitor hosts. Collected data is also specified with the *data_fn* parameter.

```console
mkdir -p ~/.config/ceph_charts
cp ceph_charts-template.yml ~/.config/ceph_charts/ceph_charts.yml
```

*Usage*

The provided *ceph_charts.py* contains all the data collection routines.

```console
source ~/.venvs/ceph_charts/bin/activate
python ceph_charts.py mon_response
```

*Installing*

```console
mkdir -p ~/bin
cp ceph_charts.py ~/bin
```

*Scheduling*

Use the following line, or similar as a crontab entry:

```crontab
*/2 * * * *  ~/.venvs/ceph_charts/bin/python ~/bin/ceph_charts.py mon_response > /dev/null
```

The recorded values include the timestamp of when they were taken, and the measured results are stored in units of seconds.

*Plotting*

To generate a single PNG image, the current time is used along with the number of days of recent history to plot.

```console
data_fn=~/.cache/ceph_charts/ceph_charts.dat
gnuplot -c 'ceph_monitors-multichart.plot' "$data_fn" output.png `date +%s` 5
```

To generate a variety of plot images, use the *regen_plots.sh* script.

```console
./regen_plots.sh
```

You can edit the script file to list the time periods you are interested in, such as 3 day, 7 day, etc.

*Viewing*

Select one of the generated PNG images, for viewing.

```console
feh --borderless ./ceph_monitors-multichart-1d.png
```

*Revising the plot*

As you collect more data, you can adjust each of the *yrange* settings in the multichart plot file to better reflect your environment. 

It shows the millisecond range of values that you are seeing, or expect to see. If you omit this setting, gnuplot will autofit the data. However if you have a better sense of your network environment, such as your network speed and whether your system is local or remote, you can tune this parameter to have a better view of the data.

*Links*
[GNUPlot](https://www.gnuplot.info/)

