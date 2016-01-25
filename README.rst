====================
libmt94x
====================

This library generates bank statements in MT940/MT942 format

Release versioning
==================

To make a release a git flow approach is used.

You need to:

* checkout and pull `develop`,
* checkout and pull `master`,
* execute `git flow release start x.x.x` ("x.x.x" = new version),
* apply release fixes/updates if needed,
* just before merging the release into master, in release branch execute `./bump-version.sh x.x.x` shell script and commit changes with message `chore(version): bumps versions to x.x.x`
* close release `git flow release finish x.x.x`
* push master,
* push tag created during release `git push origin x.x.x`
* push develop,
* check that deployment went well.
