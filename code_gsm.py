import machine
import time
from machine import UART


uart = UART(1, baudrate=9600, tx=17, rx=16)


def send_command(command, timeout=1000):
    uart.write(command + b'\r\n')
    time.sleep_ms(timeout)
    return uart.read()


send_command(b'AT')
print(send_command(b'AT'))  


send_command(b'AT+CMGF=1')


recipient_number = b'+21654595910'


sms_message = b'Fire is detected now inside the room.'
print('begin')


send_command(b'AT+CMGS="' + recipient_number + b'"', timeout=2000)
send_command(sms_message + bytearray([26]))  

print('SMS sent successfully.')

