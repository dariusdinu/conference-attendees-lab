from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Attendee


class AttendeeRepository:
    def get_all(self, session: Session) -> list[Attendee]:
        return list(session.execute(select(Attendee).order_by(Attendee.id)).scalars().all())

    def get_by_id(self, session: Session, attendee_id: int) -> Attendee | None:
        return session.get(Attendee, attendee_id)

    def get_by_email(self, session: Session, email: str) -> Attendee | None:
        stmt = select(Attendee).where(Attendee.email == email)
        return session.execute(stmt).scalars().first()

    def create(self, session: Session, attendee: Attendee) -> Attendee:
        session.add(attendee)
        session.commit()
        session.refresh(attendee)
        return attendee

    def update(self, session, attendee):
        session.commit()
        session.refresh(attendee)
        return attendee

    def delete(self, session, attendee):
        session.delete(attendee)
        session.commit()