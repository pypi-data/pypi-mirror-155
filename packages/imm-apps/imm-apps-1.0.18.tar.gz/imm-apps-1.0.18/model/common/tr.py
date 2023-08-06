from dataclasses import dataclass
from datetime import date
from email.errors import ObsoleteHeaderDefect
from syslog import LOG_MAIL
from pydantic import BaseModel, root_validator, validator
from typing import Optional, List
from model.common.address import Address

# 1. start date must be greater than today
# 2. end date must be greater than start date
class DurationModel(BaseModel):
    duration_from: date
    duration_to: date

    @validator("duration_to")
    def endDateBigger(cls, duration_to, values):
        duration_from = values.get("duration_from")
        the_date = duration_to or date.today()
        if (the_date - duration_from).days <= 0:
            raise ValueError(
                f"End date {the_date} is earlier than from date {duration_from} for the work period"
            )
        return duration_to

    @validator("duration_from")
    def checkStartDate(cls, v):
        if (v - date.today()).days <= 0:
            raise ValueError("The start date of work must be greater than today")
        return v


class TrCase(BaseModel):
    service_in: str
    application_purpose: Optional[str]  # 5257需要，1294 5 不需要
    same_as_cor: bool
    applying_country: Optional[str]
    applying_status: Optional[str]
    applying_start_date: Optional[date]
    applying_end_date: Optional[date]
    consent_of_info_release: bool
    submission_date: Optional[date]


class TrCaseIn(BaseModel):
    service_in: str
    application_purpose: Optional[str]  # TODO: consider
    original_entry_date: date
    original_entry_place: str
    original_purpose: str
    original_other_reason: Optional[str]
    most_recent_entry_date: date
    most_recent_entry_place: str
    doc_number: Optional[str]
    consent_of_info_release: bool
    submission_date: Optional[date]


class Visa(DurationModel):
    visit_purpose: str
    funds_available: int
    name1: Optional[str]
    relationship1: Optional[str]
    address1: Optional[str]
    name2: Optional[str]
    relationship2: Optional[str]
    address2: Optional[str]


class Sp(DurationModel):
    school_name: str
    study_level: str
    study_field: str
    province: str
    city: str
    address: str
    dli: str
    student_id: str
    tuition_cost: Optional[str]
    room_cost: Optional[str]
    other_cost: Optional[str]
    fund_available: str
    paid_person: str
    other: Optional[str]


class Wp(DurationModel):
    work_permit_type: str
    other_explain: Optional[str]
    employer_name: Optional[str]
    employer_address: Optional[str]
    work_province: Optional[str]
    work_city: Optional[str]
    work_address: Optional[str]
    job_title: Optional[str]
    brief_duties: Optional[str]
    lmia_num_or_offer_num: Optional[str]
    # pnp_certificated: bool
    caq_number: Optional[str]
    expiry_date: Optional[date]

    @root_validator
    def checkLMIA_OfferNum(cls, values):
        work_permit_type = values.get("work_permit_type")
        lmia_num_or_offer_num = values.get("lmia_num_or_offer_num")
        if (
            work_permit_type == "Labour Market Impact Assessment Stream"
            and not lmia_num_or_offer_num
        ):
            raise ValueError(
                "Since the work permit type is LMIA stream, LMIA number is required"
            )
        if (
            work_permit_type
            in [
                "Exemption from Labour Market Impact Assessment",
                "Live-in Caregiver Program",
                "Start-up Business Class",
            ]
            and not lmia_num_or_offer_num
        ):
            raise ValueError(
                "Since you are applying employer specific work permit, so the number of Employer portal offer of employment is required"
            )

        return values


class VrInCanada(DurationModel):
    application_purpose: str
    visit_purpose: str
    other_explain: Optional[str]
    funds_available: int
    paid_person: str
    other: Optional[str]
    name1: Optional[str]
    relationship1: Optional[str]
    address1: Optional[str]
    name2: Optional[str]
    relationship2: Optional[str]
    address2: Optional[str]


class SpInCanada(DurationModel):
    application_purpose: str
    apply_work_permit: bool
    work_permit_type: Optional[str]
    caq_number: Optional[str]
    expiry_date: Optional[date]
    school_name: str
    study_level: str
    study_field: str
    province: str
    city: str
    address: str
    dli: str
    student_id: str
    tuition_cost: Optional[str]
    room_cost: Optional[str]
    other_cost: Optional[str]
    fund_available: str
    paid_person: str
    other: Optional[str]


class WpInCanada(DurationModel):
    application_purpose: str
    caq_number: Optional[str]
    expiry_date: Optional[date]
    work_permit_type: str
    employer_name: Optional[str]
    employer_address: Optional[str]
    work_province: Optional[str]
    work_city: Optional[str]
    work_address: Optional[str]
    job_title: Optional[str]
    brief_duties: Optional[str]
    lmia_num_or_offer_num: Optional[str]
    pnp_certificated: bool

    @root_validator
    def checkLMIA_OfferNum(cls, values):
        work_permit_type = values.get("work_permit_type")
        lmia_num_or_offer_num = values.get("lmia_num_or_offer_num")
        if (
            work_permit_type == "Labour Market Impact Assessment Stream"
            and not lmia_num_or_offer_num
        ):
            raise ValueError(
                "Since the work permit type is LMIA stream, LMIA number is required"
            )
        if (
            work_permit_type
            in [
                "Exemption from Labour Market Impact Assessment",
                "Live-in Caregiver Program",
                "Start-up Business Class",
            ]
            and not lmia_num_or_offer_num
        ):
            raise ValueError(
                "Since you are applying employer specific work permit, so the number of Employer portal offer of employment is required"
            )

        return values


class TrBackground(BaseModel):
    q1a: bool
    q1b: bool
    q1c: Optional[str]
    q2a: bool
    q2b: bool
    q2c: bool
    q2d: Optional[str]
    q3a: bool
    q3b: Optional[str]
    q4a: bool
    q4b: Optional[str]
    q5: bool
    q6: bool
