
First make sure `amrclaw` is checked out to the master branch,

```
    cd $CLAW/amrclaw
    git checkout master
    git pull
```

Make html files via:

```
    doxygen doxygen.conf
```

Then move to the web via:

```
    source rsync_clawpack.github.sh
```
