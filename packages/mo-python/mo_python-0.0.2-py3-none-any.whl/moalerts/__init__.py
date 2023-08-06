"""
moalerts

A library for interacting with the MO Alerts database.

Basic usage:
   import moalerts

   moalerts.start(dbname='', user='', password='', host='', port='')
   moalerts.list_alerts()
   >>> [
   >>>   {...}
   >>> ]

   moalerts.add_alert(...)
"""

from .core import (
    add_alarm,
    add_alert,
    add_alerts_from_df,
    list_alarms,
    list_alerts,
    start,
)
