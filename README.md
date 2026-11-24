
# Raspberry Pi Pico Peripheral Tests

I use these MicroPython scripts to bring up peripherals on a Raspberry Pi Pico (RP2040) and check each connection independently. The UART test sends a known byte sequence through a physical loopback. The I²C tests progress from discovering a device address to reading a sensor register or updating an OLED. Two ADC examples measure the chip temperature and estimate the board's supply voltage.

## Hardware and setup

Use a Pico running MicroPython, a USB data cable, and Thonny. The UART test needs one jumper. The display examples use a 128 × 64 SSD1306 I²C OLED at address `0x3C`. The sensor probe expects a device with a chip-ID register at `0xD0` and an address of `0x76` or `0x77`.

1. Choose one test from the table below. Disconnect USB power while changing jumper connections.
2. Connect the Pico by USB, open Thonny, and select the MicroPython (Raspberry Pi Pico) interpreter and the board's port.
3. For the two OLED drawing examples, copy a compatible MicroPython `ssd1306.py` driver onto the Pico. The address scan runs without that driver.
4. Open the chosen script in Thonny, press **F5**, and read the output in the Shell. Each script runs independently.

Pin names below are **GPIO labels** printed as GP numbers. The OLED and sensor scripts assign opposite roles to GP6 and GP7. Wire each experiment according to its own row.

| Test | Script | Connections |
|---|---|---|
| UART0 loopback | [uart_loop_bk.py](uart_loop_bk.py) | Jumper GP0 (TX) to GP1 (RX) |
| OLED address scan | [display_address_ck.py](display_address_ck.py) | GP6 → SCL, GP7 → SDA |
| OLED text | [hello_from_pico.py](hello_from_pico.py) | Same OLED wiring |
| OLED animation | [old_dance.py](old_dance.py) | Same OLED wiring |
| I²C chip-ID read | [address_sensor.py](address_sensor.py) | GP6 → SDA, GP7 → SCL |
| Chip temperature | [temp_ck.py](temp_ck.py) | Internal ADC channel 4 |
| Supply voltage | [voltage_receive_mesurement.py](voltage_receive_mesurement.py) | Onboard VSYS sensing path via GP29 on the original Pico |

For the I²C experiments, connect the module ground to Pico GND and use a module compatible with 3.3 V power and logic. SDA and SCL need pull-ups to 3.3 V. Check whether your breakout already provides them. The file `display_ck.py` contains the same scanner as `display_address_ck.py`.

## 1. UART protocol testing with a physical loopback

UART sends bytes asynchronously. On this board, UART0 transmits on GP0 and receives on GP1. Connecting the pins returns transmitted bits to the receiver. The USB connection separately carries the Thonny console output.

Run `uart_loop_bk.py`. The script configures UART0 at **115200 baud**, clears pending input, writes the five bytes in `b"Hello"`, and requests five bytes back with a 200 ms timeout. It compares the received bytes with the original payload.

**Expected output with the jumper installed**

```text
Sent:     b'Hello'
Received: b'Hello'
PASS
```

For a negative test, disconnect the loopback jumper and rerun. The expected verdict is `FAIL`. A timeout can appear as `None`. Together, the two runs check that successful reception depends on the physical return path. Communication with a second device would require a separate test.

## 2. I²C protocol testing with an OLED

I²C uses a clock line (SCL) and a bidirectional data line (SDA). The Pico acts as the controller. These examples use MicroPython's software I²C implementation, `SoftI2C`, at **100 kHz**.

1. **Discover the address.** Run `display_address_ck.py`. The scan prints the 7-bit addresses that acknowledge the Pico. In my hardware session, the display responded with `OLED scan: ['0x3c']`.
2. **Test initialization and data transfer.** Run `hello_from_pico.py`. It scans for the display, initializes the SSD1306, draws **Hello from Pico** in a framebuffer, and calls `oled.show()` to transfer the pixels. A successful run prints `Text sent` and shows the message on the screen.
3. **Exercise repeated writes.** Run `old_dance.py`. It cycles through four stick-figure poses across 40 frames, pausing 150 ms after each update. Watch for the moving figure and check the Shell for a frame-specific transfer error.


