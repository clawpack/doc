
.. _docker_image:

Docker for Clawpack
===================

Rather than installing Clawpack and all its dependencies on your computer, if
you have `Docker <https://www.docker.com/>`_ installed then you can now use a
docker image from the `DockerHub Clawpack repositories
<https://hub.docker.com/u/clawpack/dashboard/>`_.

To download an image::

    $ docker pull clawpack/v5.6.1_dockerimage

To create a container and run it::

    $ docker run -i -t -p 8889:8889 --name clawpack-v5.6.1_container \
        clawpack/v5.6.1_dockerimage

You can change the container name if you wish, and also the port 8889 (on
which jupyter notebooks might be served, see below).

You should now see a prompt like::

    jovyan $ 

indicating that you are in the container, logged in as user `jovyan`.

Once logged in to the container, you should find a directory
`$HOME/clawpack-v5.6.1` that contains the Clawpack installation (including the
current master branch of the :ref:`apps`).

A better image for GeoClaw users
--------------------------------

**Still under development**

GeoClaw users might want to instead use the image `clawpack/v5.6.1_geoclaw`,
which includes everything in `clawpack/v5.6.1_dockerimage` but also installs
a number of other tools useful for GeoClaw users, see the Dockerfile
`clawpack/docker-files/Dockerfile_v5.6.1_geoclaw <https://github.com/clawpack/docker-files/blob/master/Dockerfile_v5.6.1_geoclaw>`_.


Stopping a container
--------------------

You can exit a container (after using `ctrl-C` to quit the jupyter server if
one is running) via::

    exit

at the `jovyan $` prompt.

Restarting a container
----------------------

You can restart the container via::

    docker start -a -i clawpack-v5.6.1_container


Running Jupyter notebooks
-------------------------

The form of run command suggested above also allows you to run Jupyter
notebooks from port 8889 on your own computer (or whatever port you 
specified when creating the container).

To start the sever, in the docker container (at the `jovyan $` prompt)
run this command::

    jupyter notebook --ip=0.0.0.0 --port=8889 --no-browser

Then open a browser (on the host machine) to::

    http://localhost:8889/?token=TOKEN

replacing `TOKEN` with the token that should have printed out when you started
the server.

This will open to the top level of `$HOME`, and you can then navigate to
wherever the notebooks are you want to run, e.g. the sample ones in the
`apps` repository can be found at `clawpack-v5.6.1/apps/notebooks`.

PyClaw users might want to start with
`clawpack-v5.6.1/apps/notebooks/pyclaw/Acoustics-1D.ipynb`.

GeoClaw users might want to try running
`clawpack-v5.6.1/apps/notebooks/geoclaw/chile2010a.ipynb`,
which exercises most aspects of GeoClaw.


Moving files between the docker container and the host machine
------------------------------------------------------------------

Often you want to run the code on Docker and then transfer the resulting output
files, and/or the plots generated, back to the host machine (e.g. some
directory on your laptop).  You can use the `--volume` flag when running a
container to accomplish this, see 
`docker volume documentation <https://docs.docker.com/storage/volumes/>`_.

Some other useful docker commands
---------------------------------

See the `docker command line documentation <https://docs.docker.com/engine/reference/commandline/cli/>`_
or any of the tutorials available on-line for more details, but here are a
few particularly useful commands::

    docker help
    docker info

    docker ps -a  # list all containsers
    docker rm clawpack-v5.6.0_container  # remove a container

    docker images -a  # list all images
    docker rmi clawpack/v5.6.0_dockerimage  # remove an image
    docker prune  # remove all images not used by any container



Creating your own docker image
------------------------------

If you want to create a new docker image that includes other software in
addition to Clawpack, you can find the `Dockerile` used to create the docker
image on dockerhub in the repository
https://github.com/clawpack/docker-files.

This might be useful if you want to distribute your own code that depends on
Clawpack in a form that's easy for others to use.

You can also create a Dockerfile that uses the already-build Clawpack 5.6.1
on Dockerhub by starting the Dockerfile with::

    FROM clawpack/v5.6.1_dockerimage:release

and then adding anything addition you want in the image, 
such as other Python modules you need or your own application code.
You may need to specify `USER root` in order to install some things, and
then switch back to `USER jovyan` at the end.  For an example, see
`clawpack/docker-files/Dockerfile_v5.6.1_geoclaw <https://github.com/clawpack/docker-files/blob/master/Dockerfile_v5.6.1_geoclaw>`_.


Dockerfiles for binder
----------------------

The username jovyan was chosen so that you can use this docker image also for 
starting up a Jupyter notebook server on `binder
<http://www.mybinder.org>`_.  You can do this by
including a simple Dockerfile at the top level of your repository that
uses the dockerhub image, as above. See this repository for a simple example:
`<https://github.com/rjleveque/test_binder>`_.

See `the binder documentation
<https://mybinder.readthedocs.io/en/latest/sample_repos.html#minimal-dockerfiles-for-binder>`_
for more details on using Dockerfiles there.

