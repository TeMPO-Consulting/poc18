
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
existing models with the new Odoo syntax.

## Modules List

Default modules installed with a new Odoo database:  
* auth_signup
* auth_totp
* auth_totp_mail
* base
* base_import
* base_import_module
* base_install_request
* base_setup
* bus
* google_gmail
* html_editor
* iap
* iap_mail
* mail
* mail_bot
* partner_autocomplete
* phone_validation
* privacy_lookup
* sms
* snailmail
* uom
* web
* web_editor
* web_tour
* web_unsplash

Additional modules installed for the POC:  
* uom (Odoo Community)
* web_responsive (OCA)
* msf_partner (Custom)
* msf_product (Custom)
