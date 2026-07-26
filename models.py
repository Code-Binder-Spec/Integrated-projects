
from pydantic import BaseModel, field_validator

class JobPosting(BaseModel):
        
        job_name : str
        company : str | None
        salary : str | None
        description : str | None
        job_type : str | None
        publication_date : str | None
        candidate_location : str | None
        url : str
      
        @field_validator("salary","company","description","job_type","publication_date","candidate_location")
        @classmethod
        def checking_data_None(cls,v):
                      if v is None :
                                return None
                      if isinstance(v,str) and v.strip() == "":
                              return None
                      else :
                              return v
