from .models import Attendee
from .repository import AttendeeRepository
from sqlalchemy.orm import Session


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class AttendeeService:
    def __init__(self, repo: AttendeeRepository):
        self.repo = repo

    def list_attendees(self, session: Session):
        return self.repo.get_all(session)

    def get_attendee(self, session: Session, attendee_id: int):
        attendee = self.repo.get_by_id(session, attendee_id)
        if not attendee:
            raise NotFoundError(f"Attendee {attendee_id} not found")
        return attendee

    def create_attendee(self, session: Session, *, first_name: str, last_name: str, email: str, age: int, is_active: bool):
        existing = self.repo.get_by_email(session, email)
        if existing:
            raise ConflictError("Email already exists")

        attendee = Attendee(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip().lower(),
            age=age,
            is_active=is_active,
        )
        return self.repo.create(session, attendee)

    def replace_attendee(self, session, attendee_id, data):
        attendee = self.repo.get_by_id(session, attendee_id)
        if not attendee:
            raise NotFoundError(f"Attendee {attendee_id} not found")

        new_email = data["email"].strip().lower()
        existing = self.repo.get_by_email(session, new_email)
        if existing and existing.id != attendee_id:
            raise ConflictError("Email already exists")

        attendee.first_name = data["first_name"].strip()
        attendee.last_name = data["last_name"].strip()
        attendee.email = new_email
        attendee.age = data["age"]
        attendee.is_active = data["is_active"]

        return self.repo.update(session, attendee)

    def patch_attendee(self, session, attendee_id, data):
        attendee = self.repo.get_by_id(session, attendee_id)
        if not attendee:
            raise NotFoundError(f"Attendee {attendee_id} not found")

        if "email" in data and data["email"] is not None:
            new_email = data["email"].strip().lower()
            existing = self.repo.get_by_email(session, new_email)
            if existing and existing.id != attendee_id:
                raise ConflictError("Email already exists")
            attendee.email = new_email

        if "first_name" in data and data["first_name"] is not None:
            attendee.first_name = data["first_name"].strip()

        if "last_name" in data and data["last_name"] is not None:
            attendee.last_name = data["last_name"].strip()

        if "age" in data and data["age"] is not None:
            attendee.age = data["age"]

        if "is_active" in data and data["is_active"] is not None:
            attendee.is_active = data["is_active"]

        return self.repo.update(session, attendee)

    def delete_attendee(self, session, attendee_id):
        attendee = self.repo.get_by_id(session, attendee_id)
        if not attendee:
            raise NotFoundError(f"Attendee {attendee_id} not found")

        self.repo.delete(session, attendee)