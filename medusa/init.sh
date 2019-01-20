#! /usr/bin/env bash
###############################################################################
# This init script sets up the environment for running and developing this
# application/module. See the end of this script for more detailed information.

# Create the python virtual environment
python3 -m venv .venv

# Activate the new python virtual environment 
source .venv/bin/activate

# Upgrade the virtual environments setuptools and pip
# New virtual environments created with the 'venv' module always seem to come
# with a setuptools and a pip that are many versions back. These modules are
# probably on the list of good ones to always update to the latest version
# unless you have a very specific reason not to.
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools

# Install packages to support and enhance IDE operation
python3 -m pip install pylint

# Install project-specific python depdendencies
python3 -m pip install -r requirements.txt


###############################################################################
#
# Before you first run the app in any shell you will always need to activate
# the python virtual environment unless you plan to install all requirements
# globally or unless your IDE provides some other library loading/access
# mechanism etc. Most IDEs, when running this program for you,usually in a
# new, visible terminal window, will do the same thing as this command.
#### source .venv/bin/activate
#
# For development in an IDE, you will may need to configure the IDE to
# recognize and automatically activate the new python virtual environment,
# however many popular IDEs can automatically see and activate this environment
# in the .venv directory in which we create it, at the base of the project dir.
#
# Some requirements we intally are there to assist the operation of IDEs.
#
# This init.sh and this information is being developed using VS Code 1.30.2.
#

###############################################################################

##
#

