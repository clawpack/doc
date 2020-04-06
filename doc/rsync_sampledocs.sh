
# Use to sync up files in sampledocs for other developers to view

chmod -R og+rX _build
rsync -avz --delete _build/html/ \
  clawpack@homer.u.washington.edu:public_html/sampledocs/sphinx-multiversion/

