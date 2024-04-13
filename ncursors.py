import curses

def main(stdscr):
    # Set up the screen
    stdscr.clear()  # Clear the screen
    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    # Title
    title = "Dungeons and Terminals"
    title_len = len(title)
    title_x = (width - title_len) // 2
    stdscr.addstr(1, title_x, title, curses.A_BOLD)

    # Input box
    input_box = curses.newwin(3, width - 25, 3, 2)
    input_box.border()
    input_box.addstr(1, 2, "Your action: ")
    input_box.nodelay(True)
    # Output box
    output_box = curses.newwin(height - 10, width - 25, 7, 2)
    output_box.border()
    output_box.addstr(1, 2, "Situation:")

    # Statistics
    stats_win = curses.newwin(height - 6, 20, 3, width - 22)
    stats_win.border()
    stats_win.addstr(1, 2, "Statistics")

    # Refresh windows
    stdscr.refresh()
    input_box.refresh()
    output_box.refresh()
    stats_win.refresh()

    user_input = ""
    # Loop to handle user input
    while True:
        # Get user input
        key = input_box.getch()
        if key != -1:

            if key == ord('q'):  # Quit if 'q' is pressed
                break 
            elif key == 127:
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
