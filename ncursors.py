import curses
from thefuzz import fuzz
from functools import partial
import nerdfonts
from DungeonMaster import DungeonMaster
import ascii
import sys
import webbrowser
from time import sleep

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
        curses.curs_set(1)
        self.is_stats = True
        self.height, self.width = self.stdscr.getmaxyx()
        self.prompt_text = ""
        self.exit_win = None
        self.dungeon_master = None
        
    def render(self):
        self.init_main()
        if self.dungeon_master is None:
            self.prompt_selector()
        self.init_main()
        self.init_info()
        self.init_output()
        self.init_shortcuts()
        self.init_input()

    def prompt_selector(self):

        width = 30
        height = 11
        prompts = list(DungeonMaster.start_prompts.keys())
        self.prompt_selector_win = self.stdscr.subwin(height,width,(self.height - height) //2,(self.width - width) // 2)
        self.prompt_selector_win.keypad(True)
        self.prompt_selector_win.bkgd(curses.color_pair(3))
        for x in range(len(prompts)):
            self.prompt_selector_win.addstr((x *2) + 1,2,f"{x + 1}. {prompts[x]}",curses.A_BOLD)
        x = 1
        curses.curs_set(0)
        while True:
            key = self.prompt_selector_win.getch()
            if key >= 49 and key <= 53:
                self.prompt_selector_win.addstr((x *2) + 1,2,f"{x + 1}. {prompts[x]}",curses.A_BOLD)
                x = key - 49
                self.prompt_selector_win.addstr(x *2 + 1,2,f"{x + 1}. {prompts[x]}",curses.A_BOLD | curses.A_REVERSE)
            if key == 27:
                curses.endwin() 
                sys.exit()
            if  key == 10:
                break      
            self.prompt_selector_win.refresh()
        self.prompt_selector_win.clear()

        self.prompt_selector_win.refresh()
        curses.curs_set(1)
        self.dungeon_master = DungeonMaster(prompts[x])
        self.situation_text = f"Dungeon Master:\n{self.dungeon_master.get_situation()}\n"
        self.prompt_selector_win = None


    def init_main(self):
        self.stdscr.clear()  # Clear the screen
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)        
        curses.use_default_colors();
        # Get screen dimensions
        self.height, self.width = self.stdscr.getmaxyx()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_BLACK)
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
        if self.dungeon_master.get_health() <= 0:
            self.show_death_screen()
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
                if self.dungeon_master.get_health() < 10:
                    self.info_win.addch(y,x + bar_width,curses.ACS_BOARD,curses.A_BLINK)
                else:
                    self.info_win.addch(y,x + bar_width,curses.ACS_BOARD)
        self.info_win.attroff(curses.color_pair(1))
        self.info_win.addstr(info_y - 2,bar_width + round((bar_width - len(str(self.dungeon_master.get_health())))/2), str(self.dungeon_master.get_health()))

        #STAMINA
        self.info_win.attron(curses.color_pair(2))
        stamina_bar_top = round((1 - self.dungeon_master.get_stamina() / 100) * bar_height)
        for y in range(info_y - 3,stamina_bar_top + 2,-1):
            for x in range(bar_width):
                if self.dungeon_master.get_stamina() < 5:
                    self.info_win.addch(y,x + 3 * bar_width,curses.ACS_BOARD,curses.A_BLINK)
                else:
                    self.info_win.addch(y,x + 3 * bar_width,curses.ACS_BOARD)
        self.info_win.attroff(curses.color_pair(2))
        self.info_win.addstr(info_y - 2, 3 * bar_width + round((bar_width - len(str(self.dungeon_master.get_stamina())))/2), str(self.dungeon_master.get_stamina()))

    def show_death_screen(self):
        self.stdscr.clear()
        curses.curs_set(0)
        death_win = self.stdscr.subwin(22,35,(self.height // 2) - 11,10)
        death_win_mirror = self.stdscr.subwin(22,35,(self.height // 2) - 11, self.width - 45)
        you_died_win = self.stdscr.subwin(22,55,(self.height // 2) - 11, (self.width // 2) - 19)
        restart = self.stdscr.subwin(2,16, (self.height) // 2 + 10,(self.width // 2) - 9)
        restart.addstr(0,0,"Escape  : Esc",curses.A_BOLD)
        restart.addstr(1,0,"Restart : Enter",curses.A_BOLD)
        death_win.border()
        death_win_mirror.border()
        skull, mirror_skull, you_died = ascii.get_skulls()
        for i, line in enumerate(skull):
            death_win.addstr(i+1,2,line)
        for i, line in enumerate(mirror_skull):
            death_win_mirror.addstr(i+1,2,line)
        for i, line in enumerate(you_died):
            you_died_win.addstr(i+4,2,line, curses.A_BLINK)
        self.stdscr.refresh()
        while True:
            key = death_win.getch()
            if key == curses.KEY_ENTER or key == 10:
                self.__init__(self.stdscr)
            if key == 27:
                curses.endwin() 
                sys.exit()

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
        text = "Toggle Inventory/Items : Ctrl B | Exit : Esc | Rickroll : Ctrl R"  
        shortcuts_y, shortcuts_x = self.shortcuts_win.getmaxyx()
        self.shortcuts_win.addstr(1,round((shortcuts_x - len(text))/ 2),text,curses.A_BOLD)
        self.shortcuts_win.refresh()

    def exit_subwin(self):
        width = 24
        height = 4
        quit = True
        self.exit_win = self.stdscr.subwin(height,width,(self.height - height) //2,(self.width - width) // 2)
        self.exit_win.keypad(True)
        self.exit_win.bkgd(curses.color_pair(3))
        self.exit_win.addstr(1,2,"Please Confirm Exit")
        self.exit_win.addstr(2,6,"CANCEL/",curses.A_BOLD)
        self.exit_win.addstr(2,13,"QUIT",curses.A_BOLD | curses.A_REVERSE)
        self.exit_win.addstr(2,12,"/",curses.A_BOLD)
        curses.curs_set(0)

        while True:
            key = self.exit_win.getch()
            if key == curses.KEY_LEFT:
                self.exit_win.addstr(2,6,"CANCEL",curses.A_BOLD | curses.A_REVERSE)
                self.exit_win.addstr(2,13,"QUIT",curses.A_BOLD)
                quit = False
            if key == curses.KEY_RIGHT:
                self.exit_win.addstr(2,6,"CANCEL",curses.A_BOLD)
                self.exit_win.addstr(2,13,"QUIT",curses.A_BOLD | curses.A_REVERSE)
                quit = True 
            if key == curses.KEY_ENTER or key == 10:
                break
            self.exit_win.refresh() 
        self.exit_win = None
        curses.curs_set(1)
        self.render()
        return quit

    def run(self):
        # Loop to handle user input
        while True:
            # Get user input
            key = self.stdscr.getch()
            if key != -1:
                if key == curses.KEY_BACKSPACE or key == 127:
                    self.prompt_text = self.prompt_text[:-1]
                elif key == curses.KEY_ENTER or key == 10:
                    if self.prompt_text == "":
                        continue
                    self.dungeon_master.get_ai_output(self.prompt_text)
                    self.situation_text = self.situation_text + f"Player:\n{self.prompt_text}\n"
                    self.situation_text = self.situation_text + f"Dungeon Master:\n{self.dungeon_master.get_situation()}\n"
                    self.update_output_text()
                    self.update_info()
                    self.prompt_text = ""
                elif key == 2:
                    self.is_stats = not self.is_stats
                    self.update_info()
                elif key == 27:
                    if self.exit_subwin():
                        break
                elif key == 18:                  
                    webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
                    sleep(1)
                    webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
                    sleep(1)
                    webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
                    sleep(1)
                    webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
                    sleep(1)
                    webbrowser.open_new_tab('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
                elif key == 410:
                    self.render()
                else:
                    self.prompt_text += chr(key)
                    with open("write.txt","w") as file:
                        file.write(str(key))
                self.update_input_text()
        curses.endwin()

def main(stdscr):
    app = DungeonsAndTerminals(stdscr)


# Run the program
if __name__ == "__main__":
    curses.wrapper(main)
