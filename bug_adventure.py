#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════╗
║    MIA'S BUG GARDEN ADVENTURE                ║
║    *** 8-BIT TERMINAL EDITION ***            ║
║                                              ║
║    A pet project by Mia & Papa  :)           ║
╚══════════════════════════════════════════════╝

Controls:
  Arrow keys = move Mia
  Q          = quit
  ENTER      = confirm / next screen
"""

import curses
import time
import sys

# ─────────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────────
C_PLAYER  = 1
C_FRIEND  = 2
C_FLOWER  = 3
C_WALL    = 4
C_TREE    = 5
C_WEB     = 6
C_UI      = 7
C_TITLE   = 8
C_WIN     = 9
C_SCORE   = 10

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(C_PLAYER, curses.COLOR_RED,     -1)
    curses.init_pair(C_FRIEND, curses.COLOR_YELLOW,  -1)
    curses.init_pair(C_FLOWER, curses.COLOR_YELLOW,  -1)
    curses.init_pair(C_WALL,   curses.COLOR_GREEN,   -1)
    curses.init_pair(C_TREE,   curses.COLOR_GREEN,   -1)
    curses.init_pair(C_WEB,    curses.COLOR_WHITE,   -1)
    curses.init_pair(C_UI,     curses.COLOR_WHITE,   -1)
    curses.init_pair(C_TITLE,  curses.COLOR_YELLOW,  -1)
    curses.init_pair(C_WIN,    curses.COLOR_CYAN,    -1)
    curses.init_pair(C_SCORE,  curses.COLOR_MAGENTA, -1)

# ─────────────────────────────────────────────
#  MAPS  (each row must be the same width)
#  Symbols:
#   #  = hedge/wall     T  = tree
#   .  = grass          *  = flower (collect!)
#   @  = Mia's start    W  = spider web (slow!)
#   B  = Bee Buzzy      F  = Butterfly Bella
#   C  = Cricket Charlie
# ─────────────────────────────────────────────

LEVELS = [
    {
        "name":        "SUNNY MEADOW",
        "friend_char": "B",
        "friend_name": "BEE BUZZY",
        "intro":       [
            "Welcome to the SUNNY MEADOW!",
            "",
            "Bee Buzzy flew away this morning.",
            "He loves to collect honey from flowers!",
            "",
            "Collect the flowers (*) to get points.",
            "Watch out for spider webs (W) - they slow you down!",
        ],
        "win_msg": [
            "*** HOORAY! ***",
            "",
            "You found BEE BUZZY!",
            "He was busy collecting honey!",
            "Buzzy says: BZZZ BZZZ! Thank you Mia!",
        ],
        "map": [
            "####################",
            "#..................#",
            "#.*.*..T.....T.*..#",
            "#..................#",
            "#...W...........W.#",
            "#.....*.......*.#.#",  # NOTE: the rogue . before # is intentional indent
            "#..................#",
            "#..*...........B..#",
            "#..................#",
            "#...W...........W.#",
            "#..*..T.....T..*..#",
            "#..................#",
            "#@.................#",
            "#..................#",
            "####################",
        ],
    },
    {
        "name":        "FLOWER GARDEN",
        "friend_char": "F",
        "friend_name": "BUTTERFLY BELLA",
        "intro":       [
            "Welcome to the FLOWER GARDEN!",
            "",
            "Butterfly Bella loves to dance!",
            "She flutters from flower to flower.",
            "",
            "There are more flowers here!",
            "But more webs too... be careful!",
        ],
        "win_msg": [
            "*** WONDERFUL! ***",
            "",
            "You found BUTTERFLY BELLA!",
            "She was dancing in the flowers!",
            "Bella says: Flutter flutter! Thank you!",
        ],
        "map": [
            "####################",
            "#..................#",
            "#T.*..*..T..*..*T.#",
            "#..................#",
            "#.W.............W.#",
            "#.....*.......*.#.#",
            "#..................#",
            "#..*.......F...*..#",
            "#..................#",
            "#.W.............W.#",
            "#T.*..*..T..*..*T.#",
            "#..................#",
            "#..W...........W..#",
            "#@.................#",
            "####################",
        ],
    },
    {
        "name":        "EVENING GARDEN",
        "friend_char": "C",
        "friend_name": "CRICKET CHARLIE",
        "intro":       [
            "Welcome to the EVENING GARDEN!",
            "",
            "Cricket Charlie loves to sing at night!",
            "He hides in the dark corners of the garden.",
            "",
            "This is the hardest level!",
            "More webs and Charlie is hiding deep inside!",
        ],
        "win_msg": [
            "*** AMAZING! ***",
            "",
            "You found CRICKET CHARLIE!",
            "He was singing his cricket song!",
            "Charlie says: CRICK CRICK! Yay Mia!",
        ],
        "map": [
            "####################",
            "#..................#",
            "#T.W..*..T..*..WT.#",
            "#..................#",
            "#.*...........W...#",
            "#...W..........*..#",
            "#..........C......#",
            "#..*..W...........*#",
            "#.......W.........#",
            "#T.W..*..T..*..WT.#",
            "#..................#",
            "#.*...W.......W..*#",
            "#..W...........W..#",
            "#@.................#",
            "####################",
        ],
    },
]

# Normalize all maps so every row is the same length
for lvl in LEVELS:
    w = max(len(row) for row in lvl["map"])
    lvl["map"] = [row.ljust(w, '.') for row in lvl["map"]]
    lvl["map_w"] = w
    lvl["map_h"] = len(lvl["map"])

# ─────────────────────────────────────────────
#  TITLE SCREEN
# ─────────────────────────────────────────────

TITLE_ART = [
    r" ____  _   _  ____      ___   ____  ____  ____  _   _  ",
    r"|  _ \| | | |/ ___|    / _ \ |  _ \|  _ \| ___|| \ | | ",
    r"| |_) | | | | |  _    / /_\ \| |_) | | | |  _|  \  | | ",
    r"|  _ <| |_| | |_| |  /  ___  \  _ <| |_| | |___ |  \ | ",
    r"|_| \_\\___/ \____|  /_/     \_\___/|____/|_____||_| \_|",
]

TITLE_SUBTITLE = [
    "",
    "   .  *  M A G I C   G A R D E N  *  .   ",
    "      - - - 8 - B I T  E D I T I O N - - -",
    "",
    "    A pet project by MIA and PAPA  :)",
    "",
    "     Press ENTER to start the adventure!",
    "         Press Q any time to quit",
]

STORY_TEXT = [
    "",
    "  One sunny morning, little ladybug MIA woke up...",
    "",
    "  She looked around her cozy leaf-house. Something was wrong.",
    "  Her best friends had DISAPPEARED!",
    "",
    "  >> BEE BUZZY is lost in the Sunny Meadow!",
    "  >> BUTTERFLY BELLA flew into the Flower Garden!",
    "  >> CRICKET CHARLIE is hiding in the Evening Garden!",
    "",
    "  MIA must find all three friends!",
    "",
    "  CONTROLS:",
    "    Arrow Keys  =  Move Mia",
    "    Q           =  Quit",
    "",
    "    Press ENTER to begin!",
]

VICTORY_TEXT = [
    "",
    "  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *",
    "",
    "         Y O U   W O N !",
    "",
    "     Mia found ALL her friends!",
    "",
    "       BEE BUZZY   - found!",
    "   BUTTERFLY BELLA - found!",
    "   CRICKET CHARLIE - found!",
    "",
    "  What an amazing adventure, Mia! ",
    "",
    "  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *",
    "",
    "        Press ENTER to play again!",
    "        Press Q to quit.",
]

# ─────────────────────────────────────────────
#  HELPER: safe addstr
# ─────────────────────────────────────────────

def safe_addstr(win, y, x, text, attr=0):
    """Draw text but silently ignore if it's out of bounds."""
    h, w = win.getmaxyx()
    if y < 0 or y >= h:
        return
    if x < 0 or x >= w:
        return
    text = text[:max(0, w - x)]
    if not text:
        return
    try:
        win.addstr(y, x, text, attr)
    except curses.error:
        pass

