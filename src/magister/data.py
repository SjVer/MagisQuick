from typing import TypedDict, List, Dict

class AppInfoType(int):
    HUISWERK = 1
    PROEFWERK = 2
    SO = 4

    def is_test(self):
        return self == self.PROEFWERK or self == self.SO
    
    def readable(self):
        match self:
            case self.HUISWERK: return "huiswerk"
            case self.PROEFWERK: return "proefwerk"
            case self.SO: return "SO"
            case _: return "les"

class AppointmentData(TypedDict):
    Aantekeningen: dict # ?
    Afgerond: bool
    Bijlagen: list # ?
    Docenten: list # Docentencode: str, Naam: str
    DuurtHeleDag: bool
    Einde: str
    Id: int
    InfoType: AppInfoType
    LesuurTotMet: int
    LesuurVan: int
    Lokatie: str
    Omschrijving: str
    Start: str
    Vakken: list # Naam: str

class GradeData(TypedDict):
    CijferId: int
    CijferStr: str
    IsVoldoende: bool
    DatumIngevoerd: str
    TeltMee: bool
    Vak: dict

class RelatedGradeData(TypedDict):
    Cijfer: str
    Weegfactor: int

class PersonalMentorData(TypedDict):
    Achternaam: str
    Tussenvoegsel: str
    Voorletters: str
    Links: List[str]

class GroupData(TypedDict):
    Id: str
    Links: List[dict]

class CourseData(TypedDict):
    Id: int
    Group: GroupData