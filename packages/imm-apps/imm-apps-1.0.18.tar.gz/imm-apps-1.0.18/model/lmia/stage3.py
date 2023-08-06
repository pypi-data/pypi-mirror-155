from datetime import date
from typing import Optional,List
from pydantic import BaseModel
from model.common.commonmodel import CommonModel
import os


class General(BaseModel):
    legal_name:str
    operating_name:Optional[str]
    website:Optional[str]
    establish_date:date
    num_pnps:int
    num_pnps_approved:int
    num_pnps_in_process:int
    has_lmia_approved:bool
    when_lmia_approved:Optional[date]
    last_revenue:float
    last_profit:float
    before_last_revenue:float
    before_last_profit:float
    retained_earning:float
    has_jobbank_account:bool
    has_bc_employer_certificate:bool

    
class Employee_list(BaseModel):
    employee:str
    job_title:str
    wage:float
    hours_per_week:float
    immigration_status:str	
    employment_start_date:date
    remark:str

class Lmi(BaseModel):
    laid_off_in_12:bool
    laid_off_canadians:Optional[int]
    laid_off_tfw:Optional[int]
    laid_off_reason:Optional[str]
    is_work_sharing:bool
    work_sharing_info:Optional[str]
    labour_dispute:bool
    labour_dispute_info:Optional[str]
    
class LmiaAssess(CommonModel):
    general:General
    employee_list:List[Employee_list]
    lmi:Lmi
    
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self,excels=None,output_excel_file=None):
        if output_excel_file:
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            excels=self.getExcels(['excel/er.xlsx','excel/lmia.xlsx'])
        else:
            if excels is None and len(excels)==0:
                raise ValueError('You must input excel file list as source data for validation')
        # call parent class for validating
        super().__init__(excels,output_excel_file,globals())

