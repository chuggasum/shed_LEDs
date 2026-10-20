# shed_LEDs

Local (LAN) control of a Tuya / Smart Life WiFi LED strip from a PC, using [tinytuya](https://github.com/jasonacox/tinytuya).

## Setup
1. `pip install tinytuya`
2. Get your device ID and local key: create a project at iot.tuya.com (data centre matching your app region), link your Smart Life account, then run `python -m tinytuya wizard`.
3. Copy `leds_config.example.json` to `leds_config.json` and fill in the device ID, local key and the strip's IP (protocol version 3.3). This file is git-ignored - never commit it.

## Use
- Window: double-click `Shed LEDs.bat` or run `python shed_leds_gui.py`
- Command line: `python shed_leds.py on | off | status | colour red | colour 255,0,128 | brightness 40 | white | rainbow`

The strip accepts one local connection at a time, so close the Smart Life app if commands fail.
