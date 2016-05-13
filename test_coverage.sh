#!/bin/bash

# exit on any error
set -e


# Initialize virtualenv in p-env if not present
if [ ! -d "./p-env/" ]; then
    virtualenv p-env
fi

# Activate it
source ./p-env/bin/activate

# Install any missing runtime dependencies
TMP_DEPS=/tmp/temp_deps_${RANDOM}
pip freeze -l > ${TMP_DEPS}
if ! cmp ./dev-requirements.txt ${TMP_DEPS} > /dev/null 2>&1
then
  echo "Installing Python dependencies ..."
  cat ${TMP_DEPS}
  pip install -r ./dev-requirements.txt
fi

# Run tests with code coverage
coverage run --source=./ginger_libmt94x --branch ./p-env/bin/nosetests --nocapture --nologcapture --with-xunit $@
coverage report -m
coverage xml

# Perform PEP8, pyflakes and other checks
flake8 ginger_libmt94x
