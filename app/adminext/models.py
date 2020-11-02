"""
Pydantic-models for parsing input data
"""
from typing import List
from pydantic import BaseModel,EmailStr,constr # pylint: disable=no-name-in-module

class CountryAssignment(BaseModel):
    name: constr(strip_whitespace=True,regex="^[a-zA-Z -]+$")
    assigned: bool

class InvitationRow(BaseModel):
    name: str
    position: str
    affiliation: str
    email: EmailStr 
    countries: List[str] 
