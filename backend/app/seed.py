import csv
from pathlib import Path
from sqlalchemy.orm import Session

from .models import Attendee


def seed_from_csv(session: Session, csv_path: Path):
    inserted = 0
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row["email"].strip().lower()
            exists = session.query(Attendee).filter(Attendee.email == email).first()
            if exists:
                continue

            attendee = Attendee(
                first_name=row["first_name"].strip(),
                last_name=row["last_name"].strip(),
                email=email,
                age=int(row["age"]),
                is_active=row["is_active"].strip().lower() == "true",
            )
            session.add(attendee)
            inserted += 1

    session.commit()
    return inserted