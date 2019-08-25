#!/bin/bash

set -e

BASE_DIR=$(realpath $(dirname $0))

DIST_DIR=$(realpath $BASE_DIR/dist)

VERSION=1.0

echo $BASE_DIR

# Remove existing directory tree and create fresh one.
\rm -rf $DIST_DIR/rpmbuild
mkdir -p $DIST_DIR/rpmbuild/SOURCES




# Create tar of source directory
tar czvf $DIST_DIR/rpmbuild/SOURCES/thumber-$VERSION.tar.gz -C $BASE_DIR/ thumber

# Generate RPM
rpmbuild -bb --define "version $VERSION" --define "_topdir $DIST_DIR/rpmbuild" $BASE_DIR/thumber.spec
