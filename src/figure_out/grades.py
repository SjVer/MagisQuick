from dataclasses import dataclass

from ..magister import MagisterSession
from ..magister.data import *

@dataclass
class Grade:
    date: str
    grade: float
    weight: int

def cijfer_str_to_float(cijfer_str) -> float:
    match cijfer_str.replace(",", "."):
        case "G": actual_grade = "8"
        case "V": actual_grade = "6"
        case "O": actual_grade = "4"
        case num: actual_grade = num
    
    return float(actual_grade)

def grades(session: MagisterSession) -> Dict[str, List[Grade]]:
    raw_grades = session.get_grades()
    grades = {}

    for g in raw_grades:
        # filter out grades that aren't actual
        # grades (such as averages)
        if (not g["CijferId"]) \
        or g["CijferKolom"]["KolomSoort"] != 1 \
        or g["CijferStr"] == "Inh":
            continue

        # sort them by subject
        subject = g["Vak"]["Afkorting"]
        if not subject in grades.keys():
            grades[subject] = []

        if "KolomInfo" in g.keys():
            weight = g["KolomInfo"]["Weging"]
        else:
            weight = None

        grades[subject].append(Grade(
            g["DatumIngevoerd"].split("T", 1)[0],
            cijfer_str_to_float(g["CijferStr"]),
            weight
        ))
    return grades

def averages(session: MagisterSession) -> Dict[str, Grade]:
    avs = {}

    # first sort by subject
    for s, gs in session.get_averages().items():
        total = 0
        count = 0

        # calculate average
        for g in gs:
            if g["Cijfer"] == "Inh": continue
            
            grade = cijfer_str_to_float(g["Cijfer"])
            total += grade * g["Weegfactor"]
            count += g["Weegfactor"]

        av = round(total / count, 1)
        avs[s] = Grade(None, av, count) 
    return avs 