import tkinter as tk


class Scrollbar(tk.Frame):
    def __init__(self, master, textw, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        
        self.tw = textw
        self.font = ("Arial", 1, "bold")

        self.config(bg="#252526", highlightthickness=0, padx=1)
        self.cw = tk.Canvas(self, bg="#1e1e1e", width=15, highlightthickness=0)
        self.cw.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.slider_image = tk.PhotoImage(data="""iVBORw0KGgoAAAANSUhEUgAAAG4AAABFCAYAAACrMNMO
        AAAACXBIWXMAAABfAAAAXwEqnu0dAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAMBJRE
        FUeJzt0UENwCAAwMAxLajjhwOkz8M+pMmdgiYda5/5kPPeDuAf46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo
        46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46
        KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIuyrgo46KMizIu6gNeAwIJ
        26ERewAAAABJRU5ErkJggg==""")

        self.cw.create_image(0, 0, image=self.slider_image, anchor=tk.NW, tag="slider")

        self.extra_y = 10
        self.y_top_lim = 0
        self.drag_data = {"y": 0, "item": None}
        self.yvalue = 0

        self.cw.tag_bind("slider", "<ButtonPress-1>", self.drag_start)
        self.cw.tag_bind("slider", "<ButtonRelease-1>", self.drag_stop)
        self.cw.tag_bind("slider", "<B1-Motion>", self.drag)

        if textw:
            self.redraw()

    def attach(self, textw):
        self.tw = textw

    def redraw(self):
        self.y_bottom_lim = int(self.tw.index(tk.END).split(".")[0]) * 2 + self.extra_y
    
    def drag_start(self, event):
        self.drag_data["item"] = self.cw.find_closest(event.x, event.y)[0]
        self.drag_data["y"] = event.y

    def drag_stop(self, event):
        self.drag_data["item"] = None
        self.drag_data["y"] = 0

    def drag(self, event):
        item = self.drag_data["item"]
        if item != 1:
            return

        delta_y = event.y - self.drag_data["y"]
        self.cw.move(item, 0, delta_y)
        self.drag_data["y"] = event.y

        self.yvalue = y = self.cw.coords(item)[1]
        if y <= self.y_top_lim:
            self.cw.move("slider", 0, -(y - self.y_top_lim))
        elif y >= self.y_bottom_lim:
            self.cw.move("slider", 0, -(y - self.y_bottom_lim))

        self.tw.yview(int(y / self.cw.winfo_height() * 100))
        self.tw.master.redraw_ln()
