from dataclasses import dataclass

from ..magister import MagisterSession
from ..magister.data import *

@dataclass
class Grade:
    date: str
    grade: float
    weight: int

def grades(session: MagisterSession) -> Dict[str, List[Grade]]:
    # TODO: include grade weight

    raw_grades = session.get_grades()
    grades = {}

    for g in raw_grades:
        # filter out grades that aren't actual
        # grades (such as averages)
        if not g["CijferId"]: continue
        if g["CijferKolom"]["KolomSoort"] != 1: continue

        # map alphabetical grades to numerical ones
        match g["CijferStr"].replace(",", "."):
            case "G": actual_grade = "8"
            case "V": actual_grade = "6"
            case "O": actual_grade = "4"
            case num: actual_grade = num

        # sort them by subject
        subject = g["Vak"]["Afkorting"]
        if not subject in grades.keys():
            grades[subject] = []

        grades[subject].append(Grade(
            g["DatumIngevoerd"].split("T", 1)[0],
            float(actual_grade),
            1 # TODO
        ))
    return grades

def averages(session: MagisterSession) -> Dict[str, Grade]:
    avs = {}

    for s, gs in grades(session).items():
        total = 0
        count = 0

        # calculate average
        for g in gs:
            total += g.grade * g.weight
            count += g.weight

        avs[s] = Grade(None, total, count) 
    return avs 