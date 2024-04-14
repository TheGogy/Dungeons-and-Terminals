from PIL import Image, ImageTk
import tkinter as tk

class Sprite:
    def __init__(self):
        self.npc_types = {
            "goblin": "goblin",
            "good": "goodguy",
            "bad": "badguy",
            "creature": "creature"
        }

        self.player_moods = {
            "neutral": "images/playerneutral.png",
            "happy": "images/playerhappy.png",
            "angry": "images/playerangy.png",
            "sad": "images/playersad.png",
            "dead": "images/playerded.png",
            "really_happy": "images/playerreallyhappy.png",
            "really_hurt": "images/playerreallyhurt.png",
            "clueless": "images/playerclueless.png",
        }

        self.npc_moods = {
            "neutral": "images/neutral.png",
            "happy": "images/happy.png",
            "angry": "images/angy.png",
            "sad": "images/sad.png",
            "dead": "images/ded.png",
            "clueless": "images/clueless.png",
        }

        self.player_items = {
            "sword": ("images/sword.png", (130, 120)),
            "shield": ("images/shield.png", (130, 120)),
            "gold_coins": ("images/goldcoins.png", (130, 120)),
            "key": ("images/key.png", (130, 120)),
            "axe": ("images/axe.png", (130, 120)),
            "paper": ("images/paper.png", (130, 120)),
            "helmet": ("images/helmet.png", (130, 120)),
            "potion": ("images/potion.png", (130, 120)),
            "artifact": ("images/artifact.png", (130, 120)),
            "bow": ("images/bow.png", (130, 120)),
            "book": ("images/book.png", (130, 120)),
            "wand": ("images/wand.png", (130, 120))
        }

        self.npc_items = {
            "sword": ("images/sword.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "shield": ("images/shield.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "gold_coins": ("images/goldcoins.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "key": ("images/key.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "axe": ("images/axe.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "paper": ("images/paper.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "helmet": ("images/helmet.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "potion": ("images/potion.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "artifact": ("images/artifact.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "bow": ("images/bow.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "book": ("images/book.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                }),
            "wand": ("images/wand.png",
                {
                "goblin": (605, 155),
                "goodguy": (560, 125),
                "badguy": (595, 130),
                "creature": (585, 155)
                })
        }

    def image(self, player_mood, npc_type=None, npc_mood=None, item=None, npc_item=None):
        root = tk.Tk()
        root.geometry('750x200+600+525')
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        final = Image.open("images/background.png").convert("RGBA")
        player = Image.open(self.player_moods[player_mood]).convert("RGBA")

        final.paste(player, (0,0), mask=player)

        if item is not None and item in self.player_items:
            item = self.player_items[item]
            player_item = Image.open(item[0]).convert("RGBA")
            final.paste(player_item, item[1], mask=player_item)
        
        if npc_mood is not None and npc_type is not None:
            path = self.npc_moods[npc_mood].split("/")
            path = "/".join([path[0], self.npc_types[npc_type] + path[1]])
            npc = Image.open(path).convert("RGBA")
            final.paste(npc, (550,0), mask=npc)

        if npc_item is not None:
            temp = self.npc_items[npc_item]
            item = Image.open(temp[0]).convert("RGBA")
            item = item.transpose(Image.FLIP_LEFT_RIGHT)
            final.paste(item, temp[1][self.npc_types[npc_type]], mask=item)

        image = ImageTk.PhotoImage(final)
        panel = tk.Label(root, image=image)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        root.mainloop()