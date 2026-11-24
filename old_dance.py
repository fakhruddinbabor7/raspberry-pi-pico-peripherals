from machine import Pin, SoftI2C
from time import sleep_ms
from ssd1306 import SSD1306_I2C

bus = SoftI2C(scl=Pin(6), sda=Pin(7), freq=100_000)
sleep_ms(200)

# Your OLED sometimes answers the scan but misses a setup command.
oled = None
for attempt in range(1, 6):
    try:
        if 0x3C in bus.scan():
            oled = SSD1306_I2C(128, 64, bus, addr=0x3C)
            break
    except OSError as error:
        print("OLED setup attempt", attempt, error)
    sleep_ms(300)

if oled is None:
    raise SystemExit("OLED did not initialize. Press F5 to try again.")

# Each pose sets the body position, hand heights, and foot positions.
poses = [
    # body x, left hand y, right hand y, left foot x, right foot x
    (56, 18, 37, 40, 62),
    (64, 22, 22, 56, 72),
    (72, 37, 18, 66, 88),
    (64, 35, 35, 54, 74),
]

for frame in range(40):
    x, left_hand, right_hand, left_foot, right_foot = poses[frame % 4]

    oled.fill(0)
    oled.text("Hello from Pico", 4, 0)

    oled.rect(x - 4, 14, 9, 9, 1)          # Head
    oled.line(x, 23, x, 40, 1)             # Body
    oled.line(x, 27, x - 14, left_hand, 1)
    oled.line(x, 27, x + 14, right_hand, 1)
    oled.line(x, 40, left_foot, 54, 1)
    oled.line(x, 40, right_foot, 54, 1)
    oled.hline(24, 56, 80, 1)              # Dance floor

    try:
        oled.show()
    except OSError as error:
        print("Display connection lost on frame", frame, error)
        break

    sleep_ms(150)