"""Control the shed LED strip locally (Tuya v3.3). Usage: python shed_leds.py <command> [args]"""
import argparse, colorsys, json, os, time
import tinytuya

COLOURS = {
    "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "orange": (255, 90, 0), "purple": (128, 0, 255),
    "pink": (255, 40, 120), "cyan": (0, 255, 255),
}

cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "leds_config.json"), encoding="utf-8-sig"))
d = tinytuya.BulbDevice(cfg["id"], cfg["ip"], cfg["key"], version=cfg["version"])

p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("on")
sub.add_parser("off")
sub.add_parser("status")
sub.add_parser("rainbow")
c = sub.add_parser("colour"); c.add_argument("value", help="name (%s) or R,G,B e.g. 255,0,128" % ", ".join(COLOURS))
b = sub.add_parser("brightness"); b.add_argument("percent", type=int)
w = sub.add_parser("white"); w.add_argument("percent", type=int, nargs="?", default=100)
a = p.parse_args()

if a.cmd == "on": d.turn_on()
elif a.cmd == "off": d.turn_off()
elif a.cmd == "status": print(d.status())
elif a.cmd == "colour":
    rgb = COLOURS.get(a.value.lower()) or tuple(int(x) for x in a.value.split(","))
    d.turn_on(); d.set_colour(*rgb)
elif a.cmd == "brightness": d.set_brightness_percentage(max(1, min(100, a.percent)))
elif a.cmd == "white": d.turn_on(); d.set_white_percentage(brightness=max(1, min(100, a.percent)))
elif a.cmd == "rainbow":
    d.turn_on()
    print("Rainbow running - Ctrl+C to stop")
    h = 0.0
    try:
        while True:
            r, g, b_ = (int(x * 255) for x in colorsys.hsv_to_rgb(h, 1, 1))
            d.set_colour(r, g, b_, nowait=True)
            h = (h + 0.02) % 1; time.sleep(0.3)
    except KeyboardInterrupt:
        pass
