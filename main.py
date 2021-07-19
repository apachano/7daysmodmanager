import tkinter as tk
import webbrowser
from mod import get_mods, Mod
from tk_helper import ScrollableFrame

library = {}


def scan_library():
    global library
    library = get_mods()


def mod_manager(parent):

    f_library = ScrollableFrame(parent, width=50)
    f_library.pack(side=tk.LEFT, fill=tk.Y)

    f_active = ScrollableFrame(parent, width=50)
    f_active.pack(side=tk.LEFT, fill=tk.Y)

    f_info = tk.Frame(parent, width=100)
    f_info.pack(side=tk.LEFT, fill=tk.Y)

    def library_list():
        for widget in f_library.scrollable_frame.winfo_children():
            widget.destroy()
        for key, mod in library.items():
            if not mod.is_active():
                mod_widget(f_library.scrollable_frame, mod)

    def active_list():
        for widget in f_active.scrollable_frame.winfo_children():
            widget.destroy()
        active = Mod.get_active_mods()
        for mod in active:
            mod_widget(f_active.scrollable_frame, mod)

    def mod_widget(_parent, _mod):
        def activate():
            _mod.activate()
            f_mod.destroy()
            active_list()

        def deactivate():
            _mod.deactivate()
            f_mod.destroy()
            library_list()

        def increment():
            _mod.inc_priority()
            active_list()

        def decrement():
            _mod.dec_priority()
            active_list()

        f_mod = tk.Frame(_parent, width=45, highlightbackground="black", highlightthickness=1)

        if _mod.is_active():
            f_actions = tk.Frame(f_mod, width=5)
            tk.Button(f_actions, width=5, text="^", command=increment).pack()
            tk.Button(f_actions, width=5, text="<", command=deactivate).pack()
            tk.Button(f_actions, width=5, text="v", command=decrement).pack()
            f_actions.pack(side=tk.LEFT)

        f_data = tk.Frame(f_mod, width=40)
        tk.Label(f_data, width=40, text=f'Mod: {_mod}').pack()
        tk.Label(f_data, width=40, text=f'    Author: {_mod.authors}').pack()
        f_data.bind("<Button-1>", lambda e: mod_info(_mod))
        for child in f_data.winfo_children():
            child.bind("<Button-1>", lambda e: mod_info(_mod))
        f_data.pack(side=tk.LEFT)

        if not _mod.is_active():
            f_actions = tk.Frame(f_mod, width=5)
            tk.Button(f_actions, width=5, text=">", command=activate).pack()
            f_actions.pack(side=tk.LEFT)

        f_mod.pack()

    def mod_info(_mod):
        for widget in f_info.winfo_children():
            widget.destroy()
        tk.Label(f_info, width=100, text=f'Mod: {_mod}').pack()
        tk.Label(f_info, width=100, text=f'    Author: {_mod.authors}').pack()
        tk.Label(f_info, width=100, text=f'    Version: {_mod.version}').pack()

        tk.Label(f_info, width=100, text='    Website:').pack()
        l_site = tk.Label(f_info, width=100, fg='Blue', text=_mod.website)
        l_site.bind('<Button-1>', lambda e: webbrowser.open(_mod.website))
        l_site.pack(side=tk.LEFT)

    active_list()
    library_list()
    for key, mod in library.items():
        mod_info(mod)
        break


def gui():
    scan_library()
    window = tk.Tk()
    tk.Label(text="Hello, Tkinter").pack()
    mod_manager(window)
    window.mainloop()


if __name__ == '__main__':
    gui()
