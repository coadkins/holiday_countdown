# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33Segment14

# Configured for the Raspberry Pi Pico -- update for your own setup
i2c = I2C(0, scl=Pin(23), sda=Pin(22))
# initalize display
DISPLAYS = [
    HT16K33Segment14(i2c, 0x70),
    HT16K33Segment14(i2c, 0x71),
    HT16K33Segment14(i2c, 0x72)
]

for display in DISPLAYS:
    display.set_brightness(5)
    display.clear()
    display.draw()

message = "Merry Christmas"
scroll = range(0, len(message) - 12 + 1)

while True:
    for i in scroll:
        for display_indx, display in enumerate(DISPLAYS):
            display.clear()
            for c in range(0,4):
                display.set_character(message[i+c + (4*display_indx)], c)
                display.draw()
        time.sleep(1)