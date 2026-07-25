
from scraper import url_passing
from salary import salary_checker


def deciding_position(conv_list,score_list):
      num = 0
      if len(conv_list) > 1:
             for i in range(len(score_list)):
                             if score_list[i] > num:
                                        num = score_list[i]
                                        position = i
                             else:
                                        continue
      else :
                     position  = 0

      return position

def acting_according_to_count(count,collection,full_data,metadata_dup):
        if count == 0:
                          collection.add(
                                        documents=[i.job_name + "-" + i.description for  i in full_data],
                                        ids=[f"{i}" for i in range(1,len(full_data)+1)],
                                        metadatas=metadata_dup,
                                )

async def url_passing_full_data_getting(session,full_data,db):
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

async def table_creation(db):
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


def appending_function(iterable_variable,appending_lis,variable_name : str =None):
        if variable_name.lower() ==  "metadata_dup":
                for i in iterable_variable:
                        appending_lis.append({f"url" : i.url})
        elif variable_name.lower() == "metadata_list":
                for i in iterable_variable:
                        appending_lis.append(i["url"])
        else :
                for i in iterable_variable:
                        appending_lis.append(i)

def ai_reply(client,prompt):
        reply = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[
                           {"role":"system","content":f"instructions : {prompt}"}
                                                                ]
        )
        return reply.choices[0].message.content



                
        