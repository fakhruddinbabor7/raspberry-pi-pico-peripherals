from machine import UART, Pin

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), timeout=200)

# Clear any byte picked up while the pins switched to UART mode.
uart.read()

message = b"Hello"
uart.write(message)
received = uart.read(len(message))

print("Sent:    ", message)
print("Received:", received)
print("PASS" if received == message else "FAIL")