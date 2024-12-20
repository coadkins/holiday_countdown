# IMPORTS
import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import board
import busio
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
from ht16k33 import HT16K33Segment14

# Christmas Date and Time
EVENT_YEAR = 2024
EVENT_MONTH = 12
EVENT_DAY = 25
EVENT_HOUR = 0
EVENT_MINUTE = 0
EVENT_NAME = "Christmas"
EVENT_MSG = "Merry Christmas * "

try:
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
# any errors, reset MCU
except Exception as e:  # pylint: disable=broad-except
    reset_on_error(10, e)

aio_username = os.getenv("ADAFRUIT_AIO_USERNAME")
aio_key = os.getenv("ADAFRUIT_AIO_KEY")
location = os.getenv("ADAFRUIT_AIO_TIMEZONE")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
# Initialize an Adafruit IO HTTP API object
try:
    io = IO_HTTP(aio_username, aio_key, requests)
except Exception as e:  # pylint: disable=broad-except
    reset_on_error(10, e)
print("Connected to Adafruit IO")

clock = time.monotonic()

event_time = time.struct_time(
    (EVENT_YEAR, EVENT_MONTH, EVENT_DAY, EVENT_HOUR, EVENT_MINUTE, 0, -1, -1, False)
)

# Configured for the Adafruit Feather ESP32v2
i2c = board.STEMMA_I2C()

while not i2c.try_lock():
    pass

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

scroll_time = 0

while True:
    if (clock + scroll_time) < time.monotonic():
            now = io.receive_time()
            # print(now)
            # print(event_time)
            remaining = time.mktime(event_time) - time.mktime(now)
            # calculate the seconds remaining
            secs_remaining = remaining % 60
            remaining //= 60
            # calculate the minutes remaining
            mins_remaining = remaining % 60
            remaining //= 60
            # calculate the hours remaining
            hours_remaining = remaining % 24
            remaining //= 24
            # calculate the days remaining
            days_remaining = remaining
            # pack the calculated times into a string to scroll
            countdown_string = (
                "* %d Days %d Hours %d Minutes %s Seconds until %s *"
                % (
                    days_remaining,
                    hours_remaining,
                    mins_remaining,
                    secs_remaining,
                    EVENT_NAME,
                )
            )
            message = countdown_string
            scroll_length = range(0, len(message) - 12 + 1)
            # if it's the day of the event...
            if remaining < 0:
                message = EVENT_MESSAGE
                scroll_length = range(0, len(message) - 12 + 1)
            print(message)
    for i in scroll_length:
        for display_indx, display in enumerate(DISPLAYS):
            display.clear()
            for c in range(0,4):
                display.set_character(message[i+c +(4*display_indx)], c)
                display.draw()
        time.sleep(.2)
