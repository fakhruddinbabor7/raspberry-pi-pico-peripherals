from machine import Pin, SoftI2C
from time import sleep_ms

bus = SoftI2C(sda=Pin(6), scl=Pin(7), freq=10_000)
sleep_ms(100)

for address in (0x76, 0x77):
    try:
        chip_id = bus.readfrom_mem(address, 0xD0, 1)[0]
        print(hex(address), "answered. Chip ID:", hex(chip_id))
    except OSError as error:
        print(hex(address), "read failed:", error)