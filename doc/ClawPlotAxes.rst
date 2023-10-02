
.. _ClawPlotAxes:

**************************************
ClawPlotAxes 
**************************************


For usage see :ref:`setplot` and :ref:`plotexamples`.

Objects of this class are usually created by the new_plotaxes method of a
:ref:`ClawPlotFigure` object.

.. seealso:: :ref:`setplot` and :ref:`plotexamples`

.. class:: ClawPlotAxes


Attributes
==========

  The following attributes can be set by the user:

  .. attribute:: name : str

  .. attribute:: axescmd : str

  The command to be used to create this axes, for example:
    *  "subplot(1,1,1)" for a single axes filling the figure
    *  "subplot(2,1,1)" for the top half
    *  "axes([0.1, 0.1, 0.2, 0.8])" for a tall skinny axis.

  See the matplotlib documentation for axes.

  .. attribute:: show : bool

     If False, suppress showing this axes and all items on it.

  .. attribute:: title : str

     The title to appear at the top of the axis.  Defaults to string
     specified by the *name* attribute.

     **New in v5.9.1:** 

     Note that the title can now include the string `h:m:s` or `d:h:m:s`
     as described further below for the case `title_with_t == True`.

  .. attribute:: title_fontsize : float

     Fontsize for title

  .. attribute:: title_kwargs : str

     Any other kwargs to be passed to plt.title(), e.g. `'color'`

  .. attribute:: title_with_t : bool

     If True, creates a title using a default format like::

          `"%s at time t = %14.8e" % (title, t)`

     And rather than `%14.8e` for `t`, the default format uses `%14.8f`
     if `0.001 <= t <= 1000`.

     A different format can be specified with the `title_t_format` attribute.

     **New in v5.9.1:** 

     If the `title` attribute contains the string
     `d:h:m:s` then the time is formatted as days:hours:minutes:seconds.

     Otherwise, if the `title` attribute contains the string
     `h:m:s` then the time is formatted as hours:minutes:seconds.

     For example, you could specify::

        plotaxes.title_with_t = True
        plotaxes.title = 'Surface elevation at time h:m:s after earthquake'

  .. attribute:: title_t_format : str

     A format string used to format `t` in the title.  If this is not
     `None`, then this is used instead of the conventions mentioned above.

     Internally it formats using::

        t_str = plotaxes.title_t_format % t
        title_str = "%s at time t = %s"  % (plotaxes.title,t_str)
        plt.title(title_str, **plotaxes.title_kwargs)

  .. attribute:: xlimits : array [xmin, xmax]  or 'auto'

     The x-axis limits if an array with two elements, or choose
     automatically

  .. attribute:: ylimits : array [ymin, ymax]  or 'auto'

     The y-axis limits if an array with two elements, or choose
     automatically

  .. attribute:: xticks_fontsize : float

     Fontsize for xtick mark labels

  .. attribute:: xticks_kwargs : dictionary

     Other kwargs to be passed to `xticks` (e.g. locations)

  .. attribute:: xlabel : str

     Label for x-axis

  .. attribute:: xlabel_fontsize : str

     Fontsize for x-axis label

  .. attribute:: xlabel_kwargs : dictionary

     Other kwargs to be passed to `xlabel` (e.g. color)

  .. attribute:: yticks_fontsize : float

     Fontsize for ytick mark labels

  .. attribute:: yticks_kwargs : dictionary

     Other kwargs to be passed to `yticks` (e.g. locations)

  .. attribute:: ylabel : str

     Label for y-axis

  .. attribute:: ylabel_fontsize : str

     Fontsize for y-axis label

  .. attribute:: ylabel_kwargs : dictionary

     Other kwargs to be passed to `ylabel` (e.g. color)


  .. attribute:: aspect : float

     Aspect ratio for plot, used internally in the command::

        plt.gca().set_aspect(plotaxes.aspect)

  .. attribute:: aspect_latitude : float

     For plots in longitude-latitude coordinates, the latitude to use for
     chosing the aspect ratio so that distances in meters are the same
     in x and y at this latitude. (For plots covering a broad range of
     latitudes, the the latitude near the middle or near the location of 
     most interest is generally most appropriate.

     This value is used internally in the command::

        plt.gca().set_aspect(1./np.cos(plotaxes.aspect_latitude \
                            * np.pi/180))

  .. attribute:: useOffset : boolean

     If `True`, then tick marks may be labeled with an offset from some
     common value that is printed at the corner.  Often it is nicer to see
     the full value at each tick mark, for which this should be set to `False`.

     Internally the command::
        
        plt.ticklabel_format(useOffset = plotaxes.useOffset)

     is issued if `useOffset is not None`.

  .. attribute:: grid : boolean

     If `True` then internally the command::

        plt.grid(**plotaxes.grid_kwargs)

     is issued to add grid lines to the plot. 

  .. attribute:: grid_kwargs : dictionary

     Any kwargs to be passed to `plt.grid`, e.g. `'color'` or `'linewidth'`.

  .. attribute:: kwargs : dictionary

     Any other attributes to be passed to `axes` command.


  .. attribute:: afteraxes : function or str

     A string or function that is to be executed after creating all 
     plot items on this axes.
     If a string, this string is executed using *exec*.  If a
     function, it should be defined to have a single argument
     :ref:`current_data`.  

     The string version is useful for 1-liners such as::

        afteraxes = "pylab.title('My custom title')"

     pylab commands can be used, since pylab has been imported into the
     plotting module.
     
     The function form is better if you want to do several things, or if you
     need access to the data stored in :ref:`current_data`.  For example::

        def afteraxes(current_data):
            # add x- and y-axes to a 1d plot already created
            from pylab import plot

            xlower = current_data.xlower
            xupper = current_data.xupper
            plot([xlower, xupper], [0.,0.], 'k')   # x-axis

            # Get y limits from variable just plotted, which is
            # available in current_data.var.  
            ymin = current_data.var.min() 
            ymax = current_data.var.max()
            plot([0.,0.], [ymin,ymax], 'k')  # y-axis



Attributes for gauge plots
==========================

The following attributes are primarily useful for gauge plots, where the
horizontal axis is time `t` rather than `x`, and are implemented in
`$CLAW/visclaw/src/python/visclaw/gaugetools.py`:

  .. attribute:: time_scale : float

     Scaling for time values, e.g. if `t` is in seconds but you want the
     plot to show hours on the horizontal axis then set
     `time_scale = 1/3600.`.

  .. attribute:: time_label : str

     Label for time axis (same as setting `xlabel`)

  .. attribute:: time_label_fontsize : float
    
     Fontsize for `xlabel` (time axis)

  .. attribute:: time_label_kwargs : dictionary

     Other kwargs to be passed to `xlabel` (e.g. color)

Methods
=======

  .. method:: new_plotitem(name=None, plot_type)

     Returns an object of class :ref:`ClawPlotItem` associated with this axes.
     A single axes may have several items associated with it.

     The name specified is used as a dictionary key.  If None is provided, 
     one is generated automatically of the form ITEM1, etc.


  .. method:: gethandle()

     Returns the handle for this axes.  

