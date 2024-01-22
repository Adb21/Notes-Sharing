from pydantic import BaseModel,EmailStr, field_validator, validator, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import date,datetime

from typing import Optional


class StudentSchema(BaseModel):
    name: str
    enrollment: int
    year: date
    address: Optional[str] = None
    mobile: PhoneNumber
    dob: date
    email: EmailStr

    @field_validator('year')
    @classmethod
    def validate_year(cls, value):
        current_year = datetime.now().date().year
        validated_year = current_year - 4
        if validated_year > value.year:
            raise ValueError({'year': 'Students with less than 3 years are not allowed'})

class SeniorStudentSchema(StudentSchema):
    
    @validator('year', always=True, pre=True)
    @classmethod
    def validate_year(cls, value):
        current_year = datetime.now().date().year
        validated_year = current_year - 3
        if validated_year > value.year:
            raise ValueError({'year': 'Senior students with less than 4 years are not allowed'})

dob = datetime.now().date()  # Example date of birth
s1 = StudentSchema(
    name='student',
    enrollment=1,
    year=date(2020, 1, 1),
    mobile='+918511409726',
    dob=dob,
    email='adite@test.com'
)

s2 = SeniorStudentSchema(
    name='senior_student',
    enrollment=2,
    year=date(2019, 1, 1),
    mobile='+918511409727',
    dob=dob,
    email='senior@test.com'
)

# print(s1.model_dump())
# print(s2.model_dump())
