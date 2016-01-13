# Raspi-dash
Dashboard for Raspberry Pi

## Steps
Install `python-dev` and `python-virtualenv`

    sudo apt-get install python-dev
    sudo apt-get install python-virtualenv

Set up the virtual environment for flask

    virtualenv flask

Install flask into the virtual environment

    flask/bin/pip install flask

Make directories

    mkdir -p app/static
    mkdir app/templates

