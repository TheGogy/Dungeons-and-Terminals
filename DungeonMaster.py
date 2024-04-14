import json
import json_repair
import re 
import google.generativeai as genai
from random import choice

class DungeonMaster():
    def __init__(self):

        genai.configure(api_key='AIzaSyACcVNtBZRh6HHxG7pDxa10JvimqoEDQzA')
        model = genai.GenerativeModel('gemini-pro')
        self.chat = model.start_chat(history=[])
        start_prompts = [
            "The tavern is known as 'The Rusty Mug,' a popular stop for travelers and adventurers alike. It's located in the small town of Oakhaven, nestled at the edge of the vast Whispering Woods. The town serves as a gateway to the wilderness beyond, where rumors speak of an ancient dungeon hidden deep within the forest. Legends tell of a powerful artifact hidden within its depths, guarded by fearsome monsters and traps. As the adventurers mingle in the tavern, they hear whispers of the dungeon's location and the riches it holds.",
            "The caravan was en route from the bustling city of Stonewall to the trading post of Eastport, following the winding road that cuts through the rugged Badlands. The attackers were a band of notorious highwaymen led by a ruthless bandit lord known as Blackfang. They've taken refuge in a makeshift fortress deep within the nearby Blackwood Forest, using it as a base of operations for their raids on travelers and merchants. The survivors of the ambush seek revenge and the recovery of their stolen goods, offering a handsome reward to anyone who can eliminate the threat.",
            "The ritual was performed by a secretive cult known as the Order of the Crimson Eye, dedicated to unlocking the secrets of forbidden knowledge. The ritual site is located atop an ancient hill known as the Altar of Lost Souls, overlooking the sprawling city of Silverhaven. The ritual was meant to summon a powerful entity from the beyond, but something went terribly wrong, causing a rift between dimensions to tear open. Strange creatures now roam the countryside, and the fabric of reality itself seems to be unraveling. The adventurers must uncover the truth behind the ritual and find a way to close the rift before it's too late.",
            "The prison is known as the Ironhold Penitentiary, a fortress-like structure built into the side of a rocky cliff overlooking the Stormfury Sea. It houses the kingdom's most dangerous criminals, from petty thieves to dark sorcerers. The chaos erupted when a group of prisoners staged a daring escape, aided by a powerful mage who breached the prison's magical wards. As the inmates fight for their freedom, the adventurers find themselves caught in the middle of the chaos. Beneath the prison lies a network of ancient catacombs and forgotten tunnels, rumored to be haunted by the restless spirits of the past.",
            "The village is known as Willowbrook, a peaceful hamlet nestled in the shadow of the towering Frostpeak Mountains. The villagers live simple lives, tending to their crops and livestock, unaware of the dark forces that lurk in the surrounding wilderness. The adventurers arrive in Willowbrook just as a series of mysterious disappearances plague the village, with the locals whispering of a malevolent presence in the nearby Whispering Woods. As the adventurers investigate, they uncover a sinister plot that threatens to consume the entire village in darkness.",
            "The adventurers were part of the crew of the merchant vessel 'The Sea Serpent,' sailing from the distant port of Brightwater to trade goods with the island nations of the Far West. A sudden storm struck without warning, driving the ship off course and smashing it against the rocky shores of a remote island. The island is shrouded in mystery, with dense jungles, towering cliffs, and ancient ruins hidden within its interior. Strange markings carved into the stone suggest that the island was once home to a lost civilization, but few have dared to venture far enough to uncover its secrets. As the survivors of the wreck, the adventurers must explore the island, fend off its dangers, and find a way to escape before they become permanent residents of its unforgiving shores."
            ]
        self.situation = {"current_health": 100, "current_stamina": 100,"current_situation": choice(start_prompts), "action":  "look around", "inventory": ["sword", "shield"]}  
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
