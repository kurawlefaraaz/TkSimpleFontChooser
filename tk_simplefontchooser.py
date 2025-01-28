try:
    from tkinter import Toplevel, StringVar, BooleanVar, IntVar
    from tkinter.ttk import Checkbutton, Frame, Label, Button, Style, Spinbox, Combobox
    from tkinter.font import Font, families, names
except ImportError:
    from Tkinter import Toplevel, StringVar, BooleanVar, IntVar
    from ttk import Checkbutton, Frame, Label, Button, Style, Spinbox, Combobox
    from tkFont import Font, families, names

from locale import getlocale

__version__ = "2.0.3" # If this simple font chooser is also accepted

# --- translation
EN = {"Cancel": "Cancel", "Bold": "Bold", "Italic": "Italic",
      "Underline": "Underline", "Overstrike": "Strikethrough"}
FR = {"Cancel": "Annuler", "Bold": "Gras", "Italic": "Italique",
      "Underline": "Souligné", "Overstrike": "Barré"}
IT = {"Cancel": "Annulla", "Bold": "Grassetto", "Italic": "Corsivo",
      "Underline": "Sottolineato", "Overstrike": "Barrato"}
RU = {"Cancel": "Отмена", "Bold": "Полужирный", "Italic": "Курсив",
      "Underline": "Подчеркнутый", "Overstrike": "Зачеркнутый"}
LANGUAGES = {"fr": FR, "en": EN, "it": IT, "ru": RU}

try:
    lang_code = getlocale()[0][:2]
    if lang_code in LANGUAGES:
        TR = LANGUAGES[lang_code]
    else:
        TR = LANGUAGES["en"]

except ValueError:
    TR = LANGUAGES["en"]

