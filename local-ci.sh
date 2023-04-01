#!/bin/bash
apps="app tests"

if [ ${1:-n} != -t ]
then
    python -m black $(echo $apps)
    python -m isort $(echo $apps)
    # Just run black and isort at the moment
    # python -m flake8 $(echo $apps)
    # python -m mypy $(echo $apps)
    # python -m pylint $(echo $apps)
fi

python -m pytest --cov