# ─────────────────────────────────────────────
#  SCREEN: title
# ─────────────────────────────────────────────

def show_title(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Draw border
    try:
        stdscr.border()
    except curses.error:
        pass

    row = 2
    # ASCII art title
    for line in TITLE_ART:
        x = max(0, (w - len(line)) // 2)
        safe_addstr(stdscr, row, x, line, curses.color_pair(C_TITLE) | curses.A_BOLD)
        row += 1

    # Subtitle lines
    for line in TITLE_SUBTITLE:
        x = max(0, (w - len(line)) // 2)
        safe_addstr(stdscr, row, x, line, curses.color_pair(C_WIN) | curses.A_BOLD)
        row += 1

    # Animated bugs at bottom
    bugs_line = "  @  ~  B  F  C  ~  @  ~  B  F  C  ~  @  "
    x = max(0, (w - len(bugs_line)) // 2)
    safe_addstr(stdscr, h - 3, x, bugs_line, curses.color_pair(C_FRIEND) | curses.A_BOLD)

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (curses.KEY_ENTER, 10, 13):
            return True
        if key in (ord('q'), ord('Q')):
            return False


# ─────────────────────────────────────────────
#  SCREEN: story / info text
# ─────────────────────────────────────────────

def show_text_screen(stdscr, lines, title="", color=C_WIN):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    try:
        stdscr.border()
    except curses.error:
        pass

    if title:
        t = f"  {title}  "
        safe_addstr(stdscr, 1, (w - len(t)) // 2, t,
                    curses.color_pair(C_TITLE) | curses.A_BOLD)

    row = 3
    for line in lines:
        x = max(2, (w - len(line)) // 2) if line.strip() else 0
        safe_addstr(stdscr, row, x, line, curses.color_pair(color))
        row += 1
        if row >= h - 2:
            break

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (curses.KEY_ENTER, 10, 13):
            return True
        if key in (ord('q'), ord('Q')):
            return False


# ─────────────────────────────────────────────
#  DRAW MAP
# ─────────────────────────────────────────────

CELL_COLOR = {
    '#': (C_WALL,   curses.A_BOLD),
    'T': (C_TREE,   curses.A_BOLD),
    '*': (C_FLOWER, curses.A_BOLD),
    'W': (C_WEB,    curses.A_DIM),
    '.': (C_WALL,   curses.A_NORMAL),  # grass - low visibility
    ' ': (C_WALL,   curses.A_NORMAL),
}

CELL_DISPLAY = {
    '#': '#',
    'T': 'T',
    '*': '*',
    'W': 'W',
    '.': '.',
    ' ': ' ',
    '@': '@',
    'B': 'B',
    'F': 'F',
    'C': 'C',
}


def draw_map(win, game_map, player_x, player_y, friend_char, offset_x, offset_y):
    """Draw the game map centered on screen."""
    win.clear()
    h, w = win.getmaxyx()

    for row_i, row in enumerate(game_map):
        for col_i, cell in enumerate(row):
            sx = offset_x + col_i
            sy = offset_y + row_i
            if sx < 0 or sx >= w or sy < 0 or sy >= h:
                continue

            if col_i == player_x and row_i == player_y:
                # Draw Mia
                safe_addstr(win, sy, sx, '@',
                            curses.color_pair(C_PLAYER) | curses.A_BOLD)
            elif cell == '#':
                safe_addstr(win, sy, sx, '#',
                            curses.color_pair(C_WALL) | curses.A_BOLD)
            elif cell == 'T':
                safe_addstr(win, sy, sx, 'T',
                            curses.color_pair(C_TREE) | curses.A_BOLD)
            elif cell == '*':
                safe_addstr(win, sy, sx, '*',
                            curses.color_pair(C_FLOWER) | curses.A_BOLD)
            elif cell == 'W':
                safe_addstr(win, sy, sx, 'W',
                            curses.color_pair(C_WEB) | curses.A_DIM)
            elif cell in ('B', 'F', 'C'):
                safe_addstr(win, sy, sx, cell,
                            curses.color_pair(C_FRIEND) | curses.A_BOLD)
            else:
                # grass
                safe_addstr(win, sy, sx, '.',
                            curses.color_pair(C_WALL) | curses.A_DIM)


# ─────────────────────────────────────────────
#  DRAW HUD (status bar)
# ─────────────────────────────────────────────

def draw_hud(win, level_name, score, flowers_left, friend_name, message, web_slow):
    h, w = win.getmaxyx()

    # Top bar
    bar = f" LEVEL: {level_name}   SCORE: {score}   FLOWERS: {flowers_left} left "
    safe_addstr(win, 0, 0, bar.ljust(w), curses.color_pair(C_SCORE) | curses.A_BOLD)

    # Friend reminder
    hint = f" Find: {friend_name} "
    safe_addstr(win, 1, 0, hint.ljust(w), curses.color_pair(C_WIN))

    # Web slow indicator
    if web_slow > 0:
        warn = " *** SPIDER WEB! Moving slowly... *** "
        safe_addstr(win, 2, 0, warn.ljust(w), curses.color_pair(C_WEB) | curses.A_BOLD)

    # Bottom message bar
    if message:
        safe_addstr(win, h - 1, 0, f" {message} ".ljust(w),
                    curses.color_pair(C_WIN) | curses.A_BOLD)


# ─────────────────────────────────────────────
#  GAME LEVEL
# ─────────────────────────────────────────────

def run_level(stdscr, level_index):
    """Run one level. Returns True if completed, False if quit."""
    level = LEVELS[level_index]
    game_map = [list(row) for row in level["map"]]
    map_h = level["map_h"]
    map_w = level["map_w"]
    friend_char = level["friend_char"]

    # Find player start
    player_x, player_y = 1, 1
    for ry, row in enumerate(game_map):
        for rx, cell in enumerate(row):
            if cell == '@':
                player_x, player_y = rx, ry
                game_map[ry][rx] = '.'
                break

    # Count flowers
    total_flowers = sum(row.count('*') for row in game_map)
    flowers = total_flowers

    score = 0
    message = "Find your friend! Collect flowers for points!"
    web_slow = 0
    move_skip = 0  # slow-down counter

    stdscr.nodelay(True)
    stdscr.timeout(80)

    while True:
        h, w = stdscr.getmaxyx()

        # Compute map offset to center it
        hud_rows = 3
        map_area_h = h - hud_rows - 1
        map_area_w = w
        offset_x = max(0, (map_area_w - map_w) // 2)
        offset_y = hud_rows + max(0, (map_area_h - map_h) // 2)

        # Draw
        draw_map(stdscr, game_map, player_x, player_y,
                 friend_char, offset_x, offset_y)
        draw_hud(stdscr, level["name"], score, flowers,
                 level["friend_name"], message, web_slow)
        stdscr.refresh()

        key = stdscr.getch()

        # Slow down on webs
        if move_skip > 0:
            move_skip -= 1
            continue

        dx, dy = 0, 0
        if key == curses.KEY_UP:
            dy = -1
        elif key == curses.KEY_DOWN:
            dy = 1
        elif key == curses.KEY_LEFT:
            dx = -1
        elif key == curses.KEY_RIGHT:
            dx = 1
        elif key in (ord('q'), ord('Q')):
            return False, score
        else:
            continue

        nx, ny = player_x + dx, player_y + dy

        # Bounds check
        if nx < 0 or nx >= map_w or ny < 0 or ny >= map_h:
            continue

        cell = game_map[ny][nx]

        # Wall collision
        if cell == '#' or cell == 'T':
            message = "Oops! That's a wall!"
            continue

        # Web - slow down
        if cell == 'W':
            web_slow = 3
            move_skip = 4
            message = "Ugh! A spider web! Moving slowly..."
            player_x, player_y = nx, ny
            continue

        # Flower - collect
        if cell == '*':
            score += 10
            flowers -= 1
            game_map[ny][nx] = '.'
            message = f"Yay! +10 points! Score: {score}"

        # Friend - win!
        elif cell == friend_char:
            score += 50
            return True, score

        else:
            # Decay web slow
            if web_slow > 0:
                web_slow -= 1
            else:
                message = "Keep going! Find your friend!"

        player_x, player_y = nx, ny


# ─────────────────────────────────────────────
#  LEVEL COMPLETE SCREEN
# ─────────────────────────────────────────────

def show_level_win(stdscr, level_index, score):
    level = LEVELS[level_index]
    msg = level["win_msg"] + [
        "",
        f"  Flowers collected! Score so far: {score}",
        "",
        "  Press ENTER for the next level!",
    ]
    return show_text_screen(stdscr, msg, f"LEVEL {level_index + 1} COMPLETE!", C_WIN)


# ─────────────────────────────────────────────
#  MAIN GAME LOOP
# ─────────────────────────────────────────────

def main(stdscr):
    curses.curs_set(0)  # hide cursor
    init_colors()
    stdscr.keypad(True)

    while True:  # outer loop: allow restart
        # Title
        if not show_title(stdscr):
            break

        # Story
        if not show_text_screen(stdscr, STORY_TEXT, "THE STORY", C_WIN):
            break

        total_score = 0
        all_won = True

        for level_index in range(len(LEVELS)):
            level = LEVELS[level_index]

            # Level intro
            if not show_text_screen(
                stdscr,
                level["intro"],
                f"LEVEL {level_index + 1}: {level['name']}",
                C_WIN,
            ):
                all_won = False
                break

            # Run level
            stdscr.nodelay(False)
            won, level_score = run_level(stdscr, level_index)
            total_score += level_score

            if not won:
                all_won = False
                break

            # Level complete screen
            if not show_level_win(stdscr, level_index, total_score):
                all_won = False
                break

        if all_won:
            # Full victory!
            final = VICTORY_TEXT + [f"", f"  FINAL SCORE: {total_score}  "]
            if not show_text_screen(stdscr, final, "YOU WIN!!!", C_WIN):
                break
            # Loop back to title screen (outer while True)
        else:
            break  # player quit mid-game


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    print()
    print("Thanks for playing MIA'S BUG GARDEN ADVENTURE!")
    print("See you next time, Mia!  :)")
    print()
