
.. _newapp:


*************************************
Creating a new application directory
*************************************

.. _copyex:

Copying an existing example
---------------------------


The simplest approach to implementing something new is to start with a
Clawpack example and modify the code appropriately.


Rather than modifying one of the examples in place, it is best to copy it to
a new directory.  You might want to create a 
directory $CLAW/myclaw at the top level 
of Clawpack that can be used to put your own work, but Clawpack should work
from any directory as long as the environment variable is set properly.
(See :ref:`setenv`.)

In unix/linux you can copy a directory recursively (with all subdirectories
intact) using the *cp -r* command, e.g. ::
 
    $ cp -r $CLAW/amrclaw/examples/example1  path-to-newdir
 

