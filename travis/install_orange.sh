#!/usr/bin/env bash
git clone https://github.com/biolab/orange3
cd orange3
pip install -r requirements-core.txt
python setup.py develop
source .travis/install_pyqt.sh
cd $TRAVIS_BUILD_DIR
