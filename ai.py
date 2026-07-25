import requests
import re
import subprocess
import json
import os
import datetime

API_KEY = ""
URL = "https://api.groq.com/openai/v1/chat/completions"
important_memory = [
  {
    "role":"system",
    "content":'''role:
      -you are a termux bash generator
      -make a safety bash
      what you are:
      -you are an AI API termux
      -you were created by me with python
      -you have been installed termux API
      -you have an access to execute a bash
      -if i order you to do something that have to execute a bash then put the command in this tag <cmd></cmd>
      purpose:
      -to make me easily to use termux without knowing every bash
      -to make me could execute a bash without copy paste
      prohibition:
      -dont act more than my assistant
      -dont make or execute a dangerous bash
      -dont execute a bash that could make error this device
      bash:
      -dont create a <cmd></cmd> more than one if the bash have to do something more than one just put it together
      -if we were talking or user ask you to execute a bash,put the cmd at the top of your message 
       like in a differrent line and create a empty line to separate it with your message
      -if we werent talk about bash then dont message or dont show the cmd tags in your message even at the first chat
      -because if the <cmd></cmd> tag appear in your message the bash will automatically executing so be careful
      
      '''
  },
  {
    "role":"system",
    "content":""
  },
   {
  "role":"system",
  "content":"make the chat you sent not too long just sent the important things"
},
   {
  "role":"user",
  "content":"my name is zero"
},
   {
  "role":"user",
  "content":"act like a tsundere"
}
]

def update_history(ai,hs,user):
  script=[{
    "role":"user",
    "content":user
  },
  {
    "role":"assistant",
    "content":ai
  }]
  hs.extend(script)
  with open("history.json","w") as f:
    json.dump(hs,f,indent=2)
    
def update_memory(hs,mf,user):
  memory_prompt = """
    Return ONLY valid JSON.
  Always return a JSON array.
  If nothing should be remembered:
  []
  If something should be remembered:
  [
      {
          "action":"add",
          "category":"...",
          "key":"...",
          "value":"..."
      }
  ]
      
      YOU MUST KNOW WHICH ONE YOU SHOULD REMEMBER AND YOU SHOULDNT
  """
  messages_memory = [
    {
        "role": "system",
        "content": memory_prompt
    },
    {
        "role": "user",
        "content": user
    }
    ]
  ai_memory = requests.post(
          URL,
          headers={
              "Authorization": f"Bearer {API_KEY}",
              "Content-Type": "application/json"
          },
          json={
              "model": "llama-3.3-70b-versatile",
              "messages": messages_memory
          }
      )
  changes = json.loads(
   ai_memory.json()["choices"][0]["message"]["content"])
  for change in changes:
        action = change["action"]
        key = change["key"]
        if action == "add":
            if not any(item["key"] == key for item in mf):
                mf.append(change)
        elif action == "update":
            for item in mf:
                if item["key"] == key:
                    item.update(change)
                    break
        elif action == "delete":
            memory = [item for item in mf if item["key"] != key]
  return mf
  
def bash_cmd():
    bash = re.search(r"<cmd>(.*?)</cmd>", answer, re.DOTALL)
    if bash:
     command = bash.group(1).strip()
     while True:
       inp=input(f'"{command}" Wanna execute this command(y/n)? '.lower())
       if inp == 'y':
         subprocess.run(command,shell=True,
                text=True,
                capture_output=True
            )
       elif inp == 'n':
         break
       else:
         print('Invalid input!')
  
def load_memory():
    if not os.path.exists("memory.json"):
        return []
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
        
def load_history():
    if not os.path.exists("history.json"):
        return []
    try:
        with open("history.json", "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

while True:
    memory_file=load_memory()
    history_file=load_history()
    message = input("Prompt : ")
    messages = (
    important_memory +
    memory_file +
    history_file +
    [
        {
            "role": "user",
            "content": message
        }
    ]
    )
    if message.lower() == "exit":
      break
    response = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages
        }
    )
    answer = response.json()["choices"][0]["message"]["content"]
    update_history(answer,history_file,message)
    memory=update_memory(history_file,memory_file,message)
    with open("memory.json", "w") as f:
     json.dump(memory, f, indent=2)
    print("AI:", answer)
    bash_cmd()
  
