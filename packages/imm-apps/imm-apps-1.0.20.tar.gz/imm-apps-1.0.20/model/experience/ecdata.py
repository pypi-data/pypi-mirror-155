from pydantic import BaseModel, validator, EmailStr, root_validator
from datetime import date
from model.common.utils import makeList, Duration
from model.common.person import Person
from model.common.id import ID, IDs
from typing import Optional, List
from model.common.employmentbase import EmploymentBase
from model.common.utils import checkRow


class Employment(EmploymentBase):
    department: Optional[str]
    duties: list
    company_brief: str
    fullname_of_certificate_provider: Optional[str]
    position_of_certificate_provider: Optional[str]
    department_of_certificate_provider: Optional[str]
    phone_of_certificate_provider: Optional[str]
    email_of_certificate_provider: Optional[EmailStr]
    employment_certificate: bool

    _normalize_duties = validator("duties", allow_reuse=True, pre=True)(makeList)

    @root_validator
    def checkCompletion(cls, values):
        all_fields = [
            "job_title",
            "noc_code",
            "weekly_hours",
            "company",
            "city",
            "province",
            "country",
            "department",
            "duties",
            "company_brief",
            "fullname_of_certificate_provider",
            "position_of_certificate_provider",
            "department_of_certificate_provider",
            "phone_of_certificate_provider",
            "email_of_certificate_provider",
            "employment_certificate",
        ]
        required_fields = [
            "job_title",
            "noc_code",
            "weekly_hours",
            "company",
            "city",
            "province",
            "country",
            "department",
            "duties",
            "company_brief",
            "fullname_of_certificate_provider",
            "position_of_certificate_provider",
            "department_of_certificate_provider",
            "phone_of_certificate_provider",
            "email_of_certificate_provider",
            "employment_certificate",
        ]

        checkRow(values, all_fields, required_fields)

        return values
