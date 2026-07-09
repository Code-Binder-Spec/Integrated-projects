import asyncio
import chromadb
import json
import os
from groq import Groq
from dotenv import load_dotenv
import aiohttp
import aiosqlite
from pydantic import BaseModel,field_validator
from bs4 import BeautifulSoup

def non_purifier(dictionary):
    
        remove_list = []
        true_list = []
        for i in dictionary.keys():
                if dictionary[i] == None:
                           remove_list.append(i)
                else :
                           true_list.append(i)
        for rem in remove_list:
                del dictionary[rem]
        
        return true_list

class score_board:
        def __init__(self,score,data):
                self.data = data
                self.score = score

        def url_initializer(self,url):
                 self.url = url

        def keyname_inititalizer(self,keyname):
                  self.keyname = keyname
 
        def db_initializer(self,db):
                self.db = db
      
        async def database_initialization(self):
                 if self.keyname in ["company","salary_type","min_salary","max_salary","job_type","location"]: 
                                   self.value_of_data = await self.db.execute(f"SELECT {self.keyname} FROM job_info WHERE url = ?",(self.url,))
                                   self.real_data = await self.value_of_data.fetchone()
                                   self.actual_data = self.real_data[0]
      
        def company_handler(self):
                if self.actual_data is None:
                         pass
                elif self.data[self.keyname].lower() == self.actual_data.lower():
                        self.score += 1
                return self.score
        
        def salary_type_handler(self):
                if self.actual_data is None:
                         pass
                elif self.data[self.keyname].lower() == self.actual_data.lower():
                        self.score += 1
                return self.score
        
        def min_salary_handler(self):
                if self.actual_data is None:
                         pass
                elif self.data[self.keyname] >= self.actual_data:
                        self.score += 1
                return self.score
   
        def max_salary_handler(self):
                if self.actual_data is None:
                         pass
                elif self.data[self.keyname] >=  self.actual_data:
                         self.score += 1
                return self.score
        
        def job_type_handler(self):
                if self.actual_data is None:
                         pass
                elif self.data[self.keyname] == self.actual_data:
                        self.score += 1
                return self.score
        
        def location_handler(self):
                if self.actual_data is None:
                         pass
                elif self.data[self.keyname].lower() == self.actual_data:
                         self.score += 1
                return self.score

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
                                           description TEXT,
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
                                               data = [(i.job_name,i.company,i.job_type,i.publication_date,i.candidate_location,i.url,i.description) for i in full_data]
                                               await db.executemany(
                                                       "INSERT OR IGNORE INTO job_info(job_name,company,job_type,publication_date,candidate_location,url,description) VALUES (?,?,?,?,?,?,?)",data
                                               )
                                               await db.commit()
                                               for i in full_data:
                                                      url = i.url
                                                      salary = i.salary
                                                      await salary_checker(salary,db,url)
                        metadata_dup = []
                        for c in full_data:
                                metadata_dup.append({f"url" : c.url})
                        print(metadata_dup)
                        if collection.count() == 0:
                                collection.add(
                                        documents=[i.job_name + "-" + i.description for  i in full_data],
                                        ids=[f"{i}" for i in range(1,len(full_data)+1)],
                                        metadatas=metadata_dup,
                                )
                        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                        print("\ntype stop in query to stop\n")
                        while True :
                                query = str(input("YOU : "))

                                if "stop" in query:
                                        break

                                message_1 = groq_client.chat.completions.create(
                                                model="llama-3.3-70b-versatile",
                                                max_tokens=1024,
                                                messages=[
                                                        {"role":"system","content":f"instructions : You are a job search assistant. Extract structured filters from the user's query and return ONLY a JSON object with exactly these keys: vector_search (the job role or skills mentioned, or null), company (company name if mentioned, or null), salary_type (only set to hourly or monthly if the user explicitly mentions it, otherwise null), min_salary (minimum salary as a number if mentioned, or null), max_salary (maximum salary as a number if mentioned, or null), job_type (map full-time or full time to full_time, part-time to part_time, contract to contract, freelance to freelance, or null if not mentioned), candidate_location (location if mentioned, or null). Return ONLY valid JSON. Do not wrap in markdown code fences or backticks. No explanation, no extra text.\n\nquery : {query}"}
                                                ]

                                )
                                print(message_1.choices[0].message.content)
                                dict_of_things = json.loads(message_1.choices[0].message.content) 
                                vector_content = dict_of_things["vector_search"]
                                if vector_content is None:
                                        vector_content = "job"
                                del dict_of_things["vector_search"]
                                true_list = non_purifier(dict_of_things)
                                result = collection.query(
                                        query_texts=[vector_content],
                                        n_results=3,
                                )
                                chunk =  result["documents"][0]
                                metadata = result["metadatas"][0]
                                metadata_list = []
                                for i in metadata:
                                               metadata_list.append(i["url"])
                                score_list = []
                                score = 0
                                board = score_board(score,dict_of_things)
                                board.db_initializer(db)
                                for url in metadata_list:
                                        board.url_initializer(url)
                                        for keyname in true_list:
                                                        board.keyname_inititalizer(keyname)
                                                        await board.database_initialization()
                                                        if keyname == "company":
                                                               score = board.company_handler()
                                                        elif keyname == "salary_type":
                                                                score = board.salary_type_handler()
                                                        elif keyname == "job_type":
                                                                score = board.job_type_handler()
                                                        elif keyname == "min_salary":
                                                                score = board.min_salary_handler()
                                                        elif keyname == "max_salary":
                                                                score = board.max_salary_handler()
                                                        elif keyname == "candidate_location":
                                                                score = board.location_handler()
                                                        else :
                                                                continue
                                        score_list.append(score)
                                print(score_list)
                                num = 0
                                position = 0
                                for i in range(3):
                                        if score_list[i] > num:
                                                num = score_list[i]
                                                position = i
                                        else:
                                                continue
                                real_chunk = collection.query(
                                        query_texts=[query],
                                        where={"url":metadata_list[position]},
                                        n_results=1
                                )
                                honest_chunk = real_chunk["documents"][0]
                                message_2  = groq_client.chat.completions.create(
                                        model="llama-3.3-70b-versatile",
                                        max_tokens=1024,
                                        messages=[
                                                {"role":"user","content":f"context : {honest_chunk}\n\ninstructions : Answer only from the context properly.if the answer is not in context please address it properly too.Begin the answering by 'The closest match of your search is' No need to compare query and context . Just answer the query based on context thats all.if user didnt say any questions force them to say it until they say anything about job. \n\nQuestion : {query}"}
                                        ]
                                )
                                print(f"AI : {message_2.choices[0].message.content}")
asyncio.run(all())
