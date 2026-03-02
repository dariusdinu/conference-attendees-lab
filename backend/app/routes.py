from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db_session
from .repository import AttendeeRepository
from .schemas import AttendeeCreate, AttendeeOut, AttendeeUpdatePut, AttendeeUpdatePatch
from .service import AttendeeService, ConflictError, NotFoundError

router = APIRouter(prefix="/users", tags=["users"])

_service = AttendeeService(AttendeeRepository())


@router.get("", response_model=list[AttendeeOut])
def list_users(session: Session = Depends(get_db_session)):
    return _service.list_attendees(session)


@router.get("/{user_id}", response_model=AttendeeOut)
def get_user(user_id: int, session: Session = Depends(get_db_session)):
    try:
        return _service.get_attendee(session, user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=AttendeeOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: AttendeeCreate, session: Session = Depends(get_db_session)):
    try:
        return _service.create_attendee(session, **payload.model_dump())
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.put("/{user_id}", response_model=AttendeeOut)
def replace_user(user_id: int, payload: AttendeeUpdatePut, session: Session = Depends(get_db_session)):
    try:
        return _service.replace_attendee(session, user_id, payload.model_dump())
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{user_id}", response_model=AttendeeOut)
def patch_user(user_id: int, payload: AttendeeUpdatePatch, session: Session = Depends(get_db_session)):
    try:
        data = payload.model_dump(exclude_unset=True)
        return _service.patch_attendee(session, user_id, data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_db_session)):
    try:
        _service.delete_attendee(session, user_id)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))