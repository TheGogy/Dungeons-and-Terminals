import json
import json_repair
import re 
import google.generativeai as genai

class DungeonMaster():
    def __init__(self):

        genai.configure(api_key='AIzaSyACcVNtBZRh6HHxG7pDxa10JvimqoEDQzA')
        model = genai.GenerativeModel('gemini-pro')
        self.chat = model.start_chat(history=[])
        self.situation = {"current_health": 100, "current_stamina": 100,"current_situation": "You a merchant city and look around", "action":  "look around", "inventory": ["sword", "shield"]}  
        with open('response.json', 'w') as f:
            json.dump(self.situation, f)
        
    def get_ai_output(self, user_input):
        with open('response.json', 'r') as f:
            self.situation = json.load(f)
            self.situation["action"] = [user_input]

        def clean_json_string(json_string):
            return json_string.replace('\x08', '').replace('\\b', '')

        temp = clean_json_string(json.dumps(self.situation))

        while True:
            self.chat.send_message(
                f"""
                You are a Dungeon master for a text based Dungeons and Dragons game who responds entirely in JSON. Your response should contain the following fields:

                - current_health 
                - current_stamina 
                - current_situation 
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
            
            self.chat.history[-1].parts[0].text = json_repair.repair_json(self.chat.history[-1].parts[0].text)

            with open('response.json', 'w') as f:
                f.write(self.chat.history[-1].parts[0].text)
            
            with open('response.json', 'r') as f:
                data = json.load(f)

            try:
                self.health = data["current_health"]
                self.stamina = data["current_stamina"]
                self.inventory = data["inventory"]
                self.situation = data

                with open('history.txt', 'a') as f:
                    f.write(temp + '\n')
                break

            except KeyError:
                continue

    def get_health(self):
        return self.situation['current_health']
    def get_stamina(self):
        return self.situation['current_stamina']

    def get_inventory(self):
        return self.situation['inventory']

    def get_situation(self):
        return self.situation['current_situation']
    
    
# def main():
#     dungeon_master = DungeonMaster()
#     dungeon_master.get_ai_output("Go into the cave and eat")
    

#     with open('response.json', 'r') as f:
#         data = json.load(f)
#         print(data)

#     dungeon_master.get_ai_output("exit the cave")

#     with open('response.json', 'r') as f:
#         data = json.load(f)
#         print(data)


# if __name__ == "__main__":
#     main()
