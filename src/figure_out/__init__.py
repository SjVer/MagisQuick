from datetime import datetime as dt

from ..magister import MagisterSession

__all__ = [
    "books",
]

def books(session: MagisterSession):
    start = dt.now()
    end = dt.now()

    apps = session.get_appointments(start, end)
    return [
        f"{', '.join([v['Naam'] for v in a['Vakken']])}"
        for a in apps
    ]