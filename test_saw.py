import numpy as np
import time
from pymodbus.client import ModbusSerialClient
"""
import RPi.GPIO as gpio
import time
import board
import busio
import adafruit_mcp4725
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(6, gpio.OUT)
gpio.setup(5, gpio.OUT)
#gpio.setup(#, gpio.OUT)         #GPIO para encender puerto #1
#pio.setup(#, gpio.OUT)         #GPIO para encender puerto #2
gpio.output(6, gpio.LOW)
gpio.output(5, gpio.LOW)
"""

alto_Mod_0_10 = 3750
bajo_Mod_0_10 = 700
alto_Mod_2_10 = 3750
bajo_Mod_2_10 = 0
alto_Mod_0_20 = 3750
bajo_Mod_0_20 = 0
alto_Mod_4_20 = 3750
bajo_Mod_4_20 = 0

i = 0
porcent_step = 1
widthTimePulse_show = 1
wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
wtp_show = widthTimePulse_show
array_1 = np.arange(0,101,porcent_step)
array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
final_array = np.concatenate((array_1, array_2))


# i2c_read_a = busio.I2C(board.SCL, board.SDA)
# adc_read_a = ADS.ADS1115(i2c_read_a)
# modulation_read_a = AnalogIn(adc_read_a, ADS.P1)
#medio salida analoga 2
# i2c_write_a = busio.I2C(board.SCL, board.SDA)
# modulation_write_a = adafruit_mcp4725.MCP4725(i2c_write_a, address=97)


client = ModbusSerialClient(
method = 'rtu'
,port='COM9'
,baudrate=19200
,parity = 'N'
,timeout=1 
)
client.connect()




"""while True:
    #while pausa_hilo == True:
    #    time.sleep(0.1)
    item = final_array[i]
    #fpos = map(item,0,100,bajo_Mod_0_10,3400)
    valor = max(0, min(item, 100))
    fpos = (valor - 0) * (3400 - bajo_Mod_0_10) / (100 - 0) + bajo_Mod_0_10
    setPoint_modulation_a = int(item)
    #modulation_write_a.raw_value = int(fpos)
    print(fpos)
    i = i + 1
    if i == len(final_array):
        i = 0
    time.sleep(0.1)"""

while True:
    item = final_array[i]
    fpos = int(item)
    setPoint_modulation_a = int(item)
    print(fpos, item)
    client.write_register(2, fpos, 1)
    i = i + 1
    if i == len(final_array):
        i = 0
    time.sleep(0.3)