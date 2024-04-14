import curses
from thefuzz import fuzz
from functools import partial
import nerdfonts
from DungeonMaster import DungeonMaster

WILL_TO_LIVE = 0
NERDFONTS = nerdfonts.get_nerdfonts()

class DungeonsAndTerminals():
    def __init__(self,stdscr):
        # Set up the screen
        self.stdscr = stdscr
        self.init_variables()
        self.render()
        self.run()

    def init_variables(self):
        self.dungeon_master = DungeonMaster()
        self.is_stats = True
        self.prompt_text = ""
        self.situation_text = f"Dungeon Master:\n{self.dungeon_master.get_situation()}\n"
        
    def render(self):
        self.init_main()
        self.init_info()
        self.init_output()
        self.init_shortcuts()
        self.init_input()

    def init_main(self):
        self.stdscr.clear()  # Clear the screen
        self.stdscr.keypad(True)
        curses.use_default_colors();
        # Get screen dimensions
        self.height, self.width = self.stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Title
        title = "Dungeons and Terminals"
        title_len = len(title)
        title_x = (self.width - title_len) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        self.stdscr.refresh()

    def init_info(self):
        self.info_win = curses.newwin(self.height - 6, 20, 3, self.width - 22)
        self.update_info()

    def update_info(self): 
        self.info_win.clear() 
        self.info_win.border()
        if self.is_stats is True:
            self.update_statistics()
        else:
            self.update_inventory()
        self.info_win.refresh()

    def update_statistics(self):
        info_y, info_x = self.info_win.getmaxyx()
        statistics_text = " Statistics "
        self.info_win.addstr(0, (info_x - len(statistics_text))//2, statistics_text, curses.A_BOLD)
        bar_height = info_y - 5
        bar_width  = info_x // 5

        #HEALTH
        self.info_win.attron(curses.color_pair(1))
        health_bar_top = round((1 - self.dungeon_master.get_health() / 100) * bar_height)
        for y in range(info_y - 3,health_bar_top + 2,-1):
            for x in range(bar_width):
                self.info_win.addch(y,x + bar_width,curses.ACS_BOARD)
        self.info_win.attroff(curses.color_pair(1))
        self.info_win.addstr(info_y - 2,bar_width + round((bar_width - len(str(self.dungeon_master.get_health())))/2), str(self.dungeon_master.get_health()))

        #STAMINA
        self.info_win.attron(curses.color_pair(2))
        stamina_bar_top = round((1 - self.dungeon_master.get_stamina() / 100) * bar_height)
        for y in range(info_y - 3,stamina_bar_top + 2,-1):
            for x in range(bar_width):
                self.info_win.addch(y,x + 3 * bar_width,curses.ACS_BOARD)
        self.info_win.attroff(curses.color_pair(2))
        self.info_win.addstr(info_y - 2, 3 * bar_width + round((bar_width - len(str(self.dungeon_master.get_stamina())))/2), str(self.dungeon_master.get_stamina()))

    def update_inventory(self):
        info_y, info_x = self.info_win.getmaxyx()
        inventory_text = " Inventory "
        self.info_win.addstr(0, (info_x - len(inventory_text))//2, inventory_text, curses.A_BOLD)

        for x in range(len(self.dungeon_master.get_inventory())):
            self.info_win.addstr((x * 2) + 2,2, f"{self.get_icon(self.dungeon_master.get_inventory()[x])} {self.dungeon_master.get_inventory()[x]}")

    def get_icon(self, item: str):
        try:
            return NERDFONTS[item]
        except KeyError:
            f = partial(fuzz.partial_ratio, item)
            match = max(NERDFONTS, key=f)
            if (f(match)) < 90:
                return "-"
            else:
                return NERDFONTS[match]

    def init_input(self):
        # Input box
        self.input_box = curses.newwin(3, self.width - 25, 3, 2)
        self.input_box.nodelay(True)
        self.update_input_text()

    def update_input_text(self):
        self.input_box.clear()
        self.input_box.border()
        self.input_box.addstr(0, 2, " Your action ", curses.A_BOLD)
        self.input_box.addstr(1, 2, self.prompt_text[-self.input_box.getmaxyx()[1] +4:])
        self.input_box.refresh()


    def init_output(self):
        # Output box
        self.output_box = curses.newwin(self.height - 10, self.width - 25, 7, 2)
        self.update_output_text() 

    def update_output_text(self):
        self.output_box.clear()
        self.output_box.border()
        self.output_box.addstr(0,2," Situation ",curses.A_BOLD)
        text_height, text_width = self.output_box.getmaxyx()
        text_width  -= 4
        text_height -= 2
        text = []
       
        for token in self.situation_text.split("\n"): 
            start = 0
            while start < len(token):
                text.append(token[start:start+text_width])
                start += text_width
        text = text[- text_height :]
        for x in range(len(text)):
            if text[x] == "Player:" or text[x] == "Dungeon Master:":
                self.output_box.addstr(1 + x, 2, text[x], curses.A_BOLD)
            else:
                self.output_box.addstr(1 + x,2, text[x])

        self.output_box.refresh()

    def init_shortcuts(self):
        self.shortcuts_win = curses.newwin(3, self.width - 4, self.height - 3,2)
        self.shortcuts_win.border()
        self.shortcuts_win.addstr(0,2, " Commands ",curses.A_BOLD)
        text = "Toggle Inventory/Items : Ctrl B | Exit : Esc | Reroll : Ctrl R"  
        shortcuts_y, shortcuts_x = self.shortcuts_win.getmaxyx()
        self.shortcuts_win.addstr(1,round((shortcuts_x - len(text))/ 2),text,curses.A_BOLD)
        self.shortcuts_win.refresh()

    def run(self):
        # Loop to handle user input
        while True:
            # Get user input
            key = self.input_box.getch()
            if key != -1:
                if key == 127:
                    self.prompt_text = self.prompt_text[:-1]
                elif key == 10:
                    self.dungeon_master.get_ai_output(self.prompt_text)
                    self.situation_text += f"Player:\n{self.prompt_text}\n"
                    self.situation_text += f"Dungeon Master:\n{self.dungeon_master.get_situation()}\n"
                    self.update_output_text()
                    self.update_info()
                    self.prompt_text = ""
                elif key == 2:
                    self.is_stats = not self.is_stats
                    self.update_info()
                elif key == 27:
                    break
                elif key == 18:
                    with open("write.txt","w") as file:
                        file.write(str("You see me rolling"))
                elif key == 410:
                    self.render()
                else:
                    self.prompt_text += chr(key)
                    with open("write.txt","w") as file:
                        file.write(str(key))
                self.update_input_text()

def main(stdscr):
    app = DungeonsAndTerminals(stdscr)


# Run the program
if __name__ == "__main__":
    curses.wrapper(main)
