import os

import pandas as pd

FOLDER = os.path.dirname(os.path.abspath(__file__))
ALARM_SCHEMA_PATH = os.path.join(FOLDER, "alarms.csv")


def _load_alarm_schema(path=ALARM_SCHEMA_PATH):
    """Load the alarm schema."""
    df = pd.read_csv(path, sep=";")
    df = df[["alarm", "name", "type"]]

    lst = df.to_dict(orient="records")

    alarms = {}
    for row in lst:
        try:
            alarms[row["alarm"]][row["name"]] = row["type"]
        except KeyError:
            alarms[row["alarm"]] = {}
            alarms[row["alarm"]][row["name"]] = row["type"]

    return alarms
