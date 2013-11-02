"""
Module for making galleries of thumbnails allowing easy browsing of
applications directories.

These tools assume that the examples have already been run and the plots
produced using "bash make_all.sh" or "make .plots".  

You should use the script make_plots.py to do this first.
"""

import os, glob


# Main root for html links:
#claw_html_root='http://clawpack.github.io/doc/gallery'
claw_html_root='.'

# Determine directory:
try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("Need to set CLAW environment variable")

# Location for gallery files:
gallery_dir_default = '.'

remake = True   # True ==> remake all thumbnails even if they exist.

class GalleryItem(object):
    
    def __init__(self, appdir, plotdir, description, images):
        self.appdir = appdir
        self.plotdir = plotdir
        self.description = description
        self.images = images

class GallerySection(object):
    
    def __init__(self,title,description=""):
        self.title = title
        self.description = description
        self.items = []

    def new_item(self, appdir, plotdir, description, thumbs):
        gitem = GalleryItem(appdir, plotdir, description, thumbs)
        self.items.append(gitem)
        return gitem


class Gallery(object):
    import os
    
    def __init__(self, title, clawdir=CLAW):
        self.title = title
        self.clawdir = clawdir
        self.claw_html_root = claw_html_root
        self.sections = []

    def new_section(self, title, description=""):
        gsec = GallerySection(title, description)
        gsec.items = []
        self.sections.append(gsec)
        return gsec
    
    def create(self,fname,gallery_dir=None, copy_plots=True, copy_files=True):

        # Directory for gallery files:
        if gallery_dir is None:
            gallery_dir = gallery_dir_default

        print "Gallery files will be created in directory "
        print "   ", gallery_dir

        try:
            if not os.path.isdir(gallery_dir):
                os.system('mkdir %s' % gallery_dir)
                print "Created directory ",gallery_dir
            start_dir = os.getcwd()
            os.chdir(gallery_dir)
        except:
            print "*** Error moving to directory ",gallery_dir
            print "*** Gallery not created"
            raise

        gfile = open(fname, 'w')
        #gfile.write(":group: pyclaw\n\n")
        gfile.write(".. _%s:\n\n" % os.path.splitext(fname)[0])
        nchar = len(self.title)
        gfile.write(nchar*"=" + "\n")
        gfile.write("%s\n"  % self.title)
        gfile.write(nchar*"=" + "\n")
        gfile.write(".. contents::\n\n")

        #gfile.write("%s\n" % self.title)
        #gfile.write("="*len(self.title)+"\n\n")
        
        for gsec in self.sections:
            gfile.write("%s\n" % gsec.title)
            gfile.write("="*len(gsec.title)+"\n")
            gfile.write("%s\n" % gsec.description)

            for gitem in gsec.items:

                if not os.path.exists('./'+gitem.appdir):
                    os.makedirs ('./'+gitem.appdir)
                static_dir = '$CLAW/doc/doc/_static/'

                if not os.path.exists(static_dir+gitem.appdir):
                    os.system('mkdir -p %s' % (static_dir+gitem.appdir))
                print "+++ static_dir = ",static_dir

                os.system('cp %s/README.rst %s' % ('$CLAW/'+gitem.appdir, './'+gitem.appdir))
                if copy_plots:
                    #os.system('cp -r %s/_plots %s' % ('$CLAW/'+gitem.appdir, './'+gitem.appdir))
                    os.system('cp -r %s/_plots %s' % ('$CLAW/'+gitem.appdir, \
                                static_dir+gitem.appdir))
                if copy_files:
                    files = []
                    for ft in ['*.f','*.f90','*.py','*.m','*.html','Makefile']:
                        files = files + glob.glob('%s/%s' % (CLAW+'/'+gitem.appdir,ft))
                    # also copy over claw_git_* files to have a record
                    # of how these plots were created
                    clawgit = glob.glob('%s/_output/claw_git*' % (CLAW+'/'+gitem.appdir))
                    files = files + clawgit
                    for file in files:
                        os.system('cp %s %s' % (file, static_dir+gitem.appdir))
                    print "+++ copied files to ",static_dir+gitem.appdir
                    #print "+++ files: ",files




                subtitle = '**Directory: `$CLAW/%s`** \n' % gitem.appdir
                gfile.write('\n')
                gfile.write(subtitle + '\n')
                #gfile.write(len(subtitle)*'-' + '\n')
                desc = gitem.description.lstrip().replace('\n',' ')
                gfile.write('%s\n\n' % desc)
                plotindex = os.path.join(claw_html_root, '../_static', \
                        gitem.appdir, gitem.plotdir, '_PlotIndex.html')
                readme = os.path.join(claw_html_root, '../_static', \
                        gitem.appdir, 'README.html')
                gfile.write('`README <%s>`__ ... \n`Plots <%s>`__\n' \
                      % (readme,plotindex))
                code = os.path.join(claw_html_root, gitem.appdir)
                gfile.write('\n\n')

                for image in gitem.images:

                    src_name = os.path.join(gitem.appdir, gitem.plotdir, image)
                    thumb_name = src_name.replace('/','_')
                    src_html = os.path.join(claw_html_root,'../_static', \
                        src_name) + '.html'
                    src_name = os.path.join(self.clawdir,src_name)
                    src_png = src_name + '.png'
                    if not os.path.isdir('thumbnails'):
                        print "Creating directory thumbnails"
                        os.system('mkdir thumbnails')
                    thumb_file = os.path.join('thumbnails',thumb_name + '.png')
                    if os.path.isfile(thumb_file) and (not remake):
                        print "Thumbnail exists: ",thumb_file
                    else:
                        scale = 0.3
                        make_thumb(src_png ,thumb_file, scale)
                    gfile.write('.. image:: %s\n   :width: 5cm\n' % thumb_file)
                    gfile.write('   :target: %s\n' % src_html)
                gfile.write('\n\n')

        print "Created ",fname, " in directory ", os.getcwd()
        os.chdir(start_dir)
                    

