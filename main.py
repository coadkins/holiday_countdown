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

while True:
    a = 65
    while (a < 80):
        for display_indx, display in enumerate(DISPLAYS):
            display.clear()
            for i in range(0,4):
                display.set_character(chr(a + i +(4*display_indx)), i)
                display.draw()
        a += 1
        time.sleep(1)