import asyncio
import chromadb
import os
from dotenv import load_dotenv
import aiohttp
import aiosqlite
from pydantic import BaseModel,field_validator
from bs4 import BeautifulSoup

def integer_appender(split_space_list,only_int_list):
        for i in split_space_list:
                try :
                        only_int_list.append(float(i))
                except :
                                continue
        return only_int_list

def max_min_salary_finder(split_list,salary_num):
      
         only_int = []
         min_salary = None
         max_salary = None
         joined_list = "".join(split_list)
         symbol_split = joined_list.split("$")
         join_symbol = " ".join(symbol_split)
        
         if salary_num == 1 :
                 split_space_num = join_symbol.split(" ")
                 n_int_list = integer_appender(split_space_num,only_int)
                 min_salary = float(n_int_list[0])
                 max_salary = float(n_int_list[1])
         elif salary_num == 1000:
                 split_space_num = join_symbol.split("k")
                 checking_sti = split_space_num[0]
                 if "," in checking_sti:
                         updated_sti = checking_sti.replace(",",".")
                         updated_again_sti = updated_sti.replace(",","")
                         split_space_num[0] = updated_again_sti
                
                 n_int_list = integer_appender(split_space_num,only_int)
                 print(n_int_list)
                 min_salary = float(n_int_list[0]*1000)
                 max_salary = float(n_int_list[1]*1000)

        
         return min_salary,max_salary

def salary_num_decider(salary_type):
        salary_num = None
        if salary_type == "hourly":
                salary_num = 1
        elif salary_type == "monthly":
                salary_num = 1000
        return salary_num


async def salary_checker(salary,db,url):
        salary_type_ = None
        min_salary = None
        max_salary = None
        if salary is None:
                await db.execute("UPDATE job_info SET min_salary = ?,max_salary = ?,salary_type = ? WHERE url = ?",(min_salary,max_salary,salary_type_,url))
                await db.commit()
        else :
                if "–" in salary:
                          salary =  salary.replace("–","-") 
                splitted_salary = salary.split("-")
                length = len(splitted_salary)
                if length > 1 :
                        if "hour" in splitted_salary[1] or "hr" in splitted_salary[1] :
                                salary_type_ = "hourly"
                                splitted_hour = splitted_salary[1].split("/")
                                actaul_max_salary = splitted_hour[0]
                                splitted_salary[1] = actaul_max_salary
                                salary_num = salary_num_decider(salary_type_)
                                min_salary,max_salary = max_min_salary_finder(splitted_salary,salary_num)
                                await db.execute("UPDATE job_info SET min_salary = ?,max_salary = ?,salary_type = ? WHERE url = ?",(min_salary,max_salary,salary_type_,url))
                                await db.commit()

                        else :
                                salary_type_ = "monthly"
                                joined_salary = "".join(splitted_salary)
                                split_space_salary = joined_salary.split()
                                if "OTE" in split_space_salary:
                                                       split_space_salary.remove(split_space_salary[0])
                                                       splitted_salary = split_space_salary
                                
                                salary_num = salary_num_decider(salary_type_)
                                min_salary,max_salary = max_min_salary_finder(splitted_salary,salary_num)
                                await db.execute("UPDATE job_info SET min_salary = ?,max_salary = ?,salary_type = ? WHERE url = ?",(min_salary,max_salary,salary_type_,url))
                                await db.commit()
                else :
                                      single_int = []
                                      symbol_split = salary.split("$")
                                      joined_st = "".join(symbol_split)
                                      k_spilt = joined_st.split("K")
                                      n_int_list = integer_appender(k_spilt,single_int)
                                      await db.execute("UPDATE job_info SET min_salary = ? WHERE url = ?",(n_int_list[0]*1000,url))
                                      await db.commit()  
                                
                                                       
class ensuring_everydata(BaseModel):
        
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

headers = {"User-Agent": "Mozilla/5.0"}
async def exctracting_data(url,session):
                async with session.get(url,headers=headers) as response:
                        data = await response.json()
                        return data

async def url_passing(url,session,full_data):
            data =   await exctracting_data(url,session)
            for job in data["jobs"]:
                   title = job["title"]
                   job_time =  job["job_type"]
                   company_name = job["company_name"]
                   income = job["salary"]
                   public_date =  job["publication_date"]
                   location = job["candidate_required_location"]
                   url_1 = job["url"]
                   about = BeautifulSoup(job["description"],"html.parser").get_text()
                   full_data.append(ensuring_everydata(job_name=title,company=company_name,salary=income,publication_date=public_date,job_type=job_time,candidate_location=location,description=about,url=url_1))

async def all(): 
           client = chromadb.PersistentClient("job.db")       
           collection = client.get_or_create_collection("jobs")
           full_data = []
           async with aiosqlite.connect("jobdata.db") as db:
                        await db.execute("""
                                      CREATE TABLE IF NOT EXISTS job_info(
                                           job_name TEXT,
                                           company TEXT,
                                           salary_type TEXT,
                                           min_salary INTEGER,
                                           max_salary INTEGER,
                                           job_type TEXT,
                                           publication_date TEXT,
                                           candidate_location TEXT,
                                           url TEXT,
                                           UNIQUE (url)
                                               )
                                         """) 
                        await db.commit()
                        async with aiohttp.ClientSession() as session :
                                               await url_passing("https://remotive.com/api/remote-jobs",session,full_data)
                                               data = [(i.job_name,i.company,i.job_type,i.publication_date,i.candidate_location,i.url) for i in full_data]
                                               await db.executemany(
                                                       "INSERT OR IGNORE INTO job_info(job_name,company,job_type,publication_date,candidate_location,url) VALUES (?,?,?,?,?,?)",data
                                               )
                                               await db.commit()
                                               for i in full_data:
                                                      url = i.url
                                                      salary = i.salary
                                                      await salary_checker(salary,db,url)
                        all_data = await db.execute("SELECT * FROM job_info")
                        for i in await all_data.fetchall():
                                print(f"\n{i}")
asyncio.run(all())
