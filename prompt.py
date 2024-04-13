# pip install -q -U google-generativeai
# Run that to work

import google.generativeai as genai
import json
import re


class Prompt():
    def __init__(self):
        genai.configure(api_key='AIzaSyACcVNtBZRh6HHxG7pDxa10JvimqoEDQzA')
        model = genai.GenerativeModel('gemini-pro')
        self.chat = model.start_chat(history=[])
        self.situation = {"current_health": 100, "current_stamina": 100,"current_situation": "You are outside a cave. There is a faint light coming from the back of the cave, with bats swirling around the entrance. A filthy smell hangs around the air.", "action":  "You choose to go into the cave", "inventory": ["sword", "shield"]}  

    def new_prompt(self, new_action):
        self.chat.send_message(
            f"""
            You are a Dungeon master for a text based Dungeons and Dragons game who responds entirely in JSON. Your response should contain the following fields:

            - current_health 
            - current_stamina 
            - situation 
            - inventory

            You also take the following inputs, in JSON format:

            - current_health
            - current_stamina
            - current_situation
            - action
            - inventory

            Do not respond with any information other than this raw JSON output or Markdown. Do not include any other information in your response. 
            {self.situation}
            """
            )
        if self.chat.history[-1].parts[0].text[0] == '`':
           self.chat.history[-1].parts[0].text = '\n'.join(self.chat.history[-1].parts[0].text.split('\n')[1:-1])
        # only change the double quotes to single quotes that are not a part of a word like apostrophes
        self.chat.history[-1].parts[0].text = re.sub(r"(?<!\w)'(?!s\s)", '"', self.chat.history[-1].parts[0].text)
        

        with open('response.json', 'w') as f:
            f.write(self.chat.history[-1].parts[0].text)
        
        with open('response.json', 'r') as f:
            data = json.load(f)
            data["action"] = [new_action]

        with open('response.json', 'w') as f:
            json.dump(data, f)

        self.situation = data
        

def main():
    prompt = Prompt()
    prompt.new_prompt("hello")
    
    with open('response.json', 'r') as f:
        data = json.load(f)
        print(data)

    prompt.new_prompt("go into the cave and eat")

    with open('response.json', 'r') as f:
        data = json.load(f)
        print(data)


if __name__ == "__main__":
    main()