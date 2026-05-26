from utilities import to_obj
from chain_4_1 import search_result_text_and_summary_chain

# test chain invocation
result_url_str = '{"result_url": "https://www.trip.com/travel-guide/destination/almaty-21387", "search_query": "Top attractions and things to do in Almaty Kazakhstan travel guide", "user_question": "What can I see and do in Almaty, Kazakhstan?"}'
result_url_dict = to_obj(result_url_str)

search_text_summary = search_result_text_and_summary_chain.invoke(result_url_dict)
print(search_text_summary)

# Result:
# {'summary': 'Source Url: https://www.trip.com/travel-guide/destination/almaty-21387\nSummary: The provided text does not list specific top attractions or things to do in Almaty. It is a Trip.com travel guide page header with navigation and site info.\n\nSummary of the text:\n- Title: Almaty Travel Guide 2026: Top Attractions, Things to Do & Deals | Trip.com | May 2026\n- URL: https://www.trip.com/travel-guide/destination/almaty-21387\n- Main sections available: Attractions & Tours, Hotels & Homes, Flights, Trains, Car services, Car Rentals, Airport Transfers, eSIM & SIM, Flight + Hotel, Private Tours, Group Tours, Trip.Planner, New Travel Inspiration, Trip.Best, Map, Trip.com Rewards, Deals, Travel Guides\n- Local experiences: Almaty Local Experiences (Map View)\n- Travel guidance details: Recommended trip 2–4 days; Current weather 18 °C\n- Footer/company info: About Trip.com, News, Careers, Terms & Conditions, Privacy/Accessibility Statements, Group info, Rewards, Affiliate program, Property listings, Security/Payment methods\n- © 2026 Trip.com Travel Singapore Pte. Ltd. All rights reserved\n\nIf you want actual top attractions, let me know and I can provide commonly recommended sights and activities for Almaty (e.g., based on other sources or a newer guide).', 'user_question': 'What can I see and do in Almaty, Kazakhstan?'}
