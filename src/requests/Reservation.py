from models.Timeslot import Timeslot


class Reservation:
    def __init__(self, request):
        self.name = request.get("name")
        self.email = request.get("email")
        self.timeslot = Timeslot.query.get(request.get("timeslot"))

    def is_valid_external_request(self):
        return self.name is not None and self.email is not None and self.timeslot is not None

    def is_valid_admin_request (self):
        return self.name is not None and self.timeslot is not None


