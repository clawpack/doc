"""
Runs code in each example directory to create sample results for webpage.

Sends output and errors to separate files to simplify looking for errors.
"""
import os
import sys


def list_examples(examples_dir=None):
    """
    Searches all subdirectories of examples_dir for examples and prints out a list.
    """
    import os

    if examples_dir is None:
        from clawpack import pyclaw
        examples_dir = pyclaw.__path__[0]+'/examples'

    examples_dir = os.path.abspath(examples_dir)
    current_dir = os.getcwd()
    os.chdir(examples_dir)

    dirlist = []
    applist = []

    # Traverse directories depth-first (topdown=False) to insure e.g. that code in
    # book/chap21/radialdam/1drad is run before code in book/chap21/radialdam
    for (dirpath, subdirs, files) in os.walk('.',topdown=False):
        # By convention we assume that all python scripts are applications
        # unless they are named 'setup.py' or 'setplot.py' or have 'test' in their name.
        files = os.listdir(os.path.abspath(dirpath))
        pyfiles=[f for f in files if f.split('.')[-1]=='py']
        appfiles=[f for f in pyfiles if f.split('.')[0] not in ('setup','setplot','__init__')]
        appfiles=[f for f in appfiles if 'test' not in f]
        appfiles=[f for f in appfiles if 'peano' not in dirpath]
        appfiles=[f for f in appfiles if 'compare_solvers' not in f]
        # Skip 3d for now because visclaw plotting is not set up for it
        appfiles=[file for file in appfiles if '3d' not in os.path.abspath(dirpath)]

        for filename in appfiles:
            dirlist.append(os.path.abspath(dirpath))
            applist.append(filename)

    os.chdir(current_dir)

    return applist, dirlist


def run_examples(examples_dir=None):
    """
    Runs all examples in subdirectories of examples_dir.
    """
    import os
    import subprocess

    current_dir = os.getcwd()

    app_list, dir_list = list_examples(examples_dir)
    for app, directory in zip(app_list,dir_list):
        print(directory+' '+app)
        app_name = app.split('.')[0]
        os.chdir(directory)
        process = subprocess.Popen(['python', app, 'outdir=_'+app_name])  # , stdout = subprocess.PIPE)
        stdout, stderr = process.communicate()

    os.chdir(current_dir)


def make_plots(examples_dir=None):
    if examples_dir is None:
        from clawpack import pyclaw
        examples_dir = pyclaw.__path__[0]+'/examples'

    examples_dir = os.path.abspath(examples_dir)
    current_dir = os.getcwd()

    print("Will run code and make plots in every subdirectory of ")
    print("    "+examples_dir)
    ans = raw_input("Ok? ")
    if ans.lower() not in ['y','yes']:
        print("Aborting.")
        sys.exit()

    fname_output = 'make_plots_output.txt'
    fout = open(fname_output, 'w')
    fout.write("ALL OUTPUT FROM RUNNING EXAMPLES\n\n")

    fname_errors = 'make_plots_errors.txt'
    ferr = open(fname_errors, 'w')
    ferr.write("ALL ERRORS FROM RUNNING EXAMPLES\n\n")

    os.chdir(examples_dir)

    goodlist_run = []
    badlist_run = []

    app_list, dir_list = list_examples(examples_dir)
    import subprocess
    for appfile, directory in zip(app_list,dir_list):
        print('Running '+directory, appfile)

        fout.write("\n=============================================\n")
        fout.write(directory)
        fout.write("\n=============================================\n")
        ferr.write("\n=============================================\n")
        ferr.write(directory)
        ferr.write("\n=============================================\n")

        # flush I/O buffers:
        fout.flush()
        ferr.flush()

        os.chdir(directory)
        job = subprocess.Popen(['python','./'+appfile,'htmlplot=True'], stdout=fout, stderr=ferr)
        return_code = job.wait()
        if return_code == 0:
            print("   Successful run")
            goodlist_run.append(directory)
        else:
            print("   *** Run errors encountered: see "+fname_errors)
            badlist_run.append(directory)
        app_name = appfile.split('.')[0]
        job = subprocess.Popen(['mv', '_plots', '_plots_'+app_name])

    if len(goodlist_run)>0:
        print(' ')
        print('Ran PyClaw and created output and plots in directories:')
        for d in goodlist_run:
            print('   '+d)
        print(' ')

    if len(badlist_run)>0:
        print('Run or plot errors encountered in the following directories:')
        for d in badlist_run:
            print('   '+d)
        print(' ')
    else:
        print('All examples ran and plotted successfully.')

    fout.close()
    ferr.close()
    print('For all output see '+fname_output)
    print('For all errors see '+fname_errors)

    os.chdir(current_dir)


if __name__=='__main__':
    if len(sys.argv)>1:
        print(sys.argv)
        make_plots(sys.argv[1])
    else:
        make_plots()
