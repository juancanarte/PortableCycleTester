from pymodbus.client import ModbusSerialClient
import threading
import time
import random


"""import RPi.GPIO as gpio
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
gpio.output(6, gpio.LOW)
gpio.output(5, gpio.LOW)
"""

#modo global
modoG = 0
modoG_1 = 0
modoG_2 = 0

#--------------------------------------------CAFE ALONE--------------------------------------------#
#parametros modulation ALONE
modulation_write_a = None
modulation_read_a = None
inputType_modulation_a = 0
setPoint_modulation_a = 0
#parametros modbus ALONE
client = None
nodo = 1
flag_a = threading.Event()
thread_modbus_a = None
#----------------------------------------------CAFE 1----------------------------------------------#
#parametros modulation 1
modulation_write_1 = None
modulation_read_1 = None
inputType_modulation_1 = 0
setPoint_modulation_1 = 0
#parametros modbus 1
client_1 = None
nodo_1 = 1
flag_1 = threading.Event()
thread_modbus_1 = None
#----------------------------------------------CAFE 2----------------------------------------------#
#parametros modulation 2
modulation_write_2 = None
modulation_read_2 = None
inputType_modulation_2 = 0
setPoint_modulation_2 = 0
#parametros modbus 2
client_2 = None
nodo_2 = 1
flag_2 = threading.Event()
thread_modbus_2 = None

