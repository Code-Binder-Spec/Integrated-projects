import re

def setting_hour_yearly(salary):
        sal_type = None
        if "hour" in salary or "hr" in salary:
                  sal_type = "hourly"
        else:
                    sal_type = "yearly" 
        return sal_type

def checking_comma_exist(salary):
        spicy = salary
        thing_to_check = ","
        if thing_to_check in salary:
                spicy = salary.replace(thing_to_check,".")
        return spicy

def normalize_thousands_suffix(specific_salary):
               normalized_salary = specific_salary
               thing_to_check = ",000"
               if thing_to_check in specific_salary:
                         normalized_salary = specific_salary.replace(thing_to_check,"k")
               return normalized_salary

def float_maker_accurate_multiply(lis_name,num):
                 for i in range(len(lis_name)-1):
                         fl_version = float(lis_name[i])
                         lis_name[i] = fl_version*num


def float_converter(lis_var):
        if "yearly" in lis_var:
                             float_maker_accurate_multiply(lis_var,1000)
        else :
                             float_maker_accurate_multiply(lis_var,1)

        return lis_var

async def writing_to_db_both_min_max(db,url,data):
             if len(data) > 2:
                        await db.execute("UPDATE job_info SET min_salary = ? , max_salary = ? , salary_type = ? WHERE url = ?",(data[0],data[1],data[2],url))
                        await db.commit()
             else :
                        await db.execute("UPDATE job_info SET min_salary = ? , max_salary = ? , salary_type = ? WHERE url = ?",(data[0],None,data[1],url))
                        await db.commit()


async def salary_writing(data,db,url):
        salary = normalize_thousands_suffix(data)
        corrected_salary = checking_comma_exist(salary)
        salary_type = setting_hour_yearly(salary)
        detailed_data= re.findall(r"[\d.]+", corrected_salary)
        detailed_data.append(salary_type)
        float_converter(detailed_data)
        await writing_to_db_both_min_max(db,url,detailed_data)
        
        