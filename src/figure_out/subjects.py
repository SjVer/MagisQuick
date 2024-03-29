from datetime import datetime as dt, timedelta
from dataclasses import dataclass

from ..magister import MagisterSession
from ..magister.data import *

DAYS_AHEAD = 70 # 4 weeks

# type alias
class AppsList(List[AppointmentData]): pass

@dataclass
class Subject:
    id: str
    name: str
    reason: str
    date: str

def find_next_schoolday(apps: AppsList) -> str:
    for app in apps:
        if len(app["Vakken"]):
            return app["Start"].split("T", 1)[0]
    return None

def find_apps_at_date(date: str, apps: AppsList) -> AppsList:
    found = []
    for app in apps:
        if app["Start"].startswith(date):
            found.append(app)
    return found

def find_tests(apps: AppsList) -> AppsList:
    found = []
    for app in apps:
        if app["InfoType"].is_test():
            found.append(app)
    return found

def upcoming_subjects(session: MagisterSession) -> List[Subject]:
    start = dt.today() + timedelta(days = 1)
    end = start + timedelta(days=DAYS_AHEAD)

    apps = session.get_appointments(start, end)

    next_day = find_next_schoolday(apps)
    if not next_day: return []

    test_apps = find_tests(apps)

    left_over_apps = [a for a in apps if a not in test_apps]
    next_day_apps = find_apps_at_date(next_day, left_over_apps)

    sorted_apps = sorted(
        test_apps + next_day_apps,
        key=lambda d: d["Start"]
    )

    subjects = []
    names = []
    for app in sorted_apps:
        if not app["Vakken"]: continue

        name = app["Vakken"][0]["Naam"]
        if not app["InfoType"] and name in names:
            # this is a normal lesson and there is
            # already another lesson of this subject 
            continue

        # filter out normal lessons
        # if app["InfoType"] == 0: continue

        dateparts = app["Start"].split("T", 1)[0].split("-")
        dateparts.reverse()
        date = "/".join(dateparts[:2])

        names.append(name)
        subjects.append(Subject(
            app["Id"],
            name,
            app["InfoType"].readable(),
            date
        ))

    return subjects

def todays_subjects(session: MagisterSession) -> List[Subject]:
    apps = sorted(
        session.get_appointments(dt.today(), dt.today()),
        key=lambda d: d["Start"]
    )

    subjects = []
    names = []
    for app in apps:
        if not app["Vakken"]: continue

        name = app["Vakken"][0]["Naam"]
        if not app["InfoType"] and name in names:
            # this is a normal lesson and there is
            # already another lesson of this subject 
            continue

        if app["LesuurVan"]:
            time = f"{app['LesuurVan']}e uur"
        else:
            [h, m, _] = app["Start"].split("T", 1)[1].split(":")
            time = f"{h}:{m}"

        names.append(name)
        subjects.append(Subject(
            app["Id"],
            name,
            app["InfoType"].readable(),
            time
        ))

    return subjects