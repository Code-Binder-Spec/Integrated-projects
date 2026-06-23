import asyncio
import aiohttp
import json
from pydantic import BaseModel,field_validator
from bs4 import BeautifulSoup


class ensuring_everydata(BaseModel):
        job_name : str
        company : str | None
        salary : str | None
        description : str | None
        job_type : str | None
        publication_date : str | None
        candidate_location : str | None
        @field_validator("salary","company","description","job_type","publication_date","candidate_location")
        @classmethod
        def checking_data_None(cls,v):
                      if v is None :
                                return None
                      if isinstance(v,str) and v.strip() == "":
                              return None
                      else :
                              return v



headers = {"User-Agent": "Mozilla/5.0"}
async def exctracting_data(url):
        async with aiohttp.ClientSession() as session:
                async with session.get(url,headers=headers) as response:
                        data = await response.json()
                        return data

async def url_passing(url,full_data):
            data =   await exctracting_data(url)
            for job in data["jobs"]:
                   title = job["title"]
                   job_time =  job["job_type"]
                   company_name = job["company_name"]
                   income = job["salary"]
                   public_date =  job["publication_date"]
                   location = job["candidate_required_location"]
                   about = BeautifulSoup(job["description"],"html.parser").get_text()
                   full_data.append(ensuring_everydata(job_name=title,company=company_name,salary=income,publication_date=public_date,job_type=job_time,candidate_location=location,description=about))

async def all():                
           full_data = []
           await url_passing("https://remotive.com/api/remote-jobs",full_data)
           print(full_data)

asyncio.run(all())
