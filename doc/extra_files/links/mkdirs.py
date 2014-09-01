
import os

dirs = """
an11
awr11
birs08
burgersadv
cise09
eswt
honshu2011
icerm-tw12-5-rcem
noaa-tsunami-benchmarks
nthmp-benchmarks
papers
radial-ocean-island
sharpclaw11
shockvacuum10
siamnews11
sphere
talks
tsunami-benchmarks
tutorials
wbfwave10
""".split()


index = open('index.html').read()

for dir in dirs:
    os.system('mkdir -p %s' % dir)
    dir_index = index.replace('links','links/%s' % dir)
    f = open('%s/index.html' % dir,'w')
    f.write(dir_index)
    f.close()