class SimpleFontChooser(Toplevel):
    
    def __init__(self, master, font:Font = None, text="Abcd", title="Font Chooser", **options):
        """
        Create a new FontChooser instance.

        Arguments:

            master : Tk or Toplevel instance
                master window

            font : Font
                ``Font`` object:

            text : str
                text to be displayed in the preview label

            title : str
                window title

            options : dict
                additional keyword arguments to be passed to ``Toplevel.__init__``
        """
        Toplevel.__init__(self, master, **options)
        self.title(title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # --- family list
        self.font_list = list(set(families()).union(names()))
        self.font_list.sort()
        
        if not font: self.font = Font(self, family="TkDefaultFont", size=10)
        else: self.font = font

        ### Font Family Select         
        self.font_family_option_selected = StringVar(self, self.font.cget('family'))
        family_menu = Combobox(self, textvariable=self.font_family_option_selected, values = self.font_list, height=10, state = 'readonly')
        family_menu.bind("<<ComboboxSelected>>", self.update_family)
        family_menu.grid(row=0, column=0, sticky="ew", pady=(10, 1), padx=(10, 0))

        ### Font Size Select
        self.font_size_selected = IntVar(self, self.font.cget('size'))
        font_size_spinbox = Spinbox(self, from_=0, textvariable=self.font_size_selected, to='infinity', command=self.update_size, state="readonly")
        
        font_size_spinbox.grid(row=0, column=1, sticky="ew",
                             pady=(10, 1), padx=(10, 0))

        ### Font Options
        options_frame = Frame(self, relief='groove', borderwidth=2)
        
        self.var_bold = BooleanVar(self, self.font.cget('weight') == "bold")
        b_bold = Checkbutton(options_frame, text=TR.get("Bold"), variable=self.var_bold, command=self.toggle_bold)
        b_bold.grid(row=0, column=0, padx=5)

        self.var_italic = BooleanVar(self, self.font.cget('slant') == "italic")
        b_italic = Checkbutton(options_frame, text=TR.get("Italic"), variable=self.var_italic, command=self.toggle_italic)
        b_italic.grid(row=0, column=1, padx=5)

        self.var_underline = BooleanVar(self, self.font.cget('underline'))
        b_underline = Checkbutton(options_frame, text=TR.get("Underline"), variable=self.var_underline, command=self.toggle_underline)
        b_underline.grid(row=0, column=2, padx=5)

        self.var_overstrike = BooleanVar(self, self.font.cget('overstrike'))
        b_overstrike = Checkbutton(options_frame, text=TR.get("Overstrike"), variable=self.var_overstrike, command=self.toggle_overstrike)
        b_overstrike.grid(row=0, column=3, padx=5)

        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        options_frame.grid_columnconfigure(2, weight=1)
        options_frame.grid_columnconfigure(3, weight=1)
        options_frame.grid(row=1, column=0, columnspan=2,
                           padx=10, pady=10, ipadx=10, sticky="ew")
    
        ### Preview Label
        style = Style(self)
        style.configure("prev.TLabel", background="white")
    
        self.preview = Label(self, relief="groove", style="prev.TLabel",
                             text=text, font=self.font,
                             anchor="center")
        self.preview.grid(row=2, column=0, columnspan=5, sticky="ew",
                          padx=10, pady=(0, 10), ipadx=4, ipady=4)
        
        ### Buttons
        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10), padx=10)
        Button(button_frame, text="Ok",
               command=self.ok_func).grid(row=0, column=0, padx=4, sticky='ew')
        Button(button_frame, text="Cancel",
               command=self.cancel_func).grid(row=0, column=1, padx=4, sticky='ew')
    
    def update_family(self, event):
        self.font.configure(family=self.font_family_option_selected.get())

    def update_size(self):
        self.font.configure(size = self.font_size_selected.get())

    def toggle_bold(self):
        """Update font preview weight."""
        b = self.var_bold.get()
        self.font.configure(weight=["normal", "bold"][b])

    def toggle_italic(self):
        """Update font font slant."""
        b = self.var_italic.get()
        self.font.configure(slant=["roman", "italic"][b])

    def toggle_underline(self):
        """Update font preview underline."""
        b = self.var_underline.get()
        self.font.configure(underline=b)

    def toggle_overstrike(self):
        """Update font preview overstrike."""
        b = self.var_overstrike.get()
        self.font.configure(overstrike=b)
    
    def cancel_func(self): 
        self.font = None
        self.destroy()

    def ok_func(self): self.destroy()

    def get_result(self):
        return self.font
        
def askfont(master=None, text="Abcd", title="Font Chooser", font=None):
    """
    Open the font chooser and return a dictionary of the font properties.

    General Arguments:

        master : Tk or Toplevel instance
            master window

        text : str
            sample text to be displayed in the font chooser

        title : str
            dialog title

    Font arguments:

        family : str
            font family

        size : int
            font size

        slant : str
            "roman" or "italic"

        weight : str
            "normal" or "bold"

        underline : bool
            whether the text is underlined

        overstrike : bool
            whether the text is overstriked

    Output: Font Object

    """
    chooser = SimpleFontChooser(master, font, text, title)
    chooser.wait_window(chooser)
    return chooser.get_result()


if __name__ == "__main__":
    """Example."""
    from tkinter import Tk


    root = Tk()
    style = Style(root)
    bg = style.lookup("TLabel", "background")
    root.configure(bg=bg)
    label = Label(root, text='Chosen font: ')
    label.pack(padx=10, pady=(10, 4))

    def callback():
        font = askfont(root, title="Choose a font", text=label.cget('text'))
        if font:
            font_str = f"{font.cget('family')} {font.cget('size')} {font.cget('weight')} {font.cget('slant')}"
            if font.cget('underline'):
                font_str += ' underline'
            if font.cget('overstrike'):
                font_str += ' overstrike'

            label.configure(font=font,
                            text='Chosen font: ' + font_str)

    Button(root, text='Font Chooser',
           command=callback).pack(padx=10, pady=(4, 10))
    root.mainloop()
