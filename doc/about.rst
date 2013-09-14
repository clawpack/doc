.. _about:

===================
About this software
===================

Clawpack stands for "Conservation Laws Package" and was initially developed
for linear and nonlinear hyperbolic systems of conservation laws, with a
focus on implementing high-resolution Godunov type methods using limiters in
a general framework applicable to many applications.  These finite volume
methods require a "Riemann solver" to resolve the jump discontinuity at the
interface between two grid cells into waves propagating into the neighboring
cells.

Adaptive mesh refinement is included, see :ref:`amrclaw`.

Recent extensions allow the solution of hyperbolic problems that are not in
conservation form.  We are actively working on extensions to parabolic
equations as well.

The "wave propagation" algorithms implemented in Clawpack are discribed in
detail in the book *Finite Volume Methods for Hyperbolic Problems*
[LeVeque-FVMHP]_.
Virtually all of the figures in this book were generated using Clawpack
(version 4.3). 

See :ref:`book` for a list of available examples with pointers to the codes
and resulting plots.

See the :ref:`biblio` for some pointers to papers describing Clawpack and
the algorithms used in more detail.



License
-------

Clawpack is distributed under the terms of the
Berkeley Software Distribution (BSD) license.  

See :ref:`license` for details.

.. _authors:

Authors
-------

Many people have contributed to the development of Clawpack since its
inception in 1994.  

Major algorithmic and software design contributions have been made by the 
following individuals:

* Randall J. LeVeque, University of Washington, 
  `@rjleveque <https://github.com/rjleveque/>`_.

* Marsha Berger, Courant Institute, NYU,
  `@mjberger <https://github.com/mjberger/>`_.

* Jan Olav Langseth, Norwegian Defence Research Establishment.

* David George, USGS Cascades Volcano Observatory, 
  `@dlgeorge <https://github.com/dlgeorge/>`_.

* David Ketcheson, KAUST
  `@ketch <https://github.com/ketch/>`_.

* Kyle Mandli, UT-Austin,
  `@mandli <https://github.com/mandli/>`_.

Other major contributors include:

* Aron Ahmadia, 
  `@ahmadia <https://github.com/ahmadia/>`_.
* Amal Alghamdi,
  `@amal-ghamdi <https://github.com/amal-ghamdi/>`_.
* Peter Blossey.
* Donna Calhoun, 
  `@donnaboise <https://github.com/donnaboise/>`_.
* Ondřej Čertík,
  `@certik <https://github.com/certik/>`_.
* Grady Lemoine, 
  `@gradylemoine <https://github.com/gradylemoine/>`_.
* Sorin Mitran. 
* Matteo Parsani,
  `@mparsani <https://github.com/mparsani/>`_.
* Andy Terrel,
  `@aterrel <https://github.com/aterrel/>`_.


Numerous students and other users have also contributed towards this software, 
by finding bugs, suggesting improvements, and exploring its use on new
applications.  Thank you!

.. _citing:

Citing this work
----------------

If you use Clawpack in publications, please cite the following::

    @misc{clawpack,
        title={Clawpack software}, 
        author={Clawpack Development Team}, 
        url={http://www.clawpack.org}, 
        note={Version x.y}
        year={2013}}

Please fill in the version number that you used.

Please also cite at least one of the following regarding the algorithms used
in Clawpack (click the links for bibtex citations):

* Basic algorithms in 1d and 2d:  [LeVeque97]_, [LeVeque-FVMHP]_

* 3d algorithms: [LangsethLeVeque00]_

* AMR: [BergerLeVeque98]_

* f-wave algorithms: [BaleLevMitRoss02]_

* GeoClaw: [BergerGeorgeLeVequeMandli11]_, [LeVequeGeorgeBerger]_

See also :ref:`pyclaw` for PyClaw citations.

.. _funding:

Funding 
-------

Development of this software has been supported in part by

 * NSF Grants DMS-8657319, DMS-9204329, DMS-9303404, DMS-9505021, 
   DMS-96226645, DMS-9803442, DMS-0106511, CMS-0245206,  DMS-0609661,
   DMS-0914942, DMS-1216732.

 * DOE Grants DE-FG06-93ER25181,  DE-FG03-96ER25292, DE-FG02-88ER25053,
   DE-FG02-92ER25139, DE-FG03-00ER2592, DE-FC02-01ER25474

 * AFOSR grant F49620-94-0132, 

 * NIH grant 5R01AR53652-2,

 * ONR grant N00014-09-1-0649

 * The Norwegian Research Council (NFR) through the program no.  101039/420.

 * The Scientific Computing Division at the National Center for Atmospheric
   Research (NCAR).

 * The Boeing Professorship and the Founders Term Professorship in the
   Department of Applied Mathematics, University of Washington.

Any opinions, findings, and conclusions or recommendations expressed in this
material are those of the author(s) and do not necessarily reflect the views
of these agencies. 



