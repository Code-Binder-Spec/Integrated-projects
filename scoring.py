def deduplicate_list(list_name):
        converted = set(list_name)
        converted_list = list(converted)
        return converted_list


def removing_non_values(dictionary):
    
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

class ScoreBoard:
        def __init__(self,score,data):
                self.data = data
                self.score = score

        def url_initializer(self,url):
                 self.url = url

        def keyname_initializer(self,keyname):
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


async def scoring(metadata_list,board,score_list,true_list):
                                        for url in metadata_list:
                                                           board.url_initializer(url)
                                                           board.score = 0
                                                           for keyname in true_list:
                                                                           board.keyname_initializer(keyname)
                                                                           await board.database_initialization()
                                                                           if keyname == "company":
                                                                                         board.company_handler()
                                                                           elif keyname == "salary_type":
                                                                                         board.salary_type_handler()
                                                                           elif keyname == "job_type":
                                                                                         board.job_type_handler()
                                                                           elif keyname == "min_salary":
                                                                                         board.min_salary_handler()
                                                                           elif keyname == "max_salary":
                                                                                         board.max_salary_handler()
                                                                           elif keyname == "candidate_location":
                                                                                         board.location_handler()
                                                                           else :
                                                                                             continue
                                                           score_list.append(board.score)
                                        return score_list
