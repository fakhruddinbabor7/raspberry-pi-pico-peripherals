from machine import ADC, Pin
from time import sleep

vsys = ADC(Pin(29))

for second in range(1, 6):
    volts = vsys.read_u16() * 3.3 * 3 / 65535
    print("Reading {}: {:.2f} V".format(second, volts))
    sleep(1)