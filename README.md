# Raspi-dash
Dashboard for Raspberry Pi

Raspi-dash is a Python/Flask rewrite of Colin Waddell's [CurrantPi][1] project.

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

Run dashboard using `run.py`

    pi: ~/git/Raspi-dash$ ./run.py
    * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
    * Restarting with stat

  [1]: https://github.com/ColinWaddell/CurrantPi
