#!/bin/bash

# exit on any error
set -e


# Run unit tests
p-env/bin/nosetests --nocapture --nologcapture --with-xunit $@

# Run style checker
p-env/bin/flake8 libmt94x
