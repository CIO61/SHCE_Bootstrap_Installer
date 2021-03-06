import filecmp
import subprocess
import sys

import colorama
from colorama.ansi import Fore, Cursor
import msvcrt
import os

colorama.init()


exedir = os.path.dirname(sys.executable)
if "Stronghold_Crusader_Extreme.exe" not in os.listdir():
    sys.exit()

cgf = "\\CustomGraphics"
option_list = {folder: [f for f in os.listdir(f"{exedir}{cgf}\\{folder}")]
               for folder in os.listdir(f"{exedir}{cgf}")}

selection = {}


def check_selection():
    for key, val in option_list.items():
        keepcheck = True
        for j, item in enumerate(val):
            same = keepcheck and filecmp.cmp(f"{exedir}{cgf}\\{key}\\{item}", f"gm\\{key}.gm1")
            if same:
                keepcheck = False
                selection[key] = j
        if keepcheck:
            selection[key] = -1


def prepare_text():
    ret_text = ""
    for i, kvpair in enumerate(option_list.items()):
        _k, _v = kvpair
        item_txts = []
        for j, item in enumerate(_v):
            color = Fore.GREEN if selection[_k] == j else Fore.RED
            item_txts.append(f"{color}{item.rpartition('.')[0]}{Fore.RESET}")
        ret_text += f"[{Fore.CYAN}{i+1}{Fore.RESET}] {_k}: [{' '.join(item_txts)}]\n"
    return ret_text


def print_status(rewind=False):
    if rewind:
        print()
        print(Cursor.UP(len(selection)+4), end="")
    print(f"Custom Texture Settings ({Fore.GREEN}green{Fore.RESET} shows the currently active option)")
    print(prepare_text())
    print(f"[{Fore.CYAN}0{Fore.RESET}]: Exit")


def input_loop():
    skip = False
    ch = ""
    while ch.upper() not in ["0"]:
        ch = msvcrt.getwch()
        if ch == "à":
            skip = True
            continue
        if skip:
            ch = ""
            skip = False
            continue

        sel_keys = list(selection.keys())
        if ch in [str(n) for n in range(1, len(sel_keys)+1)]:
            category = sel_keys[int(ch)-1]
            selection[category] += 1
            selection[category] %= len(option_list[category])
            sel_idx = selection[category]
            file = option_list[category][sel_idx]
            subprocess.run(f"copy /Y {exedir}{cgf}\\{category}\\{file} gm\\{category}.gm1 > NUL", shell=True)

        print_status(rewind=True)


print(f"Welcome to custom graphic configurator.\n"
      f"Use {Fore.CYAN}number keys{Fore.RESET} on your keyboard to apply the options.\n")
check_selection()
print_status()
input_loop()
