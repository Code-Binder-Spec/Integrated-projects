import asyncio
import chromadb
import json
import os
from groq import Groq
from dotenv import load_dotenv
import aiohttp
import aiosqlite

from other_components import deciding_position,acting_according_to_count,appending_function,table_creation,url_passing_full_data_getting,ai_reply
from scoring import deduplicate_list,removing_non_values, ScoreBoard ,scoring

async def run_pipeline(): 

           load_dotenv()

           client = chromadb.PersistentClient("job.db")       
           collection = client.get_or_create_collection("jobs")
           full_data = []
           async with aiosqlite.connect("jobdata.db") as db:
                        await table_creation(db)
                        async with aiohttp.ClientSession() as session :
                                        await url_passing_full_data_getting(session,full_data,db)
                        metadata_dup = []
                        appending_function(full_data,metadata_dup,"metadata_dup")
                        acting_according_to_count(collection.count(),collection,full_data,metadata_dup)
                        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                        print("\ntype stop in query to stop\n")
                        while True :
                                query = str(input("YOU : "))

                                if "stop" in query:
                                        break
                                reply = ai_reply(groq_client,f"You are a job search assistant. Extract structured filters from the user's query and return ONLY a JSON object with exactly these keys: vector_search (the job role or skills mentioned, or null), company (company name if mentioned, or null), salary_type (only set to hourly or monthly if the user explicitly mentions it, otherwise null), min_salary (minimum salary as a number if mentioned, or null), max_salary (maximum salary as a number if mentioned, or null), job_type (map full-time or full time to full_time, part-time to part_time, contract to contract, freelance to freelance, or null if not mentioned), candidate_location (location if mentioned, or null). Return ONLY valid JSON. Do not wrap in markdown code fences or backticks. No explanation, no extra text.\n\nquery : {query}")
                                dict_of_things = json.loads(reply) 
                                vector_content = dict_of_things["vector_search"]
                                if vector_content is None:
                                        vector_content = "job"
                                del dict_of_things["vector_search"]
                                true_list = removing_non_values(dict_of_things)
                                result = collection.query(
                                        query_texts=[vector_content],
                                        n_results=3,
                                )
                                metadata = result["metadatas"][0]
                                metadata_list = []
                                appending_function(metadata,metadata_list,"metadata_list")
                                score_list = []
                                score = 0
                                board = ScoreBoard(score,dict_of_things)
                                board.db_initializer(db)
                                score_list = await scoring(metadata_list,board,score_list,true_list)
                                converted_list = deduplicate_list(score_list)
                                position = deciding_position(converted_list,score_list)
                                real_chunk = collection.query(
                                        query_texts=[query],
                                        where={"url":metadata_list[position]},
                                        n_results=1
                                )
                                honest_chunk = real_chunk["documents"][0]
                                source_url = real_chunk["metadatas"][0][0]
                                reply_2 = ai_reply(groq_client,f"You are a job search assistant. First, check if the question is actually asking about a job, role, skill, company, or search criteria. If it is NOT a real job-related question (e.g. it's a greeting, a test message, or asking whether the system works), respond by asking the user to describe the job or role they're looking for, and do not mention the context at all. If it IS a real job-related question, answer using ONLY the context below (no outside knowledge), starting with 'The closest match of your search is:'. If the context doesn't contain enough info to answer a real question, say so clearly instead of guessing. Be concise and don't explain your reasoning or compare the question to context. If you do answer from the context, end your reply with the next line: 'Source: {source_url}'.\n\ncontext : {honest_chunk}\n\nQuestion : {query}")
                                print(f"AI : {reply_2}")
asyncio.run(run_pipeline())
