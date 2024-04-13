import curses

def main(stdscr):
    # Set up the screen
    stdscr.clear()  # Clear the screen
    curses.use_default_colors();
    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Title
    title = "Dungeons and Terminals"
    title_len = len(title)
    title_x = (width - title_len) // 2
    stdscr.addstr(1, title_x, title, curses.A_BOLD)
    # Statistics

    stats_win = curses.newwin(height - 6, 20, 3, width - 22)
    stats_win.border()
    stats_win.addstr(1, 2, "Statistics")
    HEALTH = 50
    STAMINA = 79
    WILL_TO_LIVE = 0
    
    stats_y, stats_x = stats_win.getmaxyx()
    bar_height = stats_y - 5
    bar_width  = stats_x // 5
    #HEALTH
    stats_win.attron(curses.color_pair(1))
    health_bar_top = round((1 - HEALTH / 100) * bar_height)
    for y in range(stats_y - 3,health_bar_top + 2,-1):
        for x in range(bar_width):
            stats_win.addch(y,x + bar_width,curses.ACS_BOARD)
    stats_win.attroff(curses.color_pair(1))
    #STAMINA
    stats_win.attron(curses.color_pair(2))
    stamina_bar_top = round((1 - STAMINA / 100) * bar_height)
    for y in range(stats_y - 3,stamina_bar_top + 2,-1):
        for x in range(bar_width):
            stats_win.addch(y,x + 3 * bar_width,curses.ACS_BOARD)
    stats_win.attroff(curses.color_pair(2))

    # Input box
    input_box = curses.newwin(3, width - 25, 3, 2)
    input_box.border()
    input_box.addstr(1, 2, "Your action: ")
    input_box.nodelay(True)

    # Output box
    output_box = curses.newwin(height - 10, width - 25, 7, 2)
    output_box.border()
    output_box.addstr(1, 2, "Situation:")

    # Refresh windows
    stdscr.refresh()
    stats_win.refresh()
    output_box.refresh()
    input_box.refresh()

    user_input = ""
    # Loop to handle user input
    while True:
        # Get user input
        key = input_box.getch()
        if key != -1:

            if key == 127:
                user_input = user_input[:-1]
            elif key == 10:
                output_box.clear()
                output_box.border()
                output_box.addstr(1,2,"Situation:")
                output_box.addstr(2,2, user_input)
                output_box.refresh()
                user_input = ""
            else:
                user_input += chr(key)
            input_box.clear()
            input_box.border()
            input_box.addstr(1, 2, "Your action: " + user_input)
            input_box.refresh()


# Run the program
if __name__ == "__main__":
    curses.wrapper(main)
