import re
def get_gemini_response_first(model,prompt,default_answer,text):
     response = model.generate_content(prompt.format(default_answer=default_answer,text=text))
     return response.text
    