"""Click-button window for the shed LED strip. Run: python shed_leds_gui.py"""
import colorsys, json, os, threading, time
import tkinter as tk
from tkinter import colorchooser
import tinytuya

COLOURS = {
    "Red": (255, 0, 0), "Green": (0, 255, 0), "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0), "Orange": (255, 90, 0), "Purple": (128, 0, 255),
    "Pink": (255, 40, 120), "Cyan": (0, 255, 255),
}

cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "leds_config.json"), encoding="utf-8-sig"))
d = tinytuya.BulbDevice(cfg["id"], cfg["ip"], cfg["key"], version=cfg["version"])
lock = threading.Lock()
rainbow_on = threading.Event()

HERE = os.path.dirname(os.path.abspath(__file__))
try:  # own taskbar identity so Windows shows our icon instead of Python's
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("shed.leds.gui")
except Exception:
    pass

root = tk.Tk()
root.title("Shed LEDs")
try:
    root.iconbitmap(os.path.join(HERE, "shed_leds.ico"))
except tk.TclError:
    pass
root.resizable(False, False)
status = tk.StringVar(value="Ready")


def run(fn, *args):
    """Run a device call off the UI thread so the window never freezes."""
    def work():
        rainbow_on.clear()
        try:
            with lock:
                fn(*args)
            status.set("OK")
        except Exception as e:
            status.set("Error: %s" % e)
    threading.Thread(target=work, daemon=True).start()


def set_rgb(rgb):
    d.turn_on()
    d.set_colour(*rgb)


def pick_colour():
    rgb, _ = colorchooser.askcolor(title="Pick a colour")
    if rgb:
        run(set_rgb, tuple(int(x) for x in rgb))


def set_white():
    d.turn_on()
    d.set_white_percentage(brightness=int(bright.get()))


def toggle_rainbow():
    if rainbow_on.is_set():
        rainbow_on.clear()
        status.set("Rainbow stopped")
        return

    def loop():
        rainbow_on.set()
        status.set("Rainbow running")
        h = 0.0
        try:
            with lock:
                d.turn_on()
            while rainbow_on.is_set():
                r, g, b = (int(x * 255) for x in colorsys.hsv_to_rgb(h, 1, 1))
                with lock:
                    d.set_colour(r, g, b, nowait=True)
                h = (h + 0.02) % 1
                time.sleep(0.3)
        except Exception as e:
            rainbow_on.clear()
            status.set("Error: %s" % e)
    threading.Thread(target=loop, daemon=True).start()


pad = {"padx": 6, "pady": 4}
top = tk.Frame(root); top.pack(**pad)
tk.Button(top, text="ON", width=10, bg="#4caf50", fg="white", command=lambda: run(d.turn_on)).pack(side="left", **pad)
tk.Button(top, text="OFF", width=10, bg="#e53935", fg="white", command=lambda: run(d.turn_off)).pack(side="left", **pad)

grid = tk.Frame(root); grid.pack(**pad)
for i, (name, rgb) in enumerate(COLOURS.items()):
    hexcol = "#%02x%02x%02x" % rgb
    fg = "black" if sum(rgb) > 380 else "white"
    tk.Button(grid, text=name, width=9, bg=hexcol, fg=fg,
              command=lambda r=rgb: run(set_rgb, r)).grid(row=i // 4, column=i % 4, **pad)

more = tk.Frame(root); more.pack(**pad)
tk.Button(more, text="Custom colour...", command=pick_colour).pack(side="left", **pad)
tk.Button(more, text="White", command=lambda: run(set_white)).pack(side="left", **pad)
tk.Button(more, text="Rainbow on/off", command=toggle_rainbow).pack(side="left", **pad)

tk.Label(root, text="Brightness").pack()
bright = tk.Scale(root, from_=1, to=100, orient="horizontal", length=300)
bright.set(100)
bright.pack(**pad)
bright.bind("<ButtonRelease-1>", lambda e: run(d.set_brightness_percentage, int(bright.get())))

tk.Label(root, textvariable=status, fg="gray").pack(pady=(0, 6))
root.mainloop()
