import tkinter as tk

from .entrybox import EntryBox
from .button import Button
from .findbox import FindBox
from .replacebox import ReplaceBox
from .results import FindResults
from .togglew import ToggleWidget
from .container import FindReplaceContainer

from .find_replace import FinderReplacer


class FindReplace(tk.Toplevel):
    def __init__(self, master, tw, state=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.tw = tw

        self.state = state
        self.font = self.master.font

        if not state:
            self.withdraw()

        self.overrideredirect(True)
        self.config(bg="#454545")

        self.togglew = ToggleWidget(self)
        self.container = FindReplaceContainer(self)

        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.togglew.grid(row=0, column=0, sticky=tk.NS, padx=(2, 0))
        self.container.grid(row=0, column=1, sticky=tk.NSEW)

        self.config_bindings()

    def config_bindings(self, *args):
        self.container.find_entry.entry.bind("<Configure>", self.do_find)
    
    def toggle_replace(self, state):
        self.container.toggle_replace(state)

    def do_find(self, *args):
        print(self.container.get_term())
        # self.master.highlighter.highlight_pattern(self.container.find_entry.entry.get())
    
    def refresh_geometry(self, *args):
        self.update_idletasks()
        self.geometry("+{}+{}".format(*self.master.cursor_screen_location()))

    def show(self, pos):
        self.state = True
        self.update_idletasks()
        self.geometry("+{}+{}".format(*pos))
        self.deiconify()
        self.master.find_replace_active = True

    def hide(self, *args):
        self.state = False
        self.withdraw()
        self.master.find_replace_active = False
    
    def reset(self, *args):
        ...
    
