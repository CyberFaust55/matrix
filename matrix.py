import curses
import random
import time

# Cytaty z Matrixa
quotes = [
    "Wake up, Neo...",
    "The Matrix has you.",
    "Follow the white rabbit.",
    "Knock, knock, Neo.",
    "There is no spoon.",
    "Free your mind.",
    "Choice is an illusion.",
    "Everything that has a beginning has an end.",
]

def matrix_effect(stdscr):
    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # głowa
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # ogon 1
    curses.init_pair(3, 28, curses.COLOR_BLACK)                  # ogon 2
    curses.init_pair(4, 22, curses.COLOR_BLACK)                  # ogon 3
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)   # cytaty

    stdscr.nodelay(True)
    stdscr.timeout(0)

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
    last_resize_check = time.time()
    last_quote_time = time.time()
    quote = random.choice(quotes)

    sh, sw = stdscr.getmaxyx()
    columns = sw
    drops = [random.randint(0, sh - 1) for _ in range(columns)]
    trail_length = 60      

    while True:
        current_time = time.time()

        # Sprawdzenie rozmiaru terminala co 2 sekundy
        if current_time - last_resize_check > 2:
            sh, sw = stdscr.getmaxyx()
            columns = sw
            if len(drops) != columns:
                drops = [random.randint(0, sh - 1) for _ in range(columns)]
            last_resize_check = current_time

        stdscr.erase()

        for i in range(columns):
            x = i
            y = drops[i]

            for j in range(trail_length):
                ch_y = y - j
                if 0 <= ch_y < sh:
                    # Migotanie liter
                    if random.random() < 0.05:
                        char = random.choice(chars)
                    else:
                        char = ' '

                    if j == 0:
                        color = curses.color_pair(1)
                        char = random.choice(chars)
                    elif j < trail_length / 3:
                        color = curses.color_pair(2)
                        char = random.choice(chars)
                    elif j < 2 * trail_length / 3:
                        color = curses.color_pair(3)
                    else:
                        color = curses.color_pair(4)

                    try:
                        stdscr.addstr(ch_y, x, char, color)
                    except curses.error:
                        pass

            # Reset kropli
            if y > sh + trail_length or random.random() > 0.98:
                drops[i] = 0
            else:
                drops[i] += 1

        # Wyświetlanie cytatu co 8 sekund
        if current_time - last_quote_time > 8:
            quote = random.choice(quotes)
            last_quote_time = current_time

        try:
            stdscr.addstr(sh - 2, max(0, int((sw - len(quote)) / 2)), quote, curses.color_pair(5))
        except curses.error:
            pass

        stdscr.refresh()
        time.sleep(0.05)

        try:
            key = stdscr.getch()
            if key == ord("q"):
                break
        except:
            pass

def main():
    curses.wrapper(matrix_effect)

if __name__ == "__main__":
    main()
