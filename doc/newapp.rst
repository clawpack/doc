
.. _newapp:


*************************************
Creating a new application directory
*************************************

.. _copyex:

Copying an existing example
---------------------------

.. warning:: Out of date!  Needs updating.


The simplest approach to implementing something new is to start with a
Clawpack example and modify the code appropriately.

For existing examples, see the applications in $CLAW/apps, which can be
perused at :ref:`apps`.

See also the :ref:`book`.

Rather than modifying one of the examples in place, it is best to copy it to
a new directory.  There is a directory $CLAW/myclaw at the top level 
of Clawpack that can be used to put your own work.  This way if you use
the Python server (see :ref:`startserver`)
you can view your files and plots via the web address
http://localhost:50005/myclaw/...

If your myclaw directory is located elsewhere, you can also create a
symbolic link from the top claw level to the actual location and the above
address should still work.

In unix/linux you can copy a directory recursively (with all subdirectories
intact) using the *cp -r* command, e.g. ::
 
    $ cp -r $CLAW/amrclaw/Tests/example1  path-to-newdir
 
for example.  

