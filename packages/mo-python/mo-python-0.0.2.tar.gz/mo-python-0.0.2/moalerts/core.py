import os
from pprint import pprint

import pandas as pd
import psycopg2
from psycopg2.extras import Json

from . import helpers

DB_CONFIG = {}


VALID_ALARM_TYPES = [
    "AVVIK_TILBUD",
    "ENDRING_PRODPLAN",
    "INNSIDE",
    "TIPS",
    "TILBAKEHOLD",
    "INNTEKT_PROD",
    "TEST",
]


ALARM_PARAMETERS = helpers._load_alarm_schema()


SELECT_ALARMS_QUERY = "SELECT * FROM alarms;"


SELECT_ALERTS_QUERY = "SELECT * FROM alerts;"


INSERT_ALERT_QUERY = """
INSERT INTO alerts (organization, price_area, alarm, alert_data)
VALUES (%s, %s, %s, %s);
"""


INSERT_ALARM_QUERY = """
INSERT INTO alarms (id, name)
VALUES (%s, %s);
"""


ERROR_MISSING_CONNECTION = """\n\n\n
Could not connect.\n
Have you called `moalerts.start(...)` as described in the docs?\n
See `/docs/getting-started.md`.\n
"""


ERROR_INVALID_ALARM = """\n\n\n
Invalid alarm type: `%s`.\n
The `alarm` passed in must be one of the types:\n
%s \n
"""


def _check_db_config():
    """Check if user has setup the db parameters."""
    # print(DB_CONFIG)
    # try:
    #    x = DB_CONFIG['host'] + ''
    # except KeyError:
    #    raise ConnectionError(ERROR_MISSING_CONNECTION)
    pass


def _check_alarm_type(alarm):
    """Check if the alarm type is valid."""
    is_valid = alarm in VALID_ALARM_TYPES
    if not is_valid:
        raise TypeError(ERROR_INVALID_ALARM % (alarm, VALID_ALARM_TYPES))


def _extend_alert_data(alert_data, alarm):
    """Build the alert data dict.

    Combines the relevant schema in `ALARM_PARAMETERS`
    and the passed in alert_data to make an extended
    alert data dict.

    Any key that is missing from the passed in `alert_data`
    will be set to None.

    Usage:
      passed_in_alert_data = {'test': 'ok'}
      alert_data = _extend_alert_data(
          alert_data=passed_in_alert_data,
          alarm='TEST'
        )
      > {<BASE>, 'test': 'ok'}

    Input:
      alert_data (dict)
      alarm (str)

    Returns:
      extended_ (psycopg2._json.Json)
    """
    base = {key: None for key, value in ALARM_PARAMETERS[alarm].items()}
    alert_data_ = alert_data if alert_data else dict()
    extended = {**base, **alert_data_}
    extended_ = Json(extended)
    return extended_


def start(dbname="", user="", password="", host="localhost", port="5432"):
    """Setup the connection parameters.

    Must be called with valid arugments before the user can interact
    with the moalerts database.

    Usage:
      > start(
          'postgres', 'postgres', 'secret-password', 'localhost', '5432'
        )

    Input:
      NOT IN USE - username (str)
      dbname (str)
      user (str)
      password (str)
      host (str)
      port (str)

    Returns:
      None
    """
    global DB_CONFIG, VALID_ALARM_TYPES
    DB_CONFIG = {
        "dbname": dbname,
        "user": user,
        "password": password,
        "host": host,
        "port": port,
    }


def add_alerts_from_df(df, alarm):
    """Add one or more alerts to the database.

    Usage:
      > df = pd.DataFrame(...)
      > add_alerts_from_df(df, 'TILBAKEHOLD')

    Input:
      df (pandas.DataFrame)
      alarm (str)

    Returns:
      status (str)
    """
    alerts = df.to_dict(orient="records")

    for alert_data in alerts:
        # print(alert_data)
        try:
            organization = alert_data["OrganisasjonsNavn"]
        except KeyError:
            organization = None
        # price_area = alert_data['PrisOmraade_BK']
        add_alert(
            organization=organization,
            price_area="NO1",
            alarm=alarm,
            alert_data=alert_data,
        )


def add_alert(organization=None, price_area=None, alarm=None, alert_data=None):
    """Add a new alert to the database."""
    _check_db_config()
    _check_alarm_type(alarm)
    extended_alert_data = _extend_alert_data(alert_data, alarm)
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(
        INSERT_ALERT_QUERY, (organization, price_area, alarm, extended_alert_data)
    )
    cursor.close()
    connection.commit()
    connection.close()


def add_alarm(id=None, name=None):
    """Add a new alarm to the database."""
    _check_db_config()
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(INSERT_ALARM_QUERY, (id, name))
    cursor.close()
    connection.commit()
    connection.close()


def list_alerts():
    """Get a list of all the alerts."""
    _check_db_config()
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(SELECT_ALERTS_QUERY)
    alerts = cursor.fetchall()
    cursor.close()
    connection.close()
    return alerts


def list_alarms():
    """Get a list of the valid alarm types.

    Usage:
      list_alarms()
      > ['AVVIK_TILBUD', 'ENDRING_PRODPLAN', ...]

    Returns
      alarms (list)
    """
    _check_db_config()
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(SELECT_ALARMS_QUERY)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    alarms = [key for key, value in data]
    return alarms


def _status():
    """Print status of the current DB config.

    Example:
      _status()
      >>> {...}
    """
    pprint(DB_CONFIG)