def cycle_test_params(params, modo):
    global client,modoG,nodo,client_1,modoG_1,nodo_1,client_2,modoG_2,nodo_2,modulation_read_a,modulation_write_a,inputType_modulation_a,\
    modulation_read_1,modulation_write_1,inputType_modulation_1,modulation_read_2,modulation_write_2,inputType_modulation_2

    parametros = params.split(',')
    print(parametros)
    modo_dut_1 = parametros[14].split('|')[0].upper()
    modo_dut_2 = parametros[21].split('|')[0].upper()
    modo_dut_a = parametros[4].split('|')[0].upper()
    cant_duts = 0
    #parametros DUT ALONE
    puerto_dut_alone = 0
    dut_alone = ''
    modo_dut_alone = ''
    #parametros DUT 1
    mode_dut_1 = ''
    name_dut_1 = ''
    #parametros DUT 1
    mode_dut_2 = ''
    name_dut_2 = ''
    #Cuantos DUT hay
    if parametros[0] != '0' and  parametros[1] != '0':  #Si hay 1 DUT
        cant_duts = 1
        #Consultar en que puerto esta el DUT
        if parametros[0][-1] == '1':
            puerto_dut_alone = 1
        elif parametros[0][-1] == '2':
            puerto_dut_alone = 2
        #Que DUT esta conectado CAFE or COIL or LIMIT SWITCH
        dut_alone = parametros[1]
        #Si es CAFE
        if dut_alone == 'CAFE':                
            modo_dut_alone = modo_dut_a
            #Si es CAFE DIGITAL
            if modo_dut_alone == 'DIGITAL':
                modoG = 1
                print("CAFE digital")
            #Si es CAFE MODULATION
            if modo_dut_alone == 'MODULATION':
                modoG = 2
                input_type = parametros[6].split('|')[0]
                if puerto_dut_alone == 1:
                    print("primera opcion modulacion")
                    """
                    i2c_read_a = busio.I2C(board.SCL, board.SDA)
                    adc_read_a = ADS.ADS1115(i2c_read_a)
                    modulation_read_a = AnalogIn(adc_read_a, ADS.P0)
                    #medio salida analoga 1
                    i2c_write_a = busio.I2C(board.SCL, board.SDA)
                    modulation_write_a = adafruit_mcp4725.MCP4725(i2c_write_a, address=96)
                    """
                elif puerto_dut_alone == 2:
                    print("segunda opcion modulacion")
                    """
                    i2c_read_a = busio.I2C(board.SCL, board.SDA)
                    adc_read_a = ADS.ADS1115(i2c_read_a)
                    modulation_read_a = AnalogIn(adc_read_a, ADS.P1)
                    #medio salida analoga 2
                    i2c_write_a = busio.I2C(board.SCL, board.SDA)
                    modulation_write_a = adafruit_mcp4725.MCP4725(i2c_write_a, address=97)
                    """
                if input_type == '0v-10v':              #si es 0V - 10V
                    inputType_modulation_a = '0-10v'
                    print("MODULATION 0V - 10V")
                elif input_type == '2v-10v':              #si es 2V - 10V
                    inputType_modulation_a = '2-10v'
                    print("MODULATION 2V - 10V")
                elif input_type == '0mA-20mA':              #si es 0mA-20mA
                    inputType_modulation_a = '0-20mA'
                    print("MODULATION 0mA-20mA")
                elif input_type == '4mA-20mA':              #si es 4mA-20mA
                    inputType_modulation_a = '4-20mA'
                    print("MODULATION 4mA-20mA")
            #Si es CAFE MODBUS
            if modo_dut_alone == 'MODBUS':
                puerto = 'COM6' if puerto_dut_alone == 1 else 'COM7'
                nodo = int(parametros[10])
                baud = int(parametros[7].split('|')[0])
                modoG = 3
                client = ModbusSerialClient(
                method = 'rtu'
                ,port=puerto
                ,baudrate=baud
                ,parity = 'N'
                ,timeout=1 
                )
                client.connect()
                print("CAFE MODBUS", puerto, nodo, baud)
        elif dut_alone == 'COIL':     
            print("es COIL")
        elif dut_alone == 'LIMIT SWITCH':     
            print("es LIMIT SWITCH")

    else:                                               #Si hay 2 DUT
        cant_duts = 2
        name_dut_1 = parametros[2]
        name_dut_2 = parametros[3]
        #Que es el DUT 1
        if name_dut_1 == 'CAFE':                        #Si es CAFE
            if modo_dut_1 == 'DIGITAL':                 #Si CAFE 1 es DIGITAL
                modoG_1 = 1
                print("es cafe digital")
            elif modo_dut_1 == 'MODULATION':            #Si CAFE 1 es MODULATION
                modoG_1 = 2
                input_type_1 = parametros[16].split('|')[0]

                """
                i2c_read_1 = busio.I2C(board.SCL, board.SDA)
                adc_read_1 = ADS.ADS1115(i2c_read_1)
                modulation_read_1 = AnalogIn(adc_read_1, ADS.P0)
                #medio salida analoga 1
                i2c_write_1 = busio.I2C(board.SCL, board.SDA)
                modulation_write_1 = adafruit_mcp4725.MCP4725(i2c_write_1, address=96)
                """

                if input_type_1 == '0v-10v':              #si es 0V - 10V
                    inputType_modulation_1 = '0-10v'
                    print("MODULATION 0V - 10V")
                elif input_type_1 == '2v-10v':              #si es 2V - 10V
                    inputType_modulation_1 = '2-10v'
                    print("MODULATION 2V - 10V")
                elif input_type_1 == '0mA-20mA':              #si es 0mA-20mA
                    inputType_modulation_1 = '0-20mA'
                    print("MODULATION 0mA-20mA")
                elif input_type_1 == '4mA-20mA':              #si es 4mA-20mA
                    inputType_modulation_1 = '4-20mA'
                    print("MODULATION 4mA-20mA")

                print("es cafe modulation")
            elif modo_dut_1 == 'MODBUS':                #Si CAFE 1 es MODBUS
                modoG_1 = 3
                nodo_1 = int(parametros[20])
                baud = int(parametros[17].split('|')[0])
                client_1 = ModbusSerialClient(
                method = 'rtu'
                ,port='COM6'
                ,baudrate=baud
                ,parity = 'N'
                ,timeout=1 
                )
                client_1.connect()
                print("es cafe modbus",client_1)
        elif name_dut_1 == 'COIL':                      #Si es COIL
            print("el dut1 es coil")
        elif name_dut_1 == 'LIMIT SWITCH':              #Si es LIMIT SWITCH
            print("el dut1 es limit switch")
        #Que es el DUT 2
        if name_dut_2 == 'CAFE':                        #Si es CAFE
            if modo_dut_2 == 'DIGITAL':                 #Si CAFE 2 es DIGITAL
                modoG_2 = 1
                print("es cafe digital")
            elif modo_dut_2 == 'MODULATION':            #Si CAFE 2 es MODULATION
                modoG_2 = 2
                input_type_2 = parametros[23].split('|')[0]

                """
                i2c_read_2 = busio.I2C(board.SCL, board.SDA)
                adc_read_2 = ADS.ADS1115(i2c_read_2)
                modulation_read_2 = AnalogIn(adc_read_2, ADS.P1)
                #medio salida analoga 1
                i2c_write_2 = busio.I2C(board.SCL, board.SDA)
                modulation_write_2 = adafruit_mcp4725.MCP4725(i2c_write_2, address=97)
                """

                if input_type_2 == '0v-10v':              #si es 0V - 10V
                    inputType_modulation_2 = '0-10v'
                    print("MODULATION 0V - 10V")
                elif input_type_2 == '2v-10v':              #si es 2V - 10V
                    inputType_modulation_2 = '2-10v'
                    print("MODULATION 2V - 10V")
                elif input_type_2 == '0mA-20mA':              #si es 0mA-20mA
                    inputType_modulation_2 = '0-20mA'
                    print("MODULATION 0mA-20mA")
                elif input_type_2 == '4mA-20mA':              #si es 4mA-20mA
                    inputType_modulation_2 = '4-20mA'
                    print("MODULATION 4mA-20mA")

                print("es cafe modulation")
            elif modo_dut_2 == 'MODBUS':                #Si CAFE 2 es MODBUS
                modoG_2 = 3
                nodo_2 = int(parametros[27])
                baud = int(parametros[24].split('|')[0])
                client_2 = ModbusSerialClient(
                method = 'rtu'
                ,port='COM7'
                ,baudrate=baud
                ,parity = 'N'
                ,timeout=1 
                )
                client_2.connect()
                print("es cafe modbus",client_2)
        elif name_dut_2 == 'COIL':                      #Si es COIL
            print("el dut2 es coil")
        elif name_dut_2 == 'LIMIT SWITCH':              #Si es LIMIT SWITCH
            print("el dut2 es limit switch")

    #print(cant_duts, puerto_dut_alone, dut_alone)
    #print("modo 1 = " + modo_dut_1, "modo 2 = "+modo_dut_2)