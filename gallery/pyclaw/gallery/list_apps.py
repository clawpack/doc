

def list_examples(examples_dir=None):
    """
    Searches all subdirectories of examples_dir for examples and prints out a list.
    """
    import os

    if examples_dir is None:
        from clawpack import pyclaw
        examples_dir = '/'.join(pyclaw.__path__[0].split('/')[:-2])+'/pyclaw/examples/'

    examples_dir = os.path.abspath(examples_dir)
    print examples_dir

    current_dir = os.getcwd()

    os.chdir(examples_dir)
    
    # Traverse directories depth-first (topdown=False) to insure e.g. that code in
    # book/chap21/radialdam/1drad is run before code in book/chap21/radialdam
    
    dirlist = []
    applist = []

    for (dirpath, subdirs, files) in os.walk('.',topdown=False):
        #By convention we assume that all python scripts are applications
        #unless they are named 'setup.py' or 'setplot.py'.
        files = os.listdir(os.path.abspath(dirpath))
        pyfiles=[f for f in files if f.split('.')[-1]=='py']
        appfiles=[f for f in pyfiles if f.split('.')[0] not in ('setup','setplot','__init__')]
        appfiles=[f for f in appfiles if 'test' not in f]

        for filename in appfiles:
            dirlist.append(os.path.abspath(dirpath))
            applist.append(filename)

        #if appfiles!=[]:
        #    print os.path.abspath(dirpath)
        #    for appname in appfiles: print '     ',appname
           
    os.chdir(current_dir)

    return applist, dirlist
        
def run_examples(examples_dir = None):
    """
    Runs all examples in subdirectories of examples_dir.
    """
    import os
    import subprocess

    current_dir = os.getcwd()

    app_list, dir_list = list_examples(examples_dir)
    for app, directory in zip(app_list,dir_list):
        print directory, app
        os.chdir(directory)
        process = subprocess.Popen(['python',app])#, stdout = subprocess.PIPE)
        stdout, stderr = process.communicate()

    os.chdir(current_dir)

if __name__=='__main__':
    import sys
    list_examples(sys.argv[1:])
