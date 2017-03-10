"""
Module for making galleries of thumbnails allowing easy browsing of
applications directories.

These tools assume that the examples have already been run and the plots
produced using the script make_plots.py.

"""
import os
from clawpack import pyclaw


# Main root for html links:
# claw_html_root='http://localhost:50005'
claw_html_root='..'

# Determine Clawpack directory:
try:
    clawdir_default = os.environ['CLAW']+'/'
except KeyError:
    clawdir_default = os.path.join('/'.join(pyclaw.__path__[0].split('/')[:-1])+'/')
    print('CLAW environment variable not set; using '+clawdir_default)

# Location for gallery files:
gallery_dir_default = '.'  # os.path.join(clawdir_default,'doc/gallery')

remake = True   # True ==> remake all thumbnails even if they exist.

class GalleryItem(object):

    def __init__(self, appdir, appname, plotdir, description, images):
        self.appdir = appdir
        self.appname = appname
        self.plotdir = '_plots_'+appname
        self.description = description
        self.images = images

class GallerySection(object):

    def __init__(self,title,description=""):
        self.title = title
        self.description = description
        self.items = []

    def new_item(self, appdir, appname, plotdir, description, thumbs):
        gitem = GalleryItem(appdir, appname, plotdir, description, thumbs)
        self.items.append(gitem)
        return gitem


class Gallery(object):

    def __init__(self, title, clawdir=clawdir_default):
        self.title = title
        self.clawdir = clawdir
        self.claw_html_root = claw_html_root
        self.sections = []

    def new_section(self, title, description=""):
        gsec = GallerySection(title, description)
        gsec.items = []
        self.sections.append(gsec)
        return gsec

    def create(self,fname,gallery_dir=None, copy_plots=True, write_file=True):

        # Directory for gallery files:
        if gallery_dir is None:
            gallery_dir = gallery_dir_default

        print("Gallery files will be created in directory ")
        print("   ", gallery_dir)

        try:
            if not os.path.isdir(gallery_dir):
                os.system('mkdir %s' % gallery_dir)
                print("Created directory ",gallery_dir)
            start_dir = os.getcwd()
            os.chdir(gallery_dir)
        except:
            print("*** Error moving to directory ",gallery_dir)
            print("*** Gallery not created")
            raise

        if write_file:
            gfile = open(fname, 'w')
        else:
            gfile = open(os.devnull, 'w')

        gfile.write(":group: pyclaw\n\n")
        gfile.write(".. _%s:\n\n" % os.path.splitext(fname)[0])
        nchar = len(self.title)
        gfile.write(nchar*"=" + "\n")
        gfile.write("%s\n"  % self.title)
        gfile.write(nchar*"=" + "\n")
        gfile.write(".. contents::\n\n")

        # gfile.write("%s\n" % self.title)
        # gfile.write("="*len(self.title)+"\n\n")

        for gsec in self.sections:
            gfile.write("%s\n" % gsec.title)
            gfile.write("="*len(gsec.title)+"\n")
            gfile.write("%s\n" % gsec.description)

            for gitem in gsec.items:

                if not os.path.exists('./'+gitem.appdir):
                    os.makedirs('./'+gitem.appdir)
                static_dir = clawdir_default+'doc/doc/_static/'

                if not os.path.exists(static_dir+gitem.appdir):
                    os.system('mkdir -p %s' % (static_dir+gitem.appdir))
                print("+++ static_dir = "+static_dir+gitem.appdir)

                if copy_plots:
                    os.system('cp -r %s/%s %s' % (self.clawdir+gitem.appdir,
                              gitem.plotdir, static_dir+gitem.appdir+'/'+gitem.plotdir))

                gfile.write('\n')
                desc = gitem.description.lstrip().replace('\n',' ')
                gfile.write('%s\n\n' % desc)
                plotindex = os.path.join(claw_html_root, '../_static',
                                         gitem.appdir, gitem.plotdir,
                                         '_PlotIndex.html')
                sourcepage = gitem.appname+'.html'
                gfile.write('`Source code <%s>`__ ... \n`Plots <%s>`__\n'
                            % (sourcepage,plotindex))

                if not os.path.exists('./'+gitem.appdir):
                    os.makedirs('./'+gitem.appdir)
                gfile.write('\n\n')

                # For each example, write a page containing the source
                rf = open(gitem.appname+'.rst','w')
                rf.write('.. _'+gitem.appname+':\n')
                rf.write('\n')
                rf.write(gsec.title+'\n')
                rf.write('-'*len(gsec.title)+'\n')
                rf.write('\n')
                rf.write('.. automodule:: pyclaw.examples.'+gitem.appdir.split('/')[-1]+'.'+gitem.appname+'\n')

                rf.write('\n')
                rf.write('Output:\n')
                rf.write('~~~~~~~\n')

                for image in gitem.images:

                    src_name = os.path.join(gitem.appdir, gitem.plotdir, image)
                    thumb_name = src_name.replace('/','_')
                    src_html = os.path.join(claw_html_root,'../_static',
                                            src_name) + '.html'
                    src_name = os.path.join(self.clawdir,src_name)
                    src_png = src_name + '.png'
                    if not os.path.isdir('thumbnails'):
                        print("Creating directory thumbnails")
                        os.system('mkdir thumbnails')
                    thumb_file = os.path.join('thumbnails',thumb_name + '.png')
                    if os.path.isfile(thumb_file) and (not remake):
                        print("Thumbnail exists: ",thumb_file)
                    else:
                        scale = 0.3
                        make_thumb(src_png, thumb_file, scale)

                    gfile.write('.. image:: %s\n   :width: 5cm\n' % thumb_file)
                    gfile.write('   :target: %s\n' % src_html)

                    rf.write('.. image:: %s\n   :width: 5cm\n' % thumb_file)
                    rf.write('   :target: %s\n' % src_html)

                gfile.write('\n\n')
                gfile.write('\n\n')

                rf.write('\n\n')
                rf.write('Source:\n')
                rf.write('~~~~~~~\n')
                rf.write('.. literalinclude:: ../../../../'+gitem.appdir+'/'+gitem.appname+'.py'+'\n')
                rf.close()

        print("Created ",fname, " in directory ", os.getcwd())
        os.chdir(start_dir)


