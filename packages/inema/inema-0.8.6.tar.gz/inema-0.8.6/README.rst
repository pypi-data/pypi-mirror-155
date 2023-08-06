python-inema
============

This is a python module for interfacing the "Internetmarke" API provided
by the German postal company "Deutsche Post".  It implements V3 of this
API.  It also implements the new (2020) "Warenpost International API".

The Internetmarke API allows you to buy online franking for national and
international postal products like post cards and letters of all weight
classes and service classes (normal, registered, ...).

Internetmarke API
-----------------

In order to use the Internetmarke API (SOAP), you will need to be registered
with Deutsche Post for accessing the "1C4A Webservice".  You can request
related details from pcf-1click@deutschepost.de.  Upon registration, you
will receive your individual parameters PARTNER_ID, KEY and KEY_PHASE.

This module makes use of the fairly new "zeep" module for SOAP/WSDL.


Warenpost International API
---------------------------

In order to use the Warenpost International API (REST), you will need to
be separately registered with Deutsche Post for accessing that API.
Upon registration, you will have the following individual parameters,
which you must use when initializing the WarenpostInt() class:

- PARTNER_ID
- SCHLUESSEL_DPWN_PARTNER (same as KEY?)
- EKP
- KEY_PHASE


Portokasse
----------

Furthermore, for actual payment of purchases made via both APIs, you
will need the user name (email address) and password to a "Portokasse"
account.


Authors / History
-----------------

python-inema was originally developed by Harald Welte <hwelte@sysmocom.de>
for internal use at his company sysmocom, in order to provide franking
from the Odoo based logistics system.  Like most other software at sysmocom,
it was released as open source software under a strong network copyleft
license.

Shortly after the initial release, Georg Sauthoff <mail@georg.so> joined
the development and improved and extended the code im various ways.  He
also added the command-line ``frank.py`` tool.
