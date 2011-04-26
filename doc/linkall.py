
# Create soft links to all the other package-specific documentation.

import os,sys

repos_list = """clawutil classic amrclaw geoclaw pyclaw 
                riemann visclaw
                petclaw sharpclaw""".split()

for repos in repos_list:
    try:
        os.system("ln -sf ../../%s/doc %s_doc" % (repos,repos))
    except:
        print "*** Failed to link for repos = ",repos

os.system("ls -l *_doc")
