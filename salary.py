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

def checking_thing(specific_salary):
               spicy = specific_salary
               thing_to_check = ",000"
               if thing_to_check in specific_salary:
                         spicy = specific_salary.replace(thing_to_check,"k")
               return spicy

def float_converter(lis_var):
        if "yearly" in lis_var:
                 for i in range(1):
                         fl_version = float(lis_var[i])
                         lis_var[i] = fl_version*1000
        return lis_var

async def writing_to_db(db,url):
             await db.execute("UPDATE")


def salary_extracting(data,db,url):
        salary = checking_thing(data)
        corrected_salary = checking_comma_exist(salary)
        salary_type = setting_hour_yearly(salary)
        numbers = re.findall(r"[\d.]+", corrected_salary)
        numbers.append(salary_type)
        float_converter(numbers)
        return numbers