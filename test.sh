#!/bin/bash

if [ ! -d "./p-env/" ]; then
    virtualenv p-env
fi

source ./p-env/bin/activate

TMP_DEPS=/tmp/temp_deps_${RANDOM}
pip freeze -l > ${TMP_DEPS}
if ! cmp ./requirements.txt ${TMP_DEPS} > /dev/null 2>&1
then
  echo "Installing Python dependencies ..."
  cat ${TMP_DEPS}
  pip install -r ./requirements.txt
fi

pip install nose
pip install mock
pip install coverage
pip install flake8

# export all necessary environment variables (if any) for the tests there
export UAC_AWS_ACCESS_KEY_ID=aaa
export UAC_AWS_SECRET_ACCESS_KEY=bbb
export AWS_ACCESS_KEY_ID=aaa
export AWS_SECRET_ACCESS_KEY=bbb

# Run tests with code coverage. Note that running tests with coverage could be slow, so if
# you notice issues, create a separate command for running only the tests.
coverage run --source=./ginger --branch ./p-env/bin/nosetests --nocapture --nologcapture $@  --with-xunit
coverage report -m

# Performs PEP8, pyflakes and other checks
flake8 ginger --max-line-length=120 --ignore=E124,E128,E303,F403

# Coverage-less testing (not used anymore)
#nosetests --with-xunit --nologcapture --nocapture $@
