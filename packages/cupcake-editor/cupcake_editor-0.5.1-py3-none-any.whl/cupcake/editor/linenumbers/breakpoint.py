import tkinter as tk


class Breakpoint(tk.Label):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        self.config(text="●", font=("Consolas", 14), bg="#1e1e1e", fg="#1e1e1e", cursor="hand2", 
            borderwidth=0, width=2, height=1, pady=0, padx=0, relief=tk.FLAT)

        self.active = False
        self.hovered = False
        self.config_bindings()
    
    def config_bindings(self):
        self.bind("<Button-1>", self.on_click)
        # self.bind("<Button-3>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def redraw(self):
        if self.active:
            self.config(fg="#e51400")
            return 
        
        if self.hovered:
            self.config(fg="#6e1911")
        else:
            self.config(fg="#1e1e1e")
        

    def on_click(self, event):
        self.active = not self.active
        self.redraw()
    
    def on_enter(self, event):
        self.hovered = True
        self.redraw()

    def on_leave(self, event):
        self.hovered = False
        self.redraw()
