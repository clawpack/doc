
# Use to sync up files on clawpack.org server:

chmod -R og+rX _build
rsync -avz --delete _build/html/ \
  clawpack@homer.u.washington.edu:public_html/users-5.x