def make_thumb(src_file, thumb_file, scale):
    
    from numpy import floor 
    if not os.path.exists(src_file):
        print '*** Error in make_thumb: cannot find file ',src_file
    else:
        # convert scale to percent:
        scale = int(floor(scale*100))
        os.system('convert -resize %s' % scale + '% ' + \
            '%s %s' % (src_file, thumb_file))
        print "Converted ",src_file
        print "   to     ",thumb_file

   

def test():
    gallery = Gallery(title="Test Gallery")
    plotdir = '_plots'
    gsec = gallery.new_section('1-dimensional advection')

    appdir = 'amrclaw/examples/advection_2d_square'
    description = """
        Advecting square with periodic boundary."""
    images = ('frame0000fig1', 'frame0004fig1')
    gsec.new_item(appdir, plotdir, description, images)
       
    gallery.create('test.rst',copy_files=True)



def make_1d():
    gallery = Gallery(title="Gallery of 1d Classic applications")
    plotdir = '_plots'


    #----------------------------------------------
    gsec = gallery.new_section('1-dimensional acoustics')
    appdir = 'classic/examples/acoustics_1d_example1'
    description = """
         Acoustics equations with interface showing reflection and
         transmission."""
    images = ('frame0000fig1', 'frame0004fig1', 'frame0010fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'classic/examples/acoustics_1d_heterogeneous'
    description = """
         Acoustics equations with interface showing reflection and
         transmission."""
    images = ('frame0000fig0', 'frame0007fig0', 'frame0010fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
       
    gallery.create('gallery_1d.rst')
    return gallery


def make_2d():
    gallery = Gallery("Gallery of 2d Clawpack applications")
    plotdir = '_plots'

    #----------------------------------------------
    gsec = gallery.new_section('2-dimensional advection')
    #----------------------------------------------
    appdir = 'amrclaw/examples/advection_2d_square'
    description = """
        Advecting square with periodic boundary conditions."""
    images = ('frame0000fig0', 'frame0001fig0', 'frame0001fig2')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    #----------------------------------------------
    gsec = gallery.new_section('2-dimensional variable-coefficient advection')
    #----------------------------------------------
    appdir = 'amrclaw/examples/advection_2d_swirl'
    description = """
        Advection with a swirling flow field with AMR."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0008fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    appdir = 'classic/examples/advection_2d_annulus'
    description = """
        Advection in an annular region."""
    images = ('frame0000fig0', 'frame0002fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    appdir = 'amrclaw/examples/advection_2d_annulus'
    description = """
        Advection in an annular region with AMR."""
    images = ('frame0000fig0', 'frame0002fig0', 'frame0002fig2')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    #----------------------------------------------
    gsec = gallery.new_section('2-dimensional acoustics')
    #----------------------------------------------
    appdir = 'classic/examples/acoustics_2d_radial'
    description = """
        Expanding radial acoustic wave in a homogeneous medium."""
    images = ('frame0000fig0', 'frame0002fig0', 'frame0004fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'amrclaw/examples/acoustics_2d_radial'
    description = """
        Expanding radial acoustic wave in a homogeneous medium with AMR."""
    images = ('frame0000fig0', 'frame0002fig0', 'frame0004fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    #----------------------------------------------
    gsec = gallery.new_section("2-dimensional Burgers' equation")
    #----------------------------------------------
    appdir = 'amrclaw/examples/burgers_2d_square'
    description = """
        Burgers' equation :math:`q_t + 0.5(q^2)_x + 0.5(q^2)_y = 0`
        with square initial pulse and periodic boundary conditions."""
    images = ('frame0000fig1', 'frame0005fig1', 'frame0020fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    #----------------------------------------------
    gsec = gallery.new_section('2-dimensional Euler equations')
    #----------------------------------------------
    appdir = 'amrclaw/examples/euler_2d_quadrants'
    description = """
        Euler equations with piecewise constant data in quadrants."""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0004fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    gallery.create('gallery_2d.rst')
    return gallery

def make_geoclaw():
    gallery = Gallery("Gallery of GeoClaw applications")
    plotdir = '_plots'

    #----------------------------------------------
    gsec = gallery.new_section('Chile 2010 tsunami')
    #----------------------------------------------
    appdir = 'geoclaw/examples/tsunami/chile2010'
    description = """
        Simple model of the 2010 tsunami arising offshore Maule, Chile."""
    images = ('frame0004fig0', 'frame0008fig0', 'frame0012fig0','gauge32412fig300')
    gsec.new_item(appdir, plotdir, description, images)


    #----------------------------------------------
    gsec = gallery.new_section('Radially-symmetric tsuanami in parabolic bowl')
    #----------------------------------------------
    appdir = 'geoclaw/examples/tsunami/bowl-radial'
    description = """
        Sample code where solution should be radially symmetric."""
    images = ('frame0000fig0', 'frame0015fig0', 'frame0015fig10', 'gauge0004fig300')
    gsec.new_item(appdir, plotdir, description, images)


    #----------------------------------------------
    gsec = gallery.new_section('Sloshing water in parabolic bowl')
    #----------------------------------------------
    appdir = 'geoclaw/examples/tsunami/bowl-slosh'
    description = """
        Sample code with analytic solution."""
    images = ('frame0000fig0', 'frame0000fig1', 'frame0010fig0', 'frame0010fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    gallery.create('gallery_geoclaw.rst')
    return gallery



def make_fvmbook():
    gallery = Gallery("Gallery of `FVMHP book <http://www.clawpack.org/book>`_ applications")
    plotdir = '_plots'

    #----------------------------------------------
    gsec = gallery.new_section('Chapter 3: Linear Hyperbolic Equations')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap3/acousimple'
    description = """
        1D Acoustics simple waves"""
    images = ('frame0000fig1', 'frame0008fig1', 'frame0025fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 6: High-Resolution Methods')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap6/compareadv'
    description = """
        comparison of methods"""
    images = ('frame0000fig1', 'frame0005fig1', 'frame0010fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    appdir = 'apps/fvmbook/chap6/wavepacket'
    description = """
        wave packet with 1st order Godunov shown here"""
    images = ('frame0000fig1', 'frame0001fig1', 'frame0002fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------

    #----------------------------------------------
    gsec = gallery.new_section('Chapter 7: Boundary Conditions and Ghost Cells')
    #----------------------------------------------

    appdir = 'apps/fvmbook/chap7/advinflow'
    description = """
        1D Advection with inflow boundary conditions at left and outflow BCs at right"""
    images = ('frame0001fig0', 'frame0004fig0', 'frame0011fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    appdir = 'apps/fvmbook/chap7/acouinflow'
    description = """
        1D Acoustics with inflow boundary conditions at left and reflecting BCs at right"""
    images = ('frame0001fig0', 'frame0004fig0', 'frame0011fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap7/standing'
    description = """
        1D Acoustics with a standing wave solution"""
    images = ('frame0000fig0', 'frame0005fig0', 'frame0010fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
       
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 10: Other Approaches to High Resolution')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap10/tvb'
    description = """
        1D Advection with a TVB method"""
    images = ('frame0000fig0', 'frame0005fig0', 'frame0010fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 11: Nonlinear Scalar Conservation Laws')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap11/burgers'
    description = """
        Burgers' equation"""
    images = ('frame0000fig1', 'frame0004fig1', 'frame0010fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap11/congestion'
    description = """
        Traffic flow equation with density bulge"""
    images = ('frame0000fig1', 'frame0001fig1', 'frame0002fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap11/greenlight'
    description = """
        Traffic flow equation with expansion fan"""
    images = ('frame0000fig1', 'frame0005fig1', 'frame0010fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap11/redlight'
    description = """
        Traffic flow equation with shock wave behind red light"""
    images = ('frame0000fig1', 'frame0005fig1', 'frame0010fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 12: Finite Volume Methods for' \
           + ' Nonlinear Scalar Conservation Laws')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap12/efix'
    description = """
        Burgers' equation without entropy fix"""
    images = ('frame0000fig0', 'frame0001fig0', 'frame0002fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 13: Nonlinear Systems of Conservation Laws.')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap13/collide'
    description = """
        Colliding and merging shock waves in shallow water equations"""
    images = ('frame0000fig0', 'frame0003fig0', 'frame0011fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 16: Some Nonclassical Hyperbolic Problems')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap16/vctraffic'
    description = """
        Traffic equations with a spatially varying flux"""
    images = ('frame0000fig0', 'frame0004fig0', 'frame0008fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 17: Source Terms and Balance Laws')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap17/advdiff'
    description = """
        Advection-diffusion with implicit solver"""
    images = ('frame0000fig1', 'frame0002fig1', 'frame0004fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap17/onramp'
    description = """
        Traffic flow with an on-ramp"""
    images = ('frame0000fig0', 'frame0002fig0', 'frame0004fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
        
    #----------------------------------------------
    gsec = gallery.new_section('Chapter 20: Multidimensional Scalar Equations')
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap20/rotate'
    description = """
        2D Advection with a rotation of square and Gaussian"""
    images = ('frame0000fig0', 'frame0001fig0', 'frame0002fig0')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    appdir = 'apps/fvmbook/chap20/burgers'
    description = """
        2D Burgers' equation with square and Gaussian data"""
    images = ('frame0000fig1', 'frame0001fig1', 'frame0005fig1')
    gsec.new_item(appdir, plotdir, description, images)
    #----------------------------------------------
    
    gallery.create('gallery_fvmbook.rst')
    return gallery

def make_classic_amrclaw():
    gallery_1d = make_1d()
    gallery_2d = make_2d()

    # make gallery of everything:
    gallery_classic_amrclaw = Gallery(title="Gallery of Classic and AMRClaw applications")
    gallery_classic_amrclaw.sections = gallery_1d.sections + gallery_2d.sections 
    #gallery_classic_amrclaw.sections = gallery_2d.sections 
    
    gallery_classic_amrclaw.create('gallery_classic_amrclaw.rst')

if __name__ == "__main__":
    make_classic_amrclaw()
    make_geoclaw()
    make_fvmbook()
