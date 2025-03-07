import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints
from podium import constants

from podium.db import tables
from pyairtable.formulas import match


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    # International phone number format, allowing empty string
    phone: Optional[Annotated[str, StringConstraints(pattern=r"(^$|^\+?[1-9]\d{1,14}$)")]] = ""
    street_1: str
    street_2: Optional[str] = ""
    city: str
    state: str
    # str but only allow digits
    zip_code: Annotated[str, StringConstraints()]
    # zip_code: Annotated[str, StringConstraints(pattern=r"^[\d|\s\w]*$")]
    # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    country: Annotated[str, StringConstraints(pattern=r"^[A-Z]{2}$")]
    # YYYY-MM-DD or unix time is probably the best
    # Airtable returns 2025-01-25 :)
    dob: datetime.date

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Convert dob to YYYY-MM-DD
        data["dob"] = self.dob.strftime("%Y-%m-%d")
        return data


class UserSignupPayload(UserBase): ...


class User(UserBase):
    id: Annotated[str, StringConstraints(pattern=constants.RECORD_REGEX)]
    votes: constants.MultiRecordField = []
    projects: constants.MultiRecordField = []
    owned_events: constants.MultiRecordField = []
    attending_events: constants.MultiRecordField = []
    referral: constants.MultiRecordField = []


class CurrentUser(BaseModel):
    email: str


# TODO: make this part of CurrentUser or something, since this is used way too much
def get_user_record_id_by_email(email: str) -> Optional[str]:
    users_table = tables["users"]
    # Use formula filtering to search by email
    # try:
    #     formula = match({'Email': email})
    #     records = users_table.all(formula=formula)
    #     return records[0]['id'] if records else None
    # except HTTPError as e:
    #     if '404' in str(e):  # Check specifically for 404 error
    #         return None
    #     raise  # Re-raise other HTTP errors
    formula = match({"email": email})
    records = users_table.all(formula=formula)
    return records[0]["id"] if records else None
