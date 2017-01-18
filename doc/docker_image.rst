
.. _docker_image:

Docker for Clawpack
===================

Rather than installing Clawpack and all its dependencies on your computer, if
you have `Docker <https://www.docker.com/>`_ installed then you can now use a
docker image from the `DockerHub Clawpack repositories
<https://hub.docker.com/u/clawpack/dashboard/>`_.

To download an image::

    $ docker pull clawpack/v5.4.0_dockerimage

To create a container and run it::

    $ docker run -i -t -p 8889:8889 --name clawpack-v5.4.0_container \
        clawpack/v5.4.0_dockerimage

You can change the container name if you wish.

You should now see a prompt like::

    root...# 

indicating that you are in the container.  There will be a directory
`/clawpack-v5.4.0` that contains the Clawpack installation (including the
current master branch of the :ref:`apps`).

Running Jupyter notebooks
-------------------------

The form of run command suggested above also allows you to run Jupyter
notebooks from port 8889 on your own computer (you can change the port number
if you want).  

To do so, in the docker container run this command::

    root...# jupyter notebook --notebook-dir=/clawpack-v5.4.0/apps/notebooks \
                 --ip='*' --port=8889 --no-browser

Then open a browser to::

    http://localhost:8889/tree

You should be in the `apps/notebooks` directory and can browse from there to
various notebooks.

You can exit a container (after using `ctrl-C` to quit the jupyter server if
one is running) via::

    root...# exit

Restarting a container
----------------------

You can restart the container via::

    docker start -a -i clawpack-v5.4.0_container


More resources:
---------------

 - `Introduction to Docker
   <https://geohackweek.github.io/Introductory/01-docker-tutorial/>`_ from 
   the recent `GeoHack Week <https://geohackweek.github.io>`_ at UW.

 - https://github.com/clawpack/docker-files contains the Dockerfile used to
   create this image.  You can modify if you want to create an image that
   includes other dependencies for your own work, for example.

