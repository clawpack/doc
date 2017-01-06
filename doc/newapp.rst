
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
a new directory.  Clawpack should work fine
from any directory as long as the environment variable is set properly.
(See :ref:`setenv`.)

In unix/linux you can copy a directory recursively (with all subdirectories
intact) using the *cp -r* command, e.g. ::
 
    $ cp -r $CLAW/classic/examples/acoustics_1d_example1  path/to/newdir
 

