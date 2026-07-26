from bs4 import BeautifulSoup
from models import JobPosting

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
async def extracting_data(url,session):
                async with session.get(url,headers=headers) as response:
                        data = await response.json()
                        return data

async def url_passing(url,session,full_data):
            data =   await extracting_data(url,session)
            for job in data["jobs"]:
                   title = job["title"]
                   job_time =  job["job_type"]
                   company_name = job["company_name"]
                   income = job["salary"]
                   public_date =  job["publication_date"]
                   location = job["candidate_required_location"]
                   url_1 = job["url"]
                   about = BeautifulSoup(job["description"],"html.parser").get_text()
                   full_data.append(JobPosting(job_name=title,company=company_name,salary=income,publication_date=public_date,job_type=job_time,candidate_location=location,description=about,url=url_1))