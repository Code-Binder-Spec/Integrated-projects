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
                 print(n_int_list)
                 min_salary = float(n_int_list[0])
                 max_salary = float(n_int_list[1])
         elif salary_num == 1000:
                 if "k" in join_symbol:
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
                                      if "$" and "K" in salary:
                                                    single_int = []
                                                    symbol_split = salary.split("$")
                                                    joined_st = "".join(symbol_split)
                                                    k_spilt = joined_st.split("K")
                                                    n_int_list = integer_appender(k_spilt,single_int)
                                                    print(n_int_list)
                                                    await db.execute("UPDATE job_info SET min_salary = ? WHERE url = ?",(n_int_list[0]*1000,url))
                                                    await db.commit()  