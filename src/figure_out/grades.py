from dataclasses import dataclass

from ..magister import MagisterSession
from ..magister.data import *

@dataclass
class Grade:
    date: str
    grade: str

def get_grades(session: MagisterSession) -> Dict[str, List[Grade]]:
    raw_grades = session.get_grades()
    grades = {}

    for g in raw_grades:
        # filter out grades that aren't actual
        # grades (such as averages)
        if not g["CijferId"]: continue
        if g["CijferKolom"]["KolomSoort"] != 1: continue

        match g["CijferStr"].replace(",", "."):
            case "G": actual_grade = "8"
            case "V": actual_grade = "6"
            case "O": actual_grade = "4"
            case num: actual_grade = num

        subject = g["Vak"]["Afkorting"]
        if not subject in grades.keys():
            grades[subject] = []

        grades[subject].append(Grade(
            g["DatumIngevoerd"].split("T", 1)[0],
            actual_grade
        ))

    return grades

def averages(session: MagisterSession) -> Dict[str, List[Grade]]:
    # TODO: include grade weight
    # TODO: incremented average rather
    #       than the grades themselves

    return get_grades(session)