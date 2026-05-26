from utilities import to_obj
from chain_2_1 import web_searches_chain

# test chain invocation
assistant_instruction_str = '{"assistant_type": "Tour guide assistant", "assistant_instructions": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights.", "user_question": "What can I see and do in Almaty, Kazakhstan?"}'
assistant_instruction_dict = to_obj(assistant_instruction_str)
web_searches_list = web_searches_chain.invoke(assistant_instruction_dict)
print(web_searches_list)

# Result:
# [{'search_query': 'Top attractions and things to do in Almaty Kazakhstan travel guide', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}, {'search_query': 'Almaty nature spots and outdoor activities Big Almaty Lake Shymbulak Kok Tobe mountains', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}, {'search_query': 'Historical and cultural sites in Almaty Kazakhstan Panfilov Park Zenkov Cathedral Central State Museum UNESCO', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}]