from .romaji2kana import convert
import curses
import sys
import shutil
import time
import random
import pkgutil
import string


def main():
    class _res:
        score = 0

    def scr(stdscr, res):
        if len(sys.argv) > 1:
            with open(sys.argv[1]) as f:
                data = f.read()
        else:
            data = pkgutil.get_data("typtrain", "assets/dic.csv").decode()
        qsts = []
        for d in data.strip().split("\n"):
            ds = d.split(",")
            qsts.append(["{} ({})".format(ds[0].strip(), ds[1].strip()), ds[1].strip()])
        qsts = random.sample(qsts, len(qsts))
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.clear()
        started = time.time()
        qsti = 0
        inp = ""
        combo = 1
        while True:
            if qsti >= len(qsts):
                qsts = random.sample(qsts, len(qsts))
                qsti = 0
            remaining = int(60 + started - time.time())
            ts = shutil.get_terminal_size()
            stdscr.addstr(0, 0, f"Score: {res.score}", curses.A_BOLD)
            stdscr.addstr(1, 0, f"Combo: {combo - 1}", curses.A_BOLD)
            stdscr.addstr(
                2, 0, f"Remaining: {remaining}s", curses.A_BOLD
            )
            try:
                stdscr.addstr(
                    int(ts[1] / 2) - 1,
                    int((ts[0] - len(qsts[qsti][0]) * 2 + 3) / 2),
                    qsts[qsti][0],
                    curses.A_BOLD,
                )
            except curses.error:
                qsti += 1
                continue
            if remaining <= 0:
                stdscr.clear()
                stdscr.addstr(0, 0, f"Score: {res.score}", curses.A_BOLD)
                stdscr.addstr(1, 0, "Press Enter to exit ...")
                stdscr.nodelay(False)
                while True:
                    ch = stdscr.getch()
                    if ch == 10:
                        break
                break
            ch = stdscr.getch()
            try:
                c = chr(ch)
            except Exception:
                c = ""
                continue
            if ch == 10:
                if convert(inp) == qsts[qsti][1]:
                    res.score += len(qsts[qsti][1]) * combo
                    qsti += 1
                    combo += 1
                else:
                    if inp:
                        combo = 1
                inp = ""
                stdscr.clear()
                continue
            if chr(ch) not in string.ascii_letters + "-":
                continue
            inp += c
            stdscr.clear()
            try:
                stdscr.addstr(int(ts[1] / 2) + 1, int((ts[0] - len(inp) - 1) / 2), inp)
            except curses.error:
                pass
            stdscr.refresh()

    res = _res()
    curses.wrapper(scr, res)
    print(f"Score: {res.score}")
    print("Share with \"#typtrain\"")
