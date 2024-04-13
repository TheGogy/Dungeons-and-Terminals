import curses
import sys

WILL_TO_LIVE = 0


class DungeonsAndTerminals():
    def __init__(self,stdscr):
        # Set up the screen
        self.stdscr = stdscr
        self.init_main()
        self.init_info()
        self.init_output()
        self.init_input()
        self.run()

    def init_main(self):
        self.stdscr.clear()  # Clear the screen
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
        self.HEALTH = 50
        self.STAMINA = 79
        self.is_stats = True
        self.info_win = curses.newwin(self.height - 6, 20, 3, self.width - 22)
        self.update_info()

    def update_info(self): 
        self.info_win.clear() 
        self.info_win.border()
        if self.is_stats is True:
            self.update_statistics()
        else:
            pass
        self.info_win.refresh()

    def update_statistics(self):
        self.info_win.addstr(1, 2, "Statistics")
        info_y, info_x = self.info_win.getmaxyx()
        bar_height = info_y - 5
        bar_width  = info_x // 5
        #HEALTH
        self.info_win.attron(curses.color_pair(1))
        health_bar_top = round((1 - self.HEALTH / 100) * bar_height)
        for y in range(info_y - 3,health_bar_top + 2,-1):
            for x in range(bar_width):
                self.info_win.addch(y,x + bar_width,curses.ACS_BOARD)
        self.info_win.attroff(curses.color_pair(1))
        #STAMINA
        self.info_win.attron(curses.color_pair(2))
        stamina_bar_top = round((1 - self.STAMINA / 100) * bar_height)
        for y in range(info_y - 3,stamina_bar_top + 2,-1):
            for x in range(bar_width):
                self.info_win.addch(y,x + 3 * bar_width,curses.ACS_BOARD)
        self.info_win.attroff(curses.color_pair(2))

    def init_input(self):
        # Input box
        self.input_box = curses.newwin(3, self.width - 25, 3, 2)
        self.input_box.border()
        self.input_box.addstr(1, 2, "Your action: ")
        self.input_box.nodelay(True)
        self.input_box.refresh()

    def init_output(self):
        # Output box
        self.output_box = curses.newwin(self.height - 10, self.width - 25, 7, 2)
        self.output_box.border()
        self.output_box.addstr(1, 2, "Situation:")
        self.output_box.refresh()

    def run(self):
        # Refresh windows
        user_input = ""
        # Loop to handle user input
        while True:
            # Get user input
            key = self.input_box.getch()
            if key != -1:
                if key == 127:
                    user_input = user_input[:-1]
                elif key == 10:
                    self.output_box.clear()
                    self.output_box.border()
                    self.output_box.addstr(1,2,"Situation:")
                    self.output_box.addstr(2,2, user_input)
                    self.output_box.refresh()
                    user_input = ""
                else:
                    user_input += chr(key)
                self.input_box.clear()
                self.input_box.border()
                self.input_box.addstr(1, 2, "Your action: " + user_input)
                self.input_box.refresh()

def main(stdscr):
        
    app = DungeonsAndTerminals(stdscr)


# Run the program
if __name__ == "__main__":
    curses.wrapper(main)
