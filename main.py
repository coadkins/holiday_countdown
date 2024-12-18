# IMPORTS
import utime as time
from machine import I2C, Pin, RTC
from ht16k33 import HT16K33Segment14

# Configured for the Raspberry Pi Pico -- update for your own setup
i2c = I2C(0, scl=Pin(23), sda=Pin(22))
display = HT16K33Segment14(i2c, 0x70)
display.set_brightness(5)
display.clear()

display_2 = HT16K33Segment14(i2c, 0x71)
display_2.set_brightness(5)
display_2.clear()

display_3 = HT16K33Segment14(i2c, 0x72)
display_3.set_brightness(5)
display_3.clear()

while True:
    a = 65
    b = 69
    c = 73
    while (a < 80):
        display.clear()
        display_2.clear()
        display_3.clear()
        display.set_character(chr(a), 0)
        display.set_character(chr(a + 1), 1)
        display.set_character(chr(a + 2), 2)
        display.set_character(chr(a + 3), 3)
        display_2.set_character(chr(b), 0)
        display_2.set_character(chr(b + 1), 1)
        display_2.set_character(chr(b + 2), 2)
        display_2.set_character(chr(b + 3), 3)
        display_3.set_character(chr(b), 0)
        display_3.set_character(chr(c + 1), 1)
        display_3.set_character(chr(c + 2), 2)
        display_3.set_character(chr(c + 3), 3)        
        display.draw()
        display_2.draw()
        display_3.draw()
        a += 1
        b += 1
        c += 1
        time.sleep(0.5)
    time.sleep(5)