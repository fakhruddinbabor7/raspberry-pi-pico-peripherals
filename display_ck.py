from machine import Pin, SoftI2C
from time import sleep_ms

bus = SoftI2C(scl=Pin(6), sda=Pin(7), freq=100_000)
sleep_ms(200)

addresses = bus.scan()
print("OLED scan:", [hex(addr) for addr in addresses])