def set_list_converter(list_name):
        print(list_name)
        converted = set(list_name)
        converted_list = list(converted)
        return converted_list


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
                  print(keyname)
 
        def db_initializer(self,db):
                self.db = db
      
        async def database_initialization(self):
                 if self.keyname in ["company","salary_type","min_salary","max_salary","job_type","location"]: 
                                   self.value_of_data = await self.db.execute(f"SELECT {self.keyname} FROM job_info WHERE url = ?",(self.url,))
                                   print(self.value_of_data)
                                   self.real_data = await self.value_of_data.fetchone()
                                   print(self.real_data)
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


async def scoring(url,metadata_list,board,score_list,true_list):
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
                                        return score_list
