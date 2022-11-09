from .session import MagisterSession

__all__ = [
    "MagisterSession",
]


# def get_grades(session: MagisterSession):
#     url = f"https://{session.school}.magister.net/api/personen/{session.id}/cijfers/laatste?top=25&skip=0"
#     r = requests.get(url, headers=header(session.school, session.token), timeout=5)
#     return r.json()
