pandorica-spksel
================

Web interface for the multi-room audio controller.
Created by [David Liu](http://iceboundflame.com).

Project details: <http://iceboundflame.com/projects/multi-room-audio-control-with-rpi>

This is a Python 2.7/Flask application using jQuery Mobile.

control.py uses the RPi.GPIO Python module to pulse the GPIOs. Each execution will change the relay state to match. For instance:

    sudo ./control.py            # Turn off all relays
    sudo ./control.py 0 2 3      # Turn on relays 0, 2, and 3
    sudo ./control.py 0 1 2 3 4  # Turn on all relays

spksel.py is the actual Flask web server. It serves the web interface, calling "sudo ./control.py" in order to turn rooms on and off.

This is designed to be run in a virtualenv, so unpack virtualenv and run ./setup to install the necessary packages.


# Configuration notes #

## Raspberry Pi pins used ##

    2   5V
    6   GND
    7   GPIO4
    11  GPIO17
    12  GPIO18
    13  GPIO27
    15  GPIO22
    16	GPIO23
    18  GPIO24
    22  GPIO25
    24  GPIO08
    26  GPIO07
    25  GND

To test the relay board, use control.py to make sure that all relays can click on and off. Adjust the PIN_MAP in control.py as necessary.


## spksel ##

Install nginx via apt and configure it to serve a uWSGI site on /.
Create spksel user, set up sudoers to allow "sudo control.py" without password.

Extract virtualenv, run ./setup in this repository to create "myenv" virtual environment and download Flask/Jinja2/other packages. Following deployment instructions at http://flaviusim.com/blog/Deploying-Flask-with-nginx-uWSGI-and-Supervisor/ :

    . myenv/bin/activate
    # After activating virtualenv:
    pip install uwsgi   # takes a while to build on RPi, ~15 min
    
    # Test:
    uwsgi -s /tmp/spksel.sock -w spksel:app -H /home/spksel/spksel/myenv --chmod-socket=666  --processes 4 --threads 2 --stats 127.0.0.1:9191

Set up supervisord to run uwsgi on bootup.


## LIRC & ShairPort ##

These features have been removed for the Lite version, the goal of which is only control the speaker selector. To my understanding, ShairPort is independent of the spksel application, and the intended target (Pi Zero W) doesn't have an onboard audio DAC anyway.