def make_thumb(src_file, thumb_file, scale):

    from numpy import floor
    if not os.path.exists(src_file):
        print('*** Error in make_thumb: cannot find file ',src_file)
    else:
        # convert scale to percent:
        scale = int(floor(scale*100))
        os.system('convert -resize %s' % scale + '% ' +
                  '%s %s' % (src_file, thumb_file))
        # print("Converted ",src_file)
        # print("   to     ",thumb_file)


def test():
    gallery = Gallery(title="Test Gallery")
    plotdir = '_plots'
    gsec = gallery.new_section('1-dimensional advection')

    appdir = 'pyclaw/examples/advection/1d'
    appname = 'advection_1d'
    description = """
        Advecting Gaussian with periodic boundary."""
    images = ('frame0000fig1', 'frame0004fig1')
    gsec.new_item(appdir, appname, plotdir, description, images)

    gallery.create('test.rst')


def make_1d():
    gallery = Gallery(title="Gallery of 1d PyClaw applications")
    plotdir = '_plots'

    # ----------------------------------------------
    gsec = gallery.new_section('1-dimensional advection')
    appdir = 'pyclaw/examples/advection_1d'
    appname = 'advection_1d'
    description = """
         Advecting Gaussian with periodic boundary."""
    images = ('frame0000fig1', 'frame0004fig1', 'frame0010fig1')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------
    gsec = gallery.new_section('1-dimensional variable-velocity advection')
    appdir = 'pyclaw/examples/advection_1d_variable'
    appname = 'variable_coefficient_advection'
    description = """
         Advecting Gaussian and square wave with periodic boundary."""
    images = ('frame0000fig1', 'frame0004fig1', 'frame0008fig1')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------
    gsec = gallery.new_section('1-dimensional acoustics')
    appdir = 'pyclaw/examples/acoustics_1d_homogeneous'
    appname = 'acoustics_1d'
    description = """
         Acoustics equations with wall boundary at left and extrap at
         right."""
    images = ('frame0000fig1', 'frame0002fig1', 'frame0005fig1')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------
    gsec = gallery.new_section("1-dimensional Burgers' equation")
    appdir = 'pyclaw/examples/burgers_1d'
    appname = 'burgers_1d'
    description = """
        Burgers' equation with sinusoidal initial data, steepening to
        N-wave.  """
    images = ('frame0000fig0', 'frame0003fig0', 'frame0006fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------
    gsec = gallery.new_section("1-dimensional shallow water equation")
    appdir = 'pyclaw/examples/shallow_1d'
    appname = 'dam_break'
    description = """Shallow water shock tube."""
    images = ('frame0000fig0', 'frame0003fig0', 'frame0006fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    appname = 'sill'
    description = """Flow over a sill."""
    images = ('frame0000fig0', 'frame0003fig0', 'frame0006fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------
    gsec = gallery.new_section("1-dimensional nonlinear elasticity")
    appdir = 'pyclaw/examples/stegoton_1d'
    appname = 'stegoton'
    description = """
        Evolution of two trains of solitary waves from an initial gaussian.
        """
    images = ('frame0000fig1', 'frame0003fig1', 'frame0005fig1')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------
    gsec = gallery.new_section("1-dimensional Euler equations")
    appdir = 'pyclaw/examples/euler_1d'
    description = """
        Woodward-Colella blast-wave interaction problem.
        """
    appname = 'woodward_colella_blast'
    images = ('frame0000fig0', 'frame0003fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    description = """ Shu-Osher problem.  """
    appname = 'shocksine'
    images = ('frame0000fig0', 'frame0003fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    description = """ Shock tube problem.  """
    appname = 'shocktube'
    images = ('frame0000fig0', 'frame0003fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    # ----------------------------------------------

    gallery.create('gallery_1d.rst', write_file=False)
    return gallery


def make_2d():
    gallery = Gallery("Gallery of 2d PyClaw applications")
    plotdir = '_plots'

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional advection')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/advection_2d'
    appname = 'advection_2d'
    description = """
        Advecting square with periodic boundary conditions."""
    images = ('frame0000fig0', 'frame0002fig0', 'frame0004fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional variable-coefficient advection')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/advection_2d_annulus'
    appname = 'advection_annulus'
    description = """
        Advection in an annular region."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0008fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional acoustics')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/acoustics_2d_homogeneous'
    appname = 'acoustics_2d'
    description = """
        Expanding radial acoustic wave in a homogeneous medium."""
    images = ('frame0000fig0', 'frame0002fig0', 'frame0004fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional variable-coefficient acoustics')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/acoustics_2d_variable'
    appname = 'acoustics_2d_interface'
    description = """
        Expanding radial acoustic wave in a two-material medium with an interface."""
    images = ('frame0000fig0', 'frame0010fig0', 'frame0020fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    appdir = 'pyclaw/examples/acoustics_2d_mapped'
    appname = 'acoustics_2d_inclusions'
    description = """
        Acoustic wave scattered by two cylinders."""
    images = ('frame0000fig0', 'frame0010fig0', 'frame0020fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    gsec = gallery.new_section('2-dimensional advection-reaction')
    appdir = 'pyclaw/examples/advection_reaction_2d'
    appname = 'advection_reaction'
    description = ""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional shallow water equations')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/shallow_2d'
    appname = 'radial_dam_break'
    description = """Radial dam-break."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional shallow water on the sphere')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/shallow_sphere'
    appname = 'Rossby_wave'
    description = """Wavenumber 4 Rossby-Haurwitz wave on a rotating sphere."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional Euler equations')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/euler_2d'
    appname = 'shock_bubble_interaction'
    description = """ Shock-bubble interaction."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    appname = 'shock_forward_step'
    description = """ Shockwave hitting a step."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)

    appname = 'quadrants'
    description = """Quadrants: 2D Riemann problem with four shockwaves."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional KPP equation')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/kpp'
    appname = 'kpp'
    description = """
        Non-convex flux example."""
    images = ('frame0000fig1', 'frame0004fig1', 'frame0010fig1')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    # ----------------------------------------------
    gsec = gallery.new_section('2-dimensional p-system')
    # ----------------------------------------------
    appdir = 'pyclaw/examples/psystem_2d'
    appname = 'psystem_2d'
    description = """
        Radial wave in a checkerboard-like medium."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0010fig0')
    gsec.new_item(appdir, appname, plotdir, description, images)
    # ----------------------------------------------

    gallery.create('gallery_2d.rst', write_file=False)
    return gallery

def make_all():
    gallery_1d = make_1d()
    gallery_2d = make_2d()

    # make gallery of everything:
    gallery_all = Gallery(title="Gallery of all PyClaw applications")
    gallery_all.sections = gallery_1d.sections + gallery_2d.sections
    gallery_all.create('gallery_all.rst')


if __name__ == "__main__":
    make_all()
