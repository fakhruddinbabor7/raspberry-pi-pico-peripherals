from machine import Pin, SoftI2C
from time import sleep_ms
from ssd1306 import SSD1306_I2C

bus = SoftI2C(scl=Pin(6), sda=Pin(7), freq=100_000)
sleep_ms(200)

for attempt in range(1, 6):
    stage = "scan"
    try:
        addresses = bus.scan()
        print("Attempt", attempt, "found:", [hex(a) for a in addresses])

        if 0x3C in addresses:
            stage = "OLED setup"
            oled = SSD1306_I2C(128, 64, bus, addr=0x3C)

            stage = "text update"
            oled.fill(0)
            oled.text("Hello from Pico", 0, 0)
            oled.show()
            print("Text sent")
            break

    except OSError as error:
        print(stage, "failed:", error)

    sleep_ms(500)