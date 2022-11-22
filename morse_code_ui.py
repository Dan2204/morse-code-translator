import os
import tkinter as tk
from mc import MORSE_CODE
from tk_ui_helper_functions import set_window_position

THEME_COLOR = "#375362"
DEFAULT_FONT = ("Ariel", 20, "normal")
ERROR_FONT = ("Ariel", 17, "italic")
TRANSLATION_FONT = ("Ariel", 17, "normal")
LARGE_FONT = ("Ariel", 30, "normal")
SMALL_FONT = ("Ariel", 12, "normal")
DEFAULT_WIDTH = 650
DEFAULT_HEIGHT = 400
DEFAULT_TITLE = "Morse Code Translator"
DEFAULT_WINDOW_POSITION = "center"


class MorseCodeUi:
    abs = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, **kw):
        # BASE SET UP:
        self.win = tk.Tk()
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.title = DEFAULT_TITLE
        self.win_pos = kw["position"] if kw.get("position") else DEFAULT_WINDOW_POSITION
        self.pos = set_window_position(tk=self.win, width=self.width, height=self.height, position=self.win_pos)
        self.win.geometry(self.pos)
        self.win.title(self.title)
        # UI SET UP:
        self.images = {}
        self._set_img_path("images/mc.png", "btn_img")
        self.win.config(bg=THEME_COLOR, padx=50, pady=50)
        self._set_labels()
        self._set_buttons()
        self._set_entries()
        self._render_widgets()
        self.win.resizable(False, False)
        self.win.mainloop()

    # ------------------------- FUNCTIONALITY ------------------------- #

    def _translate(self):
        text = self.text_entry.get().upper()
        code = self.code_entry.get()
        if text and code:
            self.error_label.config(text="Please clear one of the fields.", fg="#f95e5e", font=ERROR_FONT)
        elif not text and not code:
            self.error_label.config(text="Please fill one of the fields.", fg="#f95e5e", font=ERROR_FONT)
        else:
            if text:
                try:
                    translation = "   ".join(
                        [" ".join([MORSE_CODE[letter] for letter in word]) for word in text.split()])
                    self.error_label.config(text=f"Translation: {translation}", fg="white", font=TRANSLATION_FONT)
                    self.code_var.set(translation)
                except KeyError as e:
                    self.error_label.config(text="Invalid Text", fg="#f95e5e", font=ERROR_FONT)
                    print(e)
            else:
                try:
                    breakdown = [word.split(' ') for word in code.split('   ')]
                    translation = " ".join(
                        ["".join([list(MORSE_CODE.keys())[list(MORSE_CODE.values()).index(letter)] for letter in word])
                         for
                         word in breakdown])
                    self.error_label.config(text=f"Translation: {translation}", fg="white", font=TRANSLATION_FONT)
                    self.text_var.set(translation)
                except ValueError as e:
                    self.error_label.config(text=f"Invalid Code: {e} isn't morse code.", fg="#f95e5e", font=ERROR_FONT)

    # ------------------------- TK UI ------------------------- #

    @staticmethod
    def on_enter(e):
        e.widget.config(highlightbackground='#3e8abc', fg='white')

    @staticmethod
    def on_leave(e):
        e.widget.config(highlightbackground='white', fg='black')

    def _set_img_path(self, path: str, ref: str):
        self.images[ref] = tk.PhotoImage(file=os.path.join(self.abs, path))

    def _set_labels(self):
        # CREATE:
        self.text_label = tk.Label(text="Text:", font=DEFAULT_FONT)
        self.code_label = tk.Label(text="Morse Code:", font=DEFAULT_FONT)
        self.error_label = tk.Label(text="", font=ERROR_FONT)
        self.sub_title_label = tk.Label(text="Enter the text or code you wish to translate...", font=DEFAULT_FONT)
        self.title_label = tk.Label(text="Morse Code Translator", font=LARGE_FONT)
        instructions = "When entering morse code, use a single space between letters and 3 spaces between words."
        self.instructions_label = tk.Label(text=instructions, font=SMALL_FONT)
        # CONFIGURE:
        self.text_label.config(bg=THEME_COLOR, fg="white")
        self.code_label.config(bg=THEME_COLOR, fg="white")
        self.error_label.config(bg=THEME_COLOR, fg="#f95e5e")
        self.sub_title_label.config(bg=THEME_COLOR, fg="white")
        self.title_label.config(bg=THEME_COLOR, fg="white", justify="center")
        self.instructions_label.config(bg=THEME_COLOR, fg="white")

    def _set_buttons(self):
        # CREATE:
        self.translate_btn = tk.Button(image=self.images["btn_img"], highlightthickness=0, command=self._translate)
        # CONFIGURE:
        self.translate_btn.config(padx=1, pady=1)
        self.translate_btn.bind("<Enter>", self.on_enter)
        self.translate_btn.bind("<Leave>", self.on_leave)

    def _set_entries(self):
        # CREATE:
        self.text_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self.text_entry = tk.Entry(textvariable=self.text_var)
        self.code_entry = tk.Entry(textvariable=self.code_var)
        # CONFIGURE:
        self.text_entry.focus()

    def _render_widgets(self)
        self.text_label.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.code_label.grid(row=3, column=0, sticky=tk.E)
        self.error_label.grid(row=4, column=0, columnspan=3, sticky=tk.E + tk.W, pady=10)
        self.sub_title_label.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        self.title_label.grid(row=0, column=0, columnspan=3, sticky=tk.E + tk.W, pady=10)
        self.instructions_label.grid(row=5, column=0, columnspan=3, sticky=tk.E + tk.W)
        self.translate_btn.grid(row=2, column=2, rowspan=2, sticky="nsew", pady=5)
        self.text_entry.grid(row=2, column=1, padx=10)
        self.code_entry.grid(row=3, column=1)
