from chain_1_1 import assistant_instructions_chain

# test chain invocation
question = 'What can I see and do in Almaty, Kazakhstan?'

assistant_instructions = assistant_instructions_chain.invoke(question)
print(assistant_instructions)

# content='{\n  "assistant_type": "Tour guide assistant",\n  "assistant_instructions": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights.",\n  "user_question": "What can I see and do in Almaty, Kazakhstan?"\n}' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 410, 'prompt_tokens': 426, 'total_tokens': 836, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 320, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-DjpuhPWkuFozfASMeZmZPsLOzrIpd', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019e6557-1710-79b2-98a5-75722e583684-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 426, 'output_tokens': 410, 'total_tokens': 836, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 320}}