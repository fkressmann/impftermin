from enum import Enum

from models.Timeslot import Timeslot

class Vaccination(Enum):
    Erstimpfung = "1"
    Zweitimpfung = "2"
    Boosterimpfung = "3"

class Age(Enum):
    unter30 = "<30"
    über30 = ">=30"


class Reservation:
    def __init__(self, request):
        self.name = request.get("name")
        self.email = request.get("email") if request.get("email") else None
        self.timeslot = Timeslot.query.get(request.get("timeslot"))
        try:
            self.vaccination = Vaccination(request.get("vaccination")).name
            self.age = Age(request.get("age")).name
        except ValueError as e:
            print(e)
            self.vaccination = None
            self.age = None

    def is_valid_external_request(self):
        return self.name is not None and \
               self.email is not None and \
               self.timeslot is not None and \
               self.vaccination is not None and \
               self.age is not None

    def is_valid_admin_request (self):
        return self.name is not None and \
               self.timeslot is not None and \
               self.vaccination is not None and \
               self.age is not None
