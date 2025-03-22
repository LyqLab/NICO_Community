"""
Author: Yuqian Lan (Yuqian_Lan_xjtu@stu.xjtu.edu.cn)

File: gpt_structure.py
Description: functions for calling APIs.
"""
import json
import random
import openai
import time 

from utils import *
import requests                                                                                                       
from typing import List                                                                                                

from transformers import BertTokenizer, BertModel

openai.api_key = "sk-"          #openai api key, because we use both api of openai and llama2

server_url = "http://localhost:5129"                                            # Define the Flask server address for tunnel access to Llama2

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

def ChatGPT_single_request(prompt): 
  temp_sleep()

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
  )
  return completion["choices"][0]["message"]["content"]


def GPT4_request(prompt): 

  temp_sleep()

  try: 
    completion = openai.ChatCompletion.create(
    model="gpt-4", 
    messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"

# !!!! Call ChatGPT API !!!!
def ChatGPT_request(prompt): 

  # temp_sleep()
  try: 
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"


# !!!! Call Llama2 API !!!!
def Llama2_request(prompt):
  datalines: List[str] = [prompt]
  # headers = {'Content-Type': 'application/json'}

  temp_sleep()
  try:
    #print(f'[Client Message] : {prompt}')
    response = requests.post(f'{server_url}/api', json=datalines)
    # response = requests.post(f'{server_url}/api', json=data)
    # response = requests.post(f'{server_url}/api', json=data, headers=headers)

    if response.status_code == 200:
      print('\n\033[34m[ INFO ] success \033[0m\n')

      result = response.json()
      #print(f'[Server Response] : {result}')
      #print(result['result'][0]['generation'])
      #return result['result'][0]['generation']
      return result['result']
    else:
      print('\n\033[31m[ ERROR ] \033[0m\n')
      return "Llama2 ERROR"
      exit(1)

  except Exception as e:
    print('\n\033[31m[ ERROR ] Llama2 ERROR: \033[0m\n', str(e))
    return "Llama2 ERROR"
    exit(1)


def GPT4_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = GPT4_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False


def ChatGPT_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False,
                                   SimpleOut=False):
  # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  #prompt = '"""\n' + prompt + '\n"""\n'
  if SimpleOut == False:
    prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
    prompt += "Example output json:\n"
    prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 

    try:
      # curr_gpt_response = ChatGPT_request(prompt).strip()                   # !!!! Call ChatGPT API !!!!
      curr_gpt_response = Llama2_request(prompt).strip()                      # !!!! Call Llama2 API !!!!

      if SimpleOut == False:
        end_index = curr_gpt_response.rfind('}') + 1
        curr_gpt_response = curr_gpt_response[:end_index]
        curr_gpt_response = json.loads(curr_gpt_response)["output"]
      else:
        curr_gpt_response = curr_gpt_response.split(".\n")[0]

      # print ("---ashdfaf")
      # print (curr_gpt_response)
      # print ("000asdfhia")
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass


  for i in range(repeat):

    try:
      curr_gpt_response = ChatGPT_request(prompt).strip()                   # !!!! Call ChatGPT API !!!!
      # curr_gpt_response = Llama2_request(prompt).strip()                  # !!!! Call Llama2 API !!!!

      if SimpleOut == False:
        end_index = curr_gpt_response.rfind('}') + 1
        curr_gpt_response = curr_gpt_response[:end_index]
        curr_gpt_response = json.loads(curr_gpt_response)["output"]
      else:
        curr_gpt_response = curr_gpt_response.split(".\n")[0]

      if func_validate(curr_gpt_response, prompt=prompt):
        return func_clean_up(curr_gpt_response, prompt=prompt)

      if verbose:
        print("---- repeat count: \n", i, curr_gpt_response)
        print(curr_gpt_response)
        print("~~~~")

    except:
      pass

  return False


def ChatGPT_safe_generate_response_OLD(prompt, 
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 
    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      #curr_gpt_response = Llama2_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print (f"---- repeat count: {i}")
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass
  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response




def GPT_request(prompt, gpt_parameter): 
  temp_sleep()
  try: 
    response = openai.Completion.create(
                model=gpt_parameter["engine"],
                prompt=prompt,
                temperature=gpt_parameter["temperature"],
                max_tokens=gpt_parameter["max_tokens"],
                top_p=gpt_parameter["top_p"],
                frequency_penalty=gpt_parameter["frequency_penalty"],
                presence_penalty=gpt_parameter["presence_penalty"],
                stream=gpt_parameter["stream"],
                stop=gpt_parameter["stop"],)
    return response.choices[0].text
  except: 
    print ("TOKEN LIMIT EXCEEDED")
    return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file): 
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    #curr_gpt_response = GPT_request(prompt, gpt_parameter)
    curr_gpt_response = Llama2_request_para(prompt, gpt_parameter).strip()
    if func_validate(curr_gpt_response, prompt=prompt): 
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response

def safe_generate_response_GPT35(prompt,
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False):
  if verbose:
    print (prompt)

  for i in range(repeat):
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    #curr_gpt_response = Llama2_request_para(prompt, gpt_parameter).strip()
    print('>>>>>>>>>>>>>>>>>>  curr_gpt_response in safe_generate_response_GPT35  <<<<<<<<<<<<<<<<<<<<<<<<<<')
    print(curr_gpt_response)
    if func_validate(curr_gpt_response, prompt=prompt):
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose:
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response



def get_embedding(text):                    # Call BERT embedding
  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')

  words = text.split()
  length_text = len(words)
  if length_text > 500:
    text = ' '.join(words[:500])

  inputs = tokenizer(text, return_tensors='pt')
  outputs = model(**inputs)

  # last_hidden_states = outputs.last_hidden_state
  # print('last_hidden_states:' ,last_hidden_states)
  pooler_output = outputs.pooler_output
  #print('---pooler_output: ', pooler_output)

  result = pooler_output.view(-1).tolist()        # https://developer.baidu.com/article/detail.html?id=2330848
  print(result)
  return result



def Llama2_request_para(text, gpt_parameter):

  datalines: List[str] = [text]

  max_tokens = gpt_parameter["max_tokens"]
  if max_tokens > 320:
    max_tokens = 320
  temperature = gpt_parameter["temperature"]
  data = {
      'message': datalines,  # f'{[prompt_Input]}
      'max_tokens': max_tokens,
      'temperature': temperature,
  }

  temp_sleep()
  try:
    response = requests.post(f'{server_url}/para', json=data)
    if response.status_code == 200:
      print('\n\033[34m[ INFO ] \033[0m\n')
      result = response.json()
      result = result['result']

      if gpt_parameter["stop"] != None:
        result = result.split(gpt_parameter["stop"][0])
        return result[0]
      else:
        return result
    else:
      print('\n\033[31m[ ERROR ] \033[0m\n')
      return "Llama2 ERROR"
      exit(1)

  except Exception as e:
    print('\n\033[31m[ ERROR ] 发生错误： \033[0m\n', str(e))
    return "Llama2 ERROR"
    exit(1)






