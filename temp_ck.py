from machine import ADC
from time import sleep

sensor = ADC(4)  # Channel 4 reads the RP2040's internal temperature sensor

for sample in range(5):
    raw = sensor.read_u16()
    voltage = raw * 3.3 / 65535
    temperature_c = 27 - (voltage - 0.706) / 0.001721

    print("Reading", sample + 1, ":", round(temperature_c, 1), "°C")
    sleep(1)