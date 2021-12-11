from models.Timeslot import Timeslot


class Reservation:
    def __init__(self, request):
        self.name = request.get("name")
        self.email = request.get("email")
        self.timeslot = Timeslot.query.get(request.get("timeslot"))
        self.valid = self.name is not None and self.email is not None and self.timeslot is not None

    def __str__(self) -> str:
        if self.valid:
            print(self.timeslot)
            return f"Reservation for {self.name} ({self.email}) for slot {str(self.timeslot)}"
        else:
            return f"Invalid reservation: {self.name} {self.email} {self.timeslot}"



