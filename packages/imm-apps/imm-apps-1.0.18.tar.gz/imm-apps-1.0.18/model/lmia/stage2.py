from datetime import date
from typing import Optional, List
from pydantic import BaseModel, root_validator
from model.common.commonmodel import CommonModel
from model.common.utils import checkRow


class Joboffer(BaseModel):
    has_probation: bool
    probation_duration: Optional[int]
    disability_insurance: bool
    dental_insurance: bool
    empolyer_provided_persion: bool
    extended_medical_insurance: bool
    extra_benefits: Optional[str]
    supervisor_name: str
    supervisor_title: str
    employer_rep: str
    employer_rep_title: str
    vacation_pay_weeks: int
    vacation_pay_percentage: float
    english_french: bool
    oral: Optional[str]
    writing: Optional[str]
    reason_for_no: Optional[str]
    other_language_required: bool
    reason_for_other: Optional[str]
    skill_experience_requirement: Optional[str]
    other_requirements: Optional[str]

    @root_validator
    def checkProbation(cls, values):
        has_probation = values.get("has_probation", None)
        probation_duration = values["probation_duration"]
        if has_probation and not probation_duration:
            raise ValueError(
                "Since has probation is true, but did not input probation duration"
            )
        return values

    @root_validator
    def checkLanguage(cls, values):
        english_french = values.get("english_french", None)
        oral = values.get("oral", None)
        writing = values.get("writing", None)
        reason_for_no = values.get("reason_for_no", None)
        if english_french and not oral or not writing:
            raise ValueError(
                "Since English or French is true, but did not input oral or/and writting language requirement"
            )
        if not english_french and not reason_for_no:
            raise ValueError(
                "Since there is no English or French requirement, but did not input the reason"
            )
        return values

    @root_validator
    def checkOtherLanguageReason(cls, values):
        other_language_required = values.get("other_language_required", None)
        reason_for_other = values.get("reason_for_other", None)
        if other_language_required and not reason_for_other:
            raise ValueError(
                "Since required other language in job offer sheet,but did not input the reason"
            )
        return values


class Employee_list(BaseModel):
    employee: Optional[str]
    job_title: Optional[str]
    wage: Optional[float]
    hours_per_week: Optional[float]
    immigration_status: Optional[str]
    employment_start_date: Optional[date]
    remark: Optional[str]

    @root_validator
    def checkCompletion(cls, values):
        all_fields = [
            "employee",
            "job_title",
            "wage",
            "hours_per_week",
            "immigration_status",
            "employment_start_date",
            "remark",
        ]
        required_fields = [
            "employee",
            "job_title",
            "wage",
            "hours_per_week",
            "immigration_status",
            "employment_start_date",
        ]
        checkRow(values, all_fields, required_fields)
        return values


class Lmi(BaseModel):
    laid_off_in_12: bool
    laid_off_canadians: Optional[int]
    laid_off_tfw: Optional[int]
    laid_off_reason: Optional[str]
    is_work_sharing: bool
    work_sharing_info: Optional[str]
    labour_dispute: bool
    labour_dispute_info: Optional[str]

    @root_validator
    def checkLayoff(cls, values):
        laid_off_in_12 = values.get("laid_off_in_12", None)
        laid_off_canadians = values.get("laid_off_canadians", None)
        laid_off_tfw = values.get("laid_off_tfw", None)
        laid_off_reason = values.get("laid_off_reason", None)
        if laid_off_in_12 and (
            not laid_off_canadians or not laid_off_tfw or not laid_off_reason
        ):
            raise ValueError(
                "Since there is laid of in past 12 months in info lmi sheet,but did not input how many Canadians and/or foreign workers, and/or reason of lay off."
            )
        return values

    @root_validator
    def checkWorkSharing(cls, values):
        is_work_sharing = values.get("is_work_sharing", None)
        work_sharing_info = values.get("work_sharing_info", None)
        if is_work_sharing and not work_sharing_info:
            raise ValueError(
                "Since there is work sharing in info lmi sheet,but did not input the details about it."
            )
        return values

    @root_validator
    def checkLabourDisput(cls, values):
        labour_dispute = values.get("labour_dispute", None)
        labour_dispute_info = values.get("labour_dispute_info", None)
        if labour_dispute and not labour_dispute_info:
            raise ValueError(
                "Since there is labour disput in info lmi sheet,but did not input the details about it."
            )
        return values


class LmiaAssess(CommonModel):
    # general: General
    joboffer: Joboffer
    employee_list: List[Employee_list]
    lmi: Lmi

    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self, excels=None, output_excel_file=None):
        if output_excel_file:
            excels = self.getExcels(["excel/er.xlsx", "excel/lmia.xlsx"])

        else:
            if excels is None and len(excels) == 0:
                raise ValueError(
                    "You must input excel file list as source data for validation"
                )
        # call parent class for validating
        super().__init__(excels, output_excel_file, globals())
