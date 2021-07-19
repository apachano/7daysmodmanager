import tkinter as tk
from mod import get_mods, Mod
from tk_helper import ScrollableFrame

library = {}


def scan_library():
    global library
    library = get_mods()


def mod_manager(parent):
    def library_list():
        for key, mod in library.items():
            if not mod.is_active():
                mod_widget(f_library.scrollable_frame, mod)
        f_library.pack(side=tk.LEFT)

    def active_list():
        active = Mod.get_active_mods()
        for mod in active:
            mod_widget(f_active.scrollable_frame, mod)
        f_active.pack(side=tk.LEFT)

    def mod_widget(_parent, _mod):
        def activate(event, m):
            m.activate()
            event.widget.master.master.destroy()
            mod_widget(f_active.scrollable_frame, m)

        def deactivate(event, m):
            m.deactivate()
            event.widget.master.master.destroy()
            mod_widget(f_library.scrollable_frame, m)

        def increment(event, m):
            m.inc_priority()
            for mod in f_active.scrollable_frame.winfo_children():
                mod.destroy()
            active_list()

        def decrement(event, m):
            m.dec_priority()
            for mod in f_active.scrollable_frame.winfo_children():
                mod.destroy()
            active_list()

        f_mod = tk.Frame(_parent, width=45, highlightbackground="black", highlightthickness=1)

        if _mod.is_active():
            f_actions = tk.Frame(f_mod, width=5)
            btn_inc = tk.Button(f_actions, width=5, text="^")
            btn_inc.bind("<Button-1>", lambda event: increment(event, _mod))
            btn_inc.pack()
            btn_deactivate = tk.Button(f_actions, width=5, text="<")
            btn_deactivate.bind("<Button-1>", lambda event: deactivate(event, _mod))
            btn_deactivate.pack()
            btn_dec = tk.Button(f_actions, width=5, text="v")
            btn_dec.bind("<Button-1>", lambda event: decrement(event, _mod))
            btn_dec.pack()
            f_actions.pack(side=tk.LEFT)

        f_data = tk.Frame(f_mod, width=40)
        tk.Label(f_data, width=40, text=f'Mod: {_mod}').pack()
        tk.Label(f_data, width=40, text=f'    Author: {_mod.authors}').pack()
        f_data.pack(side=tk.LEFT)

        if not _mod.is_active():
            f_actions = tk.Frame(f_mod, width=5)
            btn_activate = tk.Button(f_actions, width=5, text=">")
            btn_activate.bind("<Button-1>", lambda event: activate(event, _mod))
            btn_activate.pack()
            f_actions.pack(side=tk.LEFT)

        f_mod.pack()

    f_library = ScrollableFrame(parent, width=50)
    f_active = ScrollableFrame(parent, width=50)

    library_list()
    active_list()


def gui():
    scan_library()
    window = tk.Tk()
    tk.Label(text="Hello, Tkinter").pack()
    mod_manager(window)
    window.mainloop()


if __name__ == '__main__':
    gui()
