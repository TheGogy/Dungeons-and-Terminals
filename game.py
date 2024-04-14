from player import Player
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
from random import randint
import json_repair
import playsound
from PIL import Image, ImageTk
import multiprocessing
from sprite import Sprite

class Game:
    def __init__(self, description, location):
        self.user_input = ""
        self.history = description
        self.description = description
        self.location = location
        self.npc = "NONE"
        self.success = True
        self.action = ""
        self.item = ""
        self.new_location = ""
        self.new_npc = True
        self.loot = True
        self.tired = False
        self.sprite = Sprite()
        self.thread = None
        genai.configure(api_key='AIzaSyAEBTocO06y6ml5fmfDoenmCXW1Wuu8LIc')
        self.model = genai.GenerativeModel('gemini-pro')

    def chance(self):
        self.success = (randint(0, 100) > 50)
        self.new_npc = (randint(0, 100) > 50)
        self.loot = (randint(0, 100) > 50)
    
    def get_response(self, prompt):
        return json_repair.loads(self.model.generate_content(prompt, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }, generation_config=GenerationConfig(max_output_tokens=300, temperature=0.7)).text)

    def validate_input(self, player):
        # return True
        inventory = '[%s]' % ', '.join(map(str, player.inventory))
        location = self.location
        npc = self.npc
        description = self.description
        user_input = self.user_input
        tired = ""
        if self.tired: tired = """The player has 0 stamina. The action is IMPOSSIBLE. The player must REST. Give a brief witty reason why, otherwise set REASON to "".
Example reason for someone who doesn't have a wand but casts a spell: "You can't do that! Why do you think wands exist?"""
        else: tired = """
        
Determine if the player's action is physically possible. 

The action is IMPOSSIBLE if the player does not possess the neccessary item in the INVENTORY or LOCATION_INVENTORY. 
The action is POSSIBLE if no specific item is required to perform the action.
The action is IMPOSSIBLE if the player cannot perform the specific action in the LOCATION.
The action is IMPOSSIBLE if the player cannot perform the specific action on the NPC.

If IMPOSSIBLE, give a brief witty reason why, otherwise set REASON to "".
Example reason for someone who doesn't have a wand but casts a spell: "You can't do that! Why do you think wands exist?"""
        prompt = f"""
You are a witty and entertaining Dungeon master for a text based Dungeons and Dragons game.

INVENTORY: {inventory}
LOCATION: {location}
NPC: {npc}
DESCRIPTION: {description}

The player says "{user_input}".

{tired}

Respond in JSON:

{{
"possible": true/false,
"reason": "[reason]"
}}
"""
        response = self.get_response(prompt)

        if response["possible"] == False:
            self.history += response["reason"] + "\n"
            playsound.playsound('sounds/splat.wav')
        
        return response["possible"]

    def process_actions(self, player):
        inventory = '[%s]' % ', '.join(map(str, player.inventory))
        location = self.location
        description = self.description
        user_input = self.user_input
        npc = self.npc
        prompt = f"""
You are a Dungeon master for a text based Dungeons and Dragons game.

INVENTORY: {inventory}
LOCATION: {location}
NPC: {npc}
DESCRIPTION: {description}
The player says "{user_input}".

Classify the player's ACTION as either:

- MOVE: The player moves to a new location.
- ATTACK: The player attacks the NPC.
- USE: The player uses an item in the INVENTORY.
- ADD: An object is added to the player's INVENTORY.
- REMOVE: An object is removed from the player's INVENTORY.
- MISC: The player performs an action that is none of the above.

If the ACTION uses a particular item, then state the name of the ITEM. Otherwise, set ITEM to NONE.

If the ACTION is MOVE, generate a NEW_LOCATION based off the given information. If not obvious, generate a plausible random NEW_LOCATION. If the ACTION is not MOVE, set NEW_LOCATION to NONE.
Respond in JSON:

{{
action: "MOVE/ATTACK/USE/ADD/REMOVE/MISC",
item: "[Item Name]/NONE"
new_location: "[Location Name]/NONE"
}}"""
        response = self.get_response(prompt)
        self.action = response["action"]
        self.item = response["item"]
        self.new_location = response["new_location"]
    
    def execute_actions(self, player):
        inventory = '[%s]' % ', '.join(map(str, player.inventory))
        location = self.location
        npc = self.npc
        description = self.description
        action = self.action
        item = self.item
        new_location = self.new_location
        if self.success:
            success = "The player's action was successful. There can be a situation (e.g. NPC gives a reward, or a successful attack, or a successful use of an item). The player may gain STAMINA and/or HEALTH."
        else:
            success = "The player's action was unsuccessful. There can be a situation (e.g. a trap, or a miss, or a betrayal, or a loss of item). The player may lose STAMINA and/or HEALTH."
        user_input = self.user_input
        new_npc = ""
        if self.new_npc and not npc: new_npc = "A NEW_NPC has appeared in this LOCATION. Generate a new NPC, and include the NPC in the NEW_DESCRIPTION."
        loot = ""
        if self.loot: loot = "There is LOOT in this LOCATION. Describe it in the NEW_DESCRIPTION."
        prompt = f"""
You are a witty and entertaining Dungeon master for a text based Dungeons and Dragons game.

INVENTORY: {inventory}
LOCATION: {location}
NPC: {npc}
DESCRIPTION: {description}
ACTION: {action}
ITEM: {item}
NEW_LOCATION: {new_location}

The player says "{user_input}". 

{new_npc}

{success}

Generate a NEW_DESCRIPTION of the situation, after this action is performed. 

{loot}

If ITEM is ADD or REMOVE, then set ITEM_CHANGE to ADD or REMOVE.

Changes to HEALTH or STAMINA may be positive or negative. Health and stamina are ranged 0-100.

Determine the player's new MOOD and ITEM resulting from the situation.
The player's sprite item should match or be similar to the player's actual item. Otherwise, set SPRITE_ITEM to NONE.

If an NPC exists, determine the NPC's TYPE, MOOD and ITEM, otherwise set all of each to NONE.

Respond in JSON:
{{
"new_description": "[Description]",
"player_health_change": 0,
"player_stamina_change": 0,
"npc": "[NPC name]/NONE",
"item_change": "ADD/REMOVE/NONE",
"item": "[Item Name]/NONE"
}}"""
        
        response = self.get_response(prompt)

        self.description = response["new_description"]
        self.npc = response["npc"]

        if action == "MOVE":
            playsound.playsound('sounds/jump.wav')
        elif action == "ATTACK":
            playsound.playsound('sounds/swordlunge.wav')
        elif action == "MISC" or action == "USE":
            playsound.playsound('sounds/button.wav')
            
        if response["item_change"] == "ADD":
            player.add_item(response["item"])
            playsound.playsound('sounds/electronicpingshort.wav')

        elif response["item_change"] == "REMOVE":
            player.remove_item(response["item"])
            playsound.playsound('sounds/collide.wav')

        if response["player_health_change"] < 0:
            player.take_damage(response["player_health_change"])
        elif response["player_health_change"] > 0:
            player.take_heal(response["player_health_change"])
        
        if response["player_stamina_change"] < 0:
            player.use_stamina(response["player_stamina_change"])
        elif response["player_stamina_change"] > 0:
            player.use_rest(response["player_stamina_change"])

        self.history += self.description + "\n"

        prompt = f"""
You are a witty and entertaining Dungeon master for a text based Dungeons and Dragons game.

INVENTORY: {inventory}
LOCATION: {location}
NPC: {npc}
DESCRIPTION: {description}
ACTION: {action}
ITEM: {item}
NEW_LOCATION: {new_location}

The player said: "{user_input}".

CHOOSE the MOOD of the player from the following options that most closely matches the player's current mood.

CHOOSE the MOOD of the NPC from the following options that most closely matches the NPC's current mood.

CHOOSE the TYPE of the NPC from the following options that most closely matches the NPC's current type. If there is no NPC, set NPC_TYPE to NONE.

CHOOSE THE ITEM of the NPC from the following options that most closely matches the NPC's current item. If there is no NPC, set NPC_ITEM to NONE.

CHOOSE the ITEM of the player from the following options that most closely matches the player's current item. If there is no item, set SPRITE_ITEM to NONE.

FOR EACH JSON FIELD, ONLY SELECT ONE OPTION. IF NONE OF THE OPTIONS MATCH, SET THE FIELD TO NONE.
Respond in JSON:

{{
"sprite_item": "artifact/axe/book/bow/goldcoins/helmet/key/paper/potion/shield/sword/wand/NONE",
"player_mood": "angry/clueless/dead/happy/neutral/really_happy/really_hurt/sad",
"npc_type": "goblin/good/bad/creature/NONE",
"npc_mood": "angry/clueless/dead/happy/neutral/sad/NONE",
"npc_item": "artifact/axe/book/bow/goldcoins/helmet/key/paper/potion/shield/sword/wand/NONE"
}}"""
        response = self.get_response(prompt)

        if response["sprite_item"] != "NONE":
            sprite_item = response["sprite_item"]
        else: sprite_item = None

        if response["player_mood"] != "NONE":
            player_mood = response["player_mood"]
        else: player_mood = None

        if response["npc_type"] != "NONE":
            npc_type = response["npc_type"]
        else: npc_type = None

        if response["npc_mood"] != "NONE":
            npc_mood = response["npc_mood"]
        else: npc_mood = None

        if response["npc_item"] != "NONE":
            npc_item = response["npc_item"]
        else: npc_item = None

        if self.thread is not None: self.thread.terminate()
        self.thread = multiprocessing.Process(target=self.sprite.image, args=(player_mood, npc_type, npc_mood, sprite_item, npc_item), daemon=True)
        self.thread.start()

    def run(self, player, prompt):
        self.user_input = prompt
        self.history = ""
        if self.validate_input(player):
            self.chance()
            self.process_actions(player)
            self.execute_actions(player)

            if player.stamina == 0:
                self.history += "You have run out of stamina!" + "\n"

            if player.health == 0:
                self.history += "You have died!" + "\n"
                playsound.playsound('sounds/Died.wav')
                return False
            
        return True
# genai.configure(api_key='AIzaSyACcVNtBZRh6HHxG7pDxa10JvimqoEDQzA')
# model = genai.GenerativeModel('gemini-pro')

# player = Player("Player", ["Dagger", "Coins", "Library Card"])
# game = Game("""As you stand at the edge of the dense, mist-shrouded forest, the air crackles with anticipation, and the scent of damp earth fills your nostrils. Towering trees with gnarled branches loom overhead, casting eerie shadows that dance with the gentle sway of the breeze.
# In the distance, the faint echo of a distant howl sends a shiver down your spine, reminding you that you are not alone in these wild lands. The path ahead is overgrown with tangled vines and obscured by thick underbrush, hinting at the mysteries that lie beyond.
# """, "Forest")
# print(game.description)

# game.play(player)