
# The Clawpack 5.x Software

Authors: Anyone who has....
* Made a nontrivial contribution to 5.0, 5.1, 5.2,
* Contributes at least a sentence to the paper,
* Has read the final draft and agreed to be an author.

## Github organization, subrepositories
Clawpack includes several related software projects, each of which is managed in its own repository on Github.  These projects are sub-repositories of the high-level Clawpack repository and are assigned to the Clawpack Github organization.  The set of maintainers -- with push and merge privileges -- is different for each sub-repository.  The main solver repositories are:

- Riemann (Riemann solvers used by all the other projects)
- Classic
- AMRClaw
- GeoClaw
- PyClaw

Additional repositories contain documentation and extended examples of using the code:
- doc
- apps

## Development model
* forks, master, branches, pull requests
* travis

## Global changes
* reordering indices
* input variables in setrun.py (discuss Python interface to Fortran)

## riemann repository -- used by PyClaw via f2py

## classic: 
* added 3d with OpenMP

## amrclaw: 
* added 3d with OpenMP, 
* added regions
* other changes motivated by Geoclaw

## geoclaw: 
* NTHMP benchmarks
* setaux copying for faster topography integration, recursive 
* new topotools and dtopotools
* multiple dtopo files
* fixed grid monitoring of max values

## PyClaw:
Later 4.x releases included a number of Python-based tools for handling Clawpack input and output.  The 5.0 release includes a full-fledged Python solver in which the higher-level parts of Clawpack have been reimplemented in Python.  This new solver also includes access to the high-order algorithms introduced in SharpClaw and can be used on large distributed-memory parallel machines.  Lower-level code (whatever gets executed repeatedly and needs to be fast) from the earlier Fortran Classic and SharpClaw codes is automatically wrapped at install time using f2py.

* overall structure/languages figure
* sharpclaw
* petclaw
* f2py
* pip install
* IPython notebooks

## visclaw:
* Iplotclaw
* creation of html pages
* JSAnimation
* (Once 3d is working, write a separate paper on visclaw as a general tool?)

## future plans:
* Clawpack 6 ideas
* Riemann solvers
* ForestClaw
* ???

