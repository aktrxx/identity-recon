from typing import Optional, List
from pydantic import BaseModel

class IdentifyRequest(BaseModel):
    email: Optional[str]
    phoneNumber: Optional[str]

class ContactResponse(BaseModel):
    primaryContatctId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

class IdentifyResponse(BaseModel):
    contact: ContactResponse
