

.. _quick_surge:

*****************************************************************
Quick start guide for storm surge modeling
*****************************************************************

See also this `youtube video <https://www.youtube.com/watch?v=YurKRmYgGfk&t=10s>`__
and the related materials from the `2020 GeoClaw Developers Workshop
<http://www.clawpack.org/geoclawdev-2020/>`__.

To get started with a storm surge computation it is best to refer to a previous
working example.  For example, you might start with 
`$CLAW/geoclaw/examples/storm-surge/ike`.  There are also a number of additional 
examples in the `$CLAW/geoclaw/examples/storm-surge` directory as well as some
in the `$CLAW/apps/surge-examples` directory (this is actually a repository of 
examples that is actively updated).  The primary input that one needs to provide
for a new example usually involves two data source

 - Topography data:  Data that specifies the topography and bathymetry of the
   region around the area of interest.  For storm surge computations it is 
   generally good practice to include entire oceanic basins so that you can
   ensure that flow into and out of the basin is resolved by the computation
   and is sufficiently distant from the computational domain's boundaries.
 - Storm data:  Of course we need to specify the particular storm that you
   are interested in.  There are a number of ways to specify a storm which
   are described in :ref:`setrun_surge`.  Sources for parameterized storms
   can also be found in :ref:`surgedata` and a description of how to include
   them in :ref:`_surge_module`.

Here we will concentrate on changing the Hurricane Ike (2018) example into one for
Hurricane Elsa (2021).

1. First copy the files (setrun.py, setplot.py, makefile) located in the Hurricane Ike directorty located at
   `$CLAW/geoclaw/examples/storm-surge/ike</cite>`. Note: if reader has not yet set up environment 
   variable `CLAW`, please refer to this page: `Setting Environment Variable <http://www.clawpack.org/setenv.html>`__.

2. Next let’s find some better topography for the west coast Florida area. There are several places where we can get topography/bathymetry data, for
   example `Global Multi-Resolution Topography Data Synthesis <https://www.gmrt.org/index.php>`__, 
   `Global Digital Elevation Model <https://www.jspacesystems.or.jp/ersdac/GDEM/E/1.html>`__,
   `National Center for Environmental Information <https://www.ngdc.noaa.gov/mgg/bathymetry/relief.html>`__,
   and `The General Bathymetry Chart of the Oceans <https://www.gebco.net/data_and_products/gridded_bathymetry_data/>`__.
   Here we will use the data from the last one which is the GEBCO to retrive and download the topography and bathymetry data for hurricane Elsa. Theoretically, we 
   can select the region as big as possible. However, the bigger the region, the more time it will take for GeoClaw simulation to run. So for hurricane Elsa,
   we only use the gulf of Mexico region so that it can include the region days before Elsa's landfall and the region days after the landfall. (How to specify how many 
   days before and after will be discussed in later steps below.) After downloading the grid format of the topography data, we may want to store it on cloud like google drive, 
   dropbox, or your personal website so that people in the future can have access to this topography data file. 

3. Now let’s find a storm specification for Hurricane Elsa. Several data resouces are available: `Automated Tropical Cyclone Forecasting System <https://ftp.nhc.noaa.gov/atcf/archive/>`__,
   `Atlantic Oceanographic and Meteorological Laboratory <https://www.aoml.noaa.gov/hrd/hurdat/Data_Storm.html>`__,
   `NOAA Rapid Update Cycle <https://ruc.noaa.gov/tracks/>`__,
   `National Center for Environmental Information <http://www.ncdc.noaa.gov/ibtracs/>`__,
   `Naval Meteorology and Oceanography Command <https://www.metoc.navy.mil/jtwc/jtwc.html?best-tracks>`__,
   `Coastal Hazards System <https://chs.erdc.dren.mil>`__.
   In this example we will use the ATCF database. For Hurricane Elsa, this ends up being
   the file located `here <http://ftp.nhc.noaa.gov/atcf/archive/2021/bal052021.dat.gz>`__.
   How to find a storm specific data using ATCF database for your storm? Go to `ATCF Archive <http://ftp.nhc.noaa.gov/atcf/archive/>`__. Then 
   search for you storm number. In this example, storm number for Hurricane Elsa is `AL052021`. Therefore, the storm data corresponds to Hurricane Elsa will simply 
   be `bal052021.dat` in year 2021.

4. Now we have our topography data and storm specific data ready. Next, we need to modify the `setrun.py` to use 
   our new storm specific data and topography data we just added. First, modify the 
   computational domain so that it matches or is contained in the region of the topography data. 
   Then change :code:`t0`, :code:`tfinal`, and :code:`time_offset`
   to Elsa's landfall time and time period before and after landfall we want to simulate. 
   Last but not least, change locations of retrieving topography and storm data file in topography data and 
   surge data sections.

5. We also need to modify the plotting in `setplot.py`. 
   First, we may want to change upper and lower limits for surface levels, wind speeds,
   pressure, and friction to best represent our storm. For example, Elsa is a category 1 hurricane which is 
   not very strong. Therefore, we changed the surface levels to :code:`[-1, 1]` so that 
   visualization from plots will be more evident. In the plot specifications section, we can add
   zoom-in regions. For Elsa, three more regions other than the computational domain are added. We may 
   also alter the legends, labels, colors of plots, and so on.

6. Gauges are key for validation study. We want to know how good GeoClaw's simulation is
   comparing to observed currents and tides data. Gauge information and location 
   can be found here at `NOAA Tides & Currents <https://tidesandcurrents.noaa.gov>`__.
   In `setrun.py`, add gauge locations using the :code:`rundata.gaugedata.gauges.append()` method.
   Accordingly in `setplot.py`, modify parameters of the :code:`geoclaw.util.fetch_noaa_tide_data()` method
   so that observed data from gauges will be fetched and plotted along with simulation.

7. Sometimes, plots will not look correct even though we inputed the exactly precise locations of gauges. One highly possible reason for that 
   is our region is not resolved enough. Consequently, GeoClaw might recognize topography of locations wrongly. To solve this problem, we will
   use the `AMRClaw <https://www.clawpack.org/amr_algorithm.html#amr-algorithm>`__ algorithm to further
   refine regions. For this example, Tampa Bay area was not recognized by GeoClaw until 6 levels of refinement was implemented.

8. Finally we are ready to run the simulation. Make sure all files (setrun.py, setplot.py, makefile) are in the correct directory, 
   then :code:`$ cd DirectoryPath` to the working directory. In that working directory, we can either use :code:`$ make all` or :code:`$ make .plots`
   to execute. If errors are encountered, we can follow the sequence of :code:`$ make .exe`, :code:`$ make .data`, :code:`$ make .output`, and
   :code:`$ make .plots` to debug. To eliminate all executable files and restart, we can use :code:`$ make clean`.
   Once the simulation runs successfully, we can see the result at :code:`DirectoryPath/_plots/_PlotIndex.html`. 

For a more detailed, step-by-step guide to storm surge simulations/validations, please find the jupyter 
notebook `setup.ipynb` at this `github repository <https://github.com/mandli/apps>`__.