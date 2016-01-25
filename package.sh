#!/bin/sh

PROJECT=ginger-libmt94x
VERSIONFILE=_buildinfo.txt
SKIPLIST="--exclude=.git --exclude=*.sh  --exclude=*.tgz --exclude=p-env"

if [ -z "$1" ]
then
  SUFFIX=""
else
  SUFFIX="-$1"
fi

rm $PROJECT-*.tgz || true

VERSION=`cat version.txt`
GITCOMMIT=`git rev-parse --short HEAD`
GITBRANCH=`git rev-parse --abbrev-ref HEAD`
DATE=`date +%Y-%m-%d:%H:%M:%S`


echo "major_version=$VERSION" > $VERSIONFILE
echo "minor_version=$1" >> $VERSIONFILE
echo "git_hash=$GITCOMMIT" >> $VERSIONFILE
echo "git_branch=$GITBRANCH" >> $VERSIONFILE
echo "built=$DATE" >> $VERSIONFILE

echo tar cfz $PROJECT-$VERSION$SUFFIX.tgz . $SKIPLIST
tar cfz $PROJECT-$VERSION$SUFFIX.tgz . $SKIPLIST || true
