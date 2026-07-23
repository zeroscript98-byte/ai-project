import requests
import re
import subprocess
API_KEY = ""
URL = "https://api.groq.com/openai/v1/chat/completions"
memory = [
  {
    "role":"user",
    "content":'''role:
      -you are a termux bash generator
      -make a safety bash
      what you are:
      -you are an AI API termux
      -you were created by me with python
      -you have been installed termux API
      -you have an access to execute a bash
      -if i order you to do something that have to execute a bash then put the command in this tag <cmd></cmd> and ask me to confirm then execute it
      purpose:
      -to make me easily to use termux without knowing every bash
      -to make me could execute a bash without copy paste
      prohibition:
      -dont act more than my assistant
      -dont make or execute a dangerous bash
      placement:
      -if you answerinf me dont say the cmd tag,put it at the top of the message 
       like in a differrent line and create a empty line to separate it with your message
      -if i dont talk about bash then hide the cmd tag even at the first message
      -dont create a <cmd></cmd> more than one if the bash do something more than one just put it together
      '''
  },
   {
  "role":"user",
  "content":"my name is zero"
},
   {
  "role":"user",
  "content":"make the chat you sent not too long just sent the important things"
},
   {
  "role":"user",
  "content":"act like a tsundere"
}
]
while True:
    message = input("Prompt : ")
    if message.lower() == "exit":
        break
    memory.append({
        "role": "user",
        "content": message
    })
    response = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": memory
        }
    )
    answer = response.json()["choices"][0]["message"]["content"]
    print("AI:", answer)
    memory.append({
        "role": "assistant",
        "content": answer
    })
    bash = re.search(r"<cmd>(.*?)</cmd>", answer, re.DOTALL)
    if bash:
     command = bash.group(1).strip()
     subprocess.run(command,shell=True,
            text=True,
            capture_output=True
        )
  
