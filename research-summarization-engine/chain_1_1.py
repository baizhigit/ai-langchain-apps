from llm_models import get_llm
from prompts import (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE, 
)

assistant_instructions_chain = (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE | get_llm()
)