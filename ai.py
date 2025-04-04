import os
import google.generativeai as genai

def ai_rec(weather:str, genres:list):
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="You will be given the current weather and top genres. Your job is to give me a list of 40-90 distinct, unique songs that are appropriate to the weather and the user's top genres. The output must be in a python list format where each item is the title of the song. Ensure there are no duplicate song titles. For example, if the weather is sunny and top genres are [synthwave, electronic], your answer should be in the format of ['memory reboot', 'fainted']. Do not include the artist in the title of the song. Do not write any text other than the python list.",
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  response = chat_session.send_message(f'weather:{weather} and genres:{genres}')
  return eval(response.text)
