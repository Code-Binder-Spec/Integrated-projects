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

                
        