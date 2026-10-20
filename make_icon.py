"""Generates shed_leds.ico (and a PNG preview). Run: python make_icon.py"""
import colorsys
from PIL import Image, ImageDraw

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# dark rounded tile
d.rounded_rectangle([0, 0, S - 1, S - 1], radius=230, fill=(28, 24, 54, 255))

# rainbow LED strip along the bottom
n = 7
w = (S - 2 * 150) / n
for i in range(n):
    r, g, b = (int(x * 255) for x in colorsys.hsv_to_rgb(i / n * 0.85, 0.85, 1))
    x0 = 150 + i * w
    d.rounded_rectangle([x0 + 6, 800, x0 + w - 6, 880], radius=40, fill=(r, g, b, 255))

# soft glow behind the bulb
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for k in range(12, 0, -1):
    a = int(14 * (13 - k) / 2)
    rad = 300 + k * 18
    gd.ellipse([512 - rad, 430 - rad, 512 + rad, 430 + rad], fill=(255, 210, 90, a))
img = Image.alpha_composite(img, glow)
d = ImageDraw.Draw(img)

# bulb: glass, base, highlight
d.ellipse([262, 150, 762, 650], fill=(255, 214, 80, 255))
d.polygon([(380, 590), (644, 590), (610, 700), (414, 700)], fill=(255, 214, 80, 255))
d.rounded_rectangle([404, 690, 620, 730], radius=20, fill=(190, 190, 205, 255))
d.rounded_rectangle([430, 735, 594, 775], radius=20, fill=(150, 150, 168, 255))
d.ellipse([330, 215, 430, 315], fill=(255, 246, 200, 255))

# cute face
dark = (60, 40, 20, 255)
d.ellipse([400, 360, 456, 430], fill=dark)
d.ellipse([568, 360, 624, 430], fill=dark)
d.arc([440, 410, 584, 530], start=20, end=160, fill=dark, width=18)
d.ellipse([350, 440, 410, 490], fill=(255, 140, 120, 200))
d.ellipse([614, 440, 674, 490], fill=(255, 140, 120, 200))

img.save("shed_leds_preview.png")
img.save("shed_leds.ico", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)])
