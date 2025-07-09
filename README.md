
# Unifield POC18

## Installation

Python 3.12.x recommended

    $ git clone --recurse-submodules ssh://git@github.com:TeMPO-Consulting/poc18.git
    $ cd poc18
    $ python3 -m venv venv
    $ source ./venv/bin/activate
    $ cd odoo
    $ pip install -r requirements.txt

## Utils

The utils folder contains an openERP module which can be installed on Unifield to generate field definitions for 
existing models for the new Odoo syntax.