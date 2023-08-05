from re import match, sub

# colors \033[XXm
# background \033YYYm
colors = {
    "RED": (31, 101),
    "GREEN": (32, 102),
    "YELLOW": (33, 103),
    "BLUE": (34, 104),
    "MAGENTA": (35, 105),
    "CYAN": (36, 106),
    "WHITE": (97, 107),
    "GRAY": (37, 100),
    "BLACK": (30, 40),
}
# style \033[Zm
styles = {"BOLD": 1, "UNDERLINE": 4, "DIM": 2, "BLINK": 5, "REVERSE": 7, "HIDDEN": 8}


RESET = "\033[0m"
ERASE = "\x1b[1A\x1b[2K"


class ColoredFormat:

    color = None
    bg = None
    style = list()

    def set_color(self, color):
        base_color = colors.get(color.upper())
        self.color = base_color and f"\033[{base_color[0]}m" or f"\033[38;5;{color}m"

    def set_background(self, bg):
        base_bg = colors.get(bg.upper())
        self.bg = base_bg and f"\033[{base_bg[1]}m" or f"\033[48;5;{bg}m"

    def add_style(self, style):
        self.style.append(f"\033[{styles.get(style.upper())}m")

    def rm_color(self):
        self.color = None

    def rm_background(self):
        self.bg = None

    def rm_style(self):
        self.style.clear()

    def build_formatting(self, formatting):
        to_add = {"#": self.set_color, "@": self.add_style, "!": self.set_background}
        to_remove = {"#": self.rm_color, "@": self.rm_style, "!": self.rm_background}
        if match(r"/", formatting):
            if len(formatting) == 1:
                for _, func in to_remove.items():
                    func()
            for f in formatting[1:]:
                to_remove.get(f)()
            return
        fmt, arg = match(r"([#@!])(.+)", formatting).groups()
        to_add.get(fmt)(arg)

    def build(self, string):
        for fmt in string[1:-1].split():
            self.build_formatting(fmt)
        return f"{RESET}{self.color or ''}{self.bg or ''}{''.join(self.style)}"


def check_format(formatting):
    """Validity check"""
    if match(r"\[.+\]", formatting):
        formatting = formatting[1:-1]
    if " " in formatting:
        return all(check_format(single) for single in formatting.split())
    if (m := match(r"[!#](.+)", formatting)) :
        color = m.group(1)
        return color.upper() in colors or (color.isdigit() and 0 <= int(color) <= 256)
    if (m := match(r"@(.+)", formatting)) :
        return m.group(1).upper() in styles
    return match("/[#@!]*", formatting)


def paint(string, printing=False):
    """Return pretty formatted string"""
    fmt = ColoredFormat()
    formatting = (
        lambda x: check_format(x.group(1)) and fmt.build(x.group(1)) or x.group(1)
    )
    colored_return = sub(r"(\[[^\[]+?\])", formatting, string + "[/]")
    if not printing:
        return colored_return
    print(colored_return)


def ppaint(string):
    """Print the pretty formatted string"""
    return paint(string, printing=True)


def sample(complete=False):
    paint(
        "# ---- BASE COLORS ---- #\n"
        "Color:      [#red] RED [#green] GREEN [#yellow] YELLOW [#blue] BLUE [#magenta]"
        " MAGENTA [#cyan] CYAN [#white] WHITE [#gray] GRAY [#black] BLACK\n[/]"
        "Background: [#white !red] RED [!green] GREEN [!yellow] YELLOW [!blue] BLUE "
        "[!magenta] MAGENTA [!cyan] CYAN [#black !white] WHITE [#white !gray] GRAY "
        "[!black] BLACK [/]\n"
        "Styles:     [@bold] BOLD [/@ @underline] UNDERLINE [/@ @dim] DIM [/@ @blink]"
        " BLINK [/@ @reverse] REVERSE [!white /@  @hidden] HIDDEN [/]",
        True,
    )
    if complete:
        _sample_all()


def _sample_all():
    first_row = "".join(f"[#{i}]{i:>5}" for i in range(4))
    other_rows = "".join(
        f"[#{i+3}]{i+3:>5}" + ("\n" if not i % 6 and i != 252 else "")
        for i in range(1, 253)
    )
    print("\n\n# ---- INT COLORS ---- #")
    paint(f"{first_row}\n{other_rows}", True)
    first_row = "".join(f"[!{i}]{i:>5}" for i in range(4))
    other_rows = "".join(
        f"[!{i+3}]{i+3:>5}" + ("[/]\n" if not i % 6 and i != 252 else "")
        for i in range(1, 253)
    )
    print("\n\n# ---- INT BACKGROUNDS ---- #")
    paint(f"{first_row}[/]\n{other_rows}", True)


def erase(lines=1):
    print(ERASE * lines, end="")
