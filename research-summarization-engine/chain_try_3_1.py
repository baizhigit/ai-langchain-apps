from utilities import to_obj
from chain_3_1 import search_result_urls_chain

# test chain invocation
web_search_str = '{"search_query": "Top attractions and things to do in Almaty Kazakhstan travel guide", "user_question": "What can I see and do in Almaty, Kazakhstan?"}'
web_search_dict = to_obj(web_search_str)
result_urls_list = search_result_urls_chain.invoke(web_search_dict)
print(result_urls_list)

# Result:
# [{'result_url': 'https://www.tripadvisor.com/Attractions-g298251-Activities-Almaty.html', 'search_query': 'Top attractions and things to do in Almaty Kazakhstan travel guide', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}, {'result_url': 'https://www.trip.com/travel-guide/destination/almaty-21387/', 'search_query': 'Top attractions and things to do in Almaty Kazakhstan travel guide', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}, {'result_url': 'https://www.pinterest.com/pin/top-15-things-to-do-in-almaty--234539093090018466/', 'search_query': 'Top attractions and things to do in Almaty Kazakhstan travel guide', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}]
