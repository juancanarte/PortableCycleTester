from pymodbus.client import ModbusSerialClient
import threading
import time
import random
import json
import numpy as np
from cycle_test.models import defSettings as defSet

""""""
try:
    import RPi.GPIO as gpio
    import pcf8574_io
    import time
    import smbus
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
    
    gpio.setup(12, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    gpio.setup(20, gpio.OUT)
    gpio.setup(21, gpio.OUT)
    
    gpio.setup(18, gpio.IN)
    gpio.setup(23, gpio.IN)
    gpio.setup(24, gpio.IN)
    gpio.setup(25, gpio.IN)
    
    #Set salidas analogas
    gpio.output(6, gpio.LOW)
    gpio.output(5, gpio.LOW)

    #Set AC/DC
    gpio.output(12, gpio.LOW)
    gpio.output(16, gpio.LOW)
    
    #Set Control digital
    gpio.output(20, gpio.LOW)
    gpio.output(21, gpio.LOW)
    
    
except:
    print("windows")
""""""

#-----------PCF8574-------#

# Inicializa el bus I2C
try:
    bus = smbus.SMBus(1)
    pcf8574_address = 0x20  # La dirección del PCF8574 (cámbiala si es diferente)
except:
    print("Es windows")

def write_pcf8574(data):
    bus.write_byte(pcf8574_address, data)

def read_pcf8574():
    return bus.read_byte(pcf8574_address)


try:
    #---------pcb digital output / Analog Input i2c---------·#
    pcfRPI = pcf8574_io.PCF(0x27)
    pcfRPI.pin_mode("p0", "INPUT")
    pcfRPI.pin_mode("p1", "INPUT")
    pcfRPI.pin_mode("p2", "INPUT")
    pcfRPI.pin_mode("p3", "INPUT")
    pcfRPI.pin_mode("p4", "OUTPUT")
    pcfRPI.pin_mode("p5", "OUTPUT")
    pcfRPI.pin_mode("p6", "OUTPUT")
    pcfRPI.pin_mode("p7", "OUTPUT")

    pcfRPI.write("p4", "LOW")
    pcfRPI.write("p5", "LOW")
    pcfRPI.write("p6", "LOW")
    pcfRPI.write("p7", "LOW")

    #---------pcb digital output / Digital input i2c---------·#
    pcfRPI_on_off = pcf8574_io.PCF(0x26)
    pcfRPI_on_off.pin_mode("p0", "INPUT")
    pcfRPI_on_off.pin_mode("p1", "INPUT")
    pcfRPI_on_off.pin_mode("p2", "INPUT")
    pcfRPI_on_off.pin_mode("p3", "INPUT")
    pcfRPI_on_off.pin_mode("p4", "OUTPUT")
    pcfRPI_on_off.pin_mode("p5", "OUTPUT")
    pcfRPI_on_off.pin_mode("p6", "OUTPUT")
    pcfRPI_on_off.pin_mode("p7", "OUTPUT")

    pcfRPI_on_off.write("p4", "LOW")
    pcfRPI_on_off.write("p5", "LOW")
    pcfRPI_on_off.write("p6", "LOW")
    pcfRPI_on_off.write("p7", "LOW")
except:
    print("Es windows")

widthTimePulse_show = 6

#modo global
modoG = 0
modoG_1 = 0
modoG_2 = 0

cant_duts = 0

alto_Mod_0_10 = 3460
bajo_Mod_0_10 = 0
alto_Mod_2_10 = 3495
bajo_Mod_2_10 = 720
alto_Mod_0_20 = 3750
bajo_Mod_0_20 = 0
alto_Mod_4_20 = 3750
bajo_Mod_4_20 = 720

scale_porcent = 10
width_time_saw = 0.3
tOutModbus = 0.5

#-------------LEDS----------#
flag_led = threading.Event()
thread_leds = None
#--------------------------------------------CAFE ALONE--------------------------------------------#
modo_dut_alone = ''
dut_alone = ''
tiempoApagadoCafe_a = 6
tiempoEncendidoCafe_a = 6
op_voltage_a = None
#Encender puerto alone
port_gpio_alone = None
#parametros modulation ALONE
modulation_write_a = None
modulation_read_a = None
inputType_modulation_a = 0
setPoint_modulation_a = 0
position_a = 0
#parametros modbus ALONE
client = None
nodo = 1
flag_a = threading.Event()
thread_modbus_a = None
#----------------------------------------------CAFE 1----------------------------------------------#
modo_dut_1 = ''
name_dut_1 = ''
tiempoApagadoCafe_1 = 6
op_voltage_1 = None
#parametros modulation 1
modulation_write_1 = None
modulation_read_1 = None
inputType_modulation_1 = 0
setPoint_modulation_1 = 0
position_1 = 0
#parametros modbus 1
client_1 = None
nodo_1 = 1
flag_1 = threading.Event()
thread_modbus_1 = None
#----------------------------------------------CAFE 2----------------------------------------------#
modo_dut_2 = ''
name_dut_2 = ''
tiempoApagadoCafe_2 = 6
op_voltage_2 = None
#parametros modulation 2
modulation_write_2 = None
modulation_read_2 = None
inputType_modulation_2 = 0
setPoint_modulation_2 = 0
position_2 = 0
#parametros modbus 2
client_2 = None
nodo_2 = 1
flag_2 = threading.Event()
thread_modbus_2 = None
#----------------------------------------------COIL ALONE----------------------------------------------#
posCoil_a = None
#----------------------------------------------COIL 1----------------------------------------------#
posCoil_1 = None
#----------------------------------------------COIL 2----------------------------------------------#
posCoil_2 = None
#----------------------------------------------LS ALONE----------------------------------------------#

stop_condition = threading.Condition()
running_threads = []

#--------------LEDs status------------#
def start_blink_led_wifi():
    global thread_leds

    if thread_leds is None or not thread_leds.is_alive():
        thread_leds = threading.Thread(target=blink_led_wifi)
        thread_leds.start()
        #running_threads.append(thread_leds) 

def stop_blink_led_wifi():
    if thread_leds is not None and thread_leds.is_alive():
        flag_led.set()
        thread_leds.join()
        flag_led.clear()
            # print("open_modb

def blink_led_wifi():
    global flag_led

    while not flag_led.is_set():
        pcfRPI.write("p6", "HIGH")
        time.sleep(1)

        pcfRPI.write("p6", "LOW")
        time.sleep(1)

start_blink_led_wifi()

#--------------LEDs status------------#

def extraer_parametros(parametrosR, modo):
    parametros = parametrosR.split(',')
    listaP = []

    print(parametros[35], parametros[36], parametros[37], parametros[38])

    for i in range(4,34):
        listaP.append(parametros[i].split('|')[0])

    opVoltage_coil_a = parametros[11].split('|')[0].upper()
    opVoltage_coil_1 = parametros[28].split('|')[0].upper()
    opVoltage_coil_2 = parametros[30].split('|')[0].upper()

    modo_dut_1 = parametros[14].split('|')[0].upper()
    modo_dut_2 = parametros[21].split('|')[0].upper()
    modo_dut_a = parametros[4].split('|')[0].upper()
    #print("modo 1 = "+modo_dut_1+" modo 2 = "+modo_dut_2+" total = "+parametrosR)
    #print(modo_dut_1==0)
    id_dut = 0
    label_dut = 0
    label_dut_1 = 0
    label_dut_2 = 0
    temp_dut_alone = None
    temp_dut_1 = None
    temp_dut_2 = None
    if parametros[0] != 0 and parametros[1] != 0:
        id_dut = parametros[0][-1]
        label_dut = parametros[1]
        #Vista SHOW para un solo DUT
        if label_dut == 'CAFE' and modo == 'Show':
            temp_dut_alone = "Proyecto_PCT/templates/show/show_box/show_cafe/show_cafe_alone.html"
        elif label_dut == 'COIL' and modo == 'Show':
            temp_dut_alone = "Proyecto_PCT/templates/show/show_box/show_coil/show_coil_alone.html"
        elif label_dut == 'LIMIT SWITCH' and modo == 'Show':
            temp_dut_alone = "Proyecto_PCT/templates/show/show_box/show_ls/show_ls_alone.html"
        #Vista CYCLE TEST para un solo DUT
        elif label_dut == 'CAFE' and modo == 'Cycle test':
            temp_dut_alone = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_cafe/cycle_test_cafe_alone.html"
        elif label_dut == 'COIL' and modo == 'Cycle test':
            temp_dut_alone = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_coil/cycle_test_coil_alone.html"
        elif label_dut == 'LIMIT SWITCH' and modo == 'Cycle test':
            temp_dut_alone = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_ls/cycle_test_ls_alone.html"

    if parametros[2] != 0 and parametros[3] != 0:
        label_dut_1 = parametros[2]
        label_dut_2 = parametros[3]
        #Vista SHOW para el DUT #1
        if label_dut_1 == 'CAFE' and modo == 'Show':
            temp_dut_1 = "Proyecto_PCT/templates/show/show_box/show_cafe/show_cafe_1.html"
        elif label_dut_1 == 'COIL' and modo == 'Show':
            temp_dut_1 = "Proyecto_PCT/templates/show/show_box/show_coil/show_coil_1.html"
        elif label_dut_1 == 'LIMIT SWITCH' and modo == 'Show':
            temp_dut_1 = "Proyecto_PCT/templates/show/show_box/show_ls/show_ls_1.html"
        #Vista SHOW para el DUT #2
        if label_dut_2 == 'CAFE' and modo == 'Show':
            temp_dut_2 = "Proyecto_PCT/templates/show/show_box/show_cafe/show_cafe_2.html"
        elif label_dut_2 == 'COIL' and modo == 'Show':
            temp_dut_2 = "Proyecto_PCT/templates/show/show_box/show_coil/show_coil_2.html"
        elif label_dut_2 == 'LIMIT SWITCH' and modo == 'Show':
            temp_dut_2 = "Proyecto_PCT/templates/show/show_box/show_ls/show_ls_2.html"
        #Vista CYCLE TEST para el DUT #1
        if label_dut_1 == 'CAFE' and modo == 'Cycle test':
            temp_dut_1 = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_cafe/cycle_test_cafe_1.html"
        elif label_dut_1 == 'COIL' and modo == 'Cycle test':
            temp_dut_1 = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_coil/cycle_test_coil_1.html"
        elif label_dut_1 == 'LIMIT SWITCH' and modo == 'Cycle test':
            temp_dut_1 = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_ls/cycle_test_ls_1.html"
        #Vista CYCLE TEST para el DUT #2
        if label_dut_2 == 'CAFE' and modo == 'Cycle test':
            temp_dut_2 = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_cafe/cycle_test_cafe_2.html"
        elif label_dut_2 == 'COIL' and modo == 'Cycle test':
            temp_dut_2 = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_coil/cycle_test_coil_2.html"
        elif label_dut_2 == 'LIMIT SWITCH' and modo == 'Cycle test':
            temp_dut_2 = "Proyecto_PCT/templates/cycle_test/cycle_test_box/cycle_test_ls/cycle_test_ls_2.html"

    respuesta_2 = [id_dut, label_dut, temp_dut_alone, label_dut_1, label_dut_2, temp_dut_1, temp_dut_2] + listaP

    return respuesta_2

def show_params(params, modo):
    global client,modoG,nodo,client_1,modoG_1,nodo_1,client_2,modoG_2,nodo_2,modulation_read_a,modulation_write_a,inputType_modulation_a,\
    modulation_read_1,modulation_write_1,inputType_modulation_1,modulation_read_2,modulation_write_2,inputType_modulation_2,port_gpio_alone,\
    op_voltage_a,op_voltage_1,op_voltage_2, cant_duts, name_dut_1, name_dut_2, dut_alone, modo_dut_1, modo_dut_2, modo_dut_alone

    parametros = params.split(',')
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
            port_gpio_alone = 1
        elif parametros[0][-1] == '2':
            puerto_dut_alone = 2
            port_gpio_alone = 2
        #Que DUT esta conectado CAFE or COIL or LIMIT SWITCH
        dut_alone = parametros[1]
        #Si es CAFE
        if dut_alone == 'CAFE':                
            modo_dut_alone = modo_dut_a
            op_voltage_a = parametros[5].split('|')[0]
            
            try:
                #Activar voltaje de operacion en DUT correcto
                if puerto_dut_alone == 1:
                    #Activar voltaje DUT #1
                    if op_voltage_a == '24vdc':
                        gpio.output(16, gpio.LOW)#Swich to DC DUT 1
                    else:
                        gpio.output(16, gpio.HIGH)#Swich to AC DUT 1
                elif puerto_dut_alone == 2:
                    #Activar DUT #2
                    if op_voltage_a == '24vdc':
                        gpio.output(21, gpio.LOW)#Swich to DC DUT 2
                    else:
                        gpio.output(21, gpio.HIGH)#Swich to AC DUT 2
            except:
                pass

            #Si es CAFE DIGITAL
            if modo_dut_alone == 'DIGITAL':
                modoG = 1
                print("CAFE digital")
            #Si es CAFE MODULATION
            if modo_dut_alone == 'MODULATION':
                modoG = 2
                input_type = parametros[6].split('|')[0]
                if puerto_dut_alone == 1:
                    #Switch Relay Modulation/Modbus
                    pcfRPI.write("p4", "HIGH")
                    
                    print("primera opcion modulacion")
                    try:
                        """"""
                        i2c_read_a = busio.I2C(board.SCL, board.SDA)
                        adc_read_a = ADS.ADS1115(i2c_read_a)
                        modulation_read_a = AnalogIn(adc_read_a, ADS.P0)
                        #medio salida analoga 1
                        i2c_write_a = busio.I2C(board.SCL, board.SDA)
                        modulation_write_a = adafruit_mcp4725.MCP4725(i2c_write_a, address=96)
                        """"""
                    except:
                        pass

                elif puerto_dut_alone == 2:
                    #Switch Relay Modulation/Modbus
                    pcfRPI.write("p5", "HIGH")
                    
                    print("segunda opcion modulacion")
                    try:
                        """"""
                        i2c_read_a = busio.I2C(board.SCL, board.SDA)
                        adc_read_a = ADS.ADS1115(i2c_read_a)
                        modulation_read_a = AnalogIn(adc_read_a, ADS.P1)
                        #medio salida analoga 2
                        i2c_write_a = busio.I2C(board.SCL, board.SDA)
                        modulation_write_a = adafruit_mcp4725.MCP4725(i2c_write_a, address=97)
                        """"""
                    except:
                        pass

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
                if puerto_dut_alone == 1:
                    puerto = '/dev/ttyUSB0'
                    #Switch Relay Modulation/Modbus DUT #1
                    pcfRPI.write("p4", "LOW")
                    
                else:
                    puerto = '/dev/ttyUSB1'
                    #Switch Relay Modulation/Modbus DUT #2
                    pcfRPI.write("p5", "LOW")
                
                #puerto = '/dev/ttyUSB1' if puerto_dut_alone == 1 else '/dev/ttyUSB0'
                #puerto = 'COM9' if puerto_dut_alone == 1 else 'COM9'

                nodo = int(parametros[10])
                baud = int(parametros[7].split('|')[0])
                modoG = 3
                client = ModbusSerialClient(
                method = 'rtu'
                ,port=puerto
                ,baudrate=baud
                ,parity = 'N'
                ,timeout = tOutModbus
                )
                client.connect()
                print("CAFE MODBUS", puerto, nodo, baud)
        
        elif dut_alone == 'COIL':     
            op_voltage_a = parametros[11].split('|')[0]
            
            #Activar voltaje de operacion en DUT correcto
            if puerto_dut_alone == 1:
                #Activar voltaje DUT #1
                try:
                    if op_voltage_a == '24vdc':
                        gpio.output(16, gpio.LOW)#Swich to DC DUT 1
                    else:
                        gpio.output(16, gpio.HIGH)#Swich to AC DUT 1
                except:
                    pass
            elif puerto_dut_alone == 2:
                #Activar DUT #2
                if op_voltage_a == '24vdc':
                    gpio.output(21, gpio.LOW)#Swich to DC DUT 2
                else:
                    gpio.output(21, gpio.HIGH)#Swich to AC DUT 2
                    
            #Dejar en bajo los reles de abrir CAFE modo Digital
            try:
                gpio.output(20, gpio.LOW)
                gpio.output(12, gpio.LOW)
            except:
                pass

        elif dut_alone == 'LIMIT SWITCH':     
            op_voltage_a = parametros[13].split('|')[0]

    else:                                               #Si hay 2 DUT
        cant_duts = 2
        name_dut_1 = parametros[2]
        name_dut_2 = parametros[3]
        #Que es el DUT 1
        if name_dut_1 == 'CAFE':                        #Si es CAFE
            op_voltage_1 = parametros[15].split('|')[0]
            if op_voltage_1 == '24vdc':
                gpio.output(16, gpio.LOW)#Swich to DC DUT 1
            else:
                gpio.output(16, gpio.HIGH)#Swich to AC DUT 1
            
            if modo_dut_1 == 'DIGITAL':                 #Si CAFE 1 es DIGITAL
                modoG_1 = 1
                print("es cafe digital")
            elif modo_dut_1 == 'MODULATION':            #Si CAFE 1 es MODULATION
                modoG_1 = 2
                input_type_1 = parametros[16].split('|')[0]

                try:
                    """"""
                    i2c_read_1 = busio.I2C(board.SCL, board.SDA)
                    adc_read_1 = ADS.ADS1115(i2c_read_1)
                    modulation_read_1 = AnalogIn(adc_read_1, ADS.P0)
                    #medio salida analoga 1
                    i2c_write_1 = busio.I2C(board.SCL, board.SDA)
                    modulation_write_1 = adafruit_mcp4725.MCP4725(i2c_write_1, address=96)
                    #Switch Relay Modulation/Modbus
                    pcfRPI.write("p4", "HIGH")
                    """"""
                except:
                    pass

                if input_type_1 == '0v-10v':              #si es 0V - 10V
                    inputType_modulation_1 = '0-10v'
                    #modulation_write_1.raw_value = 0
                    print("MODULATION 0V - 10V")
                elif input_type_1 == '2v-10v':              #si es 2V - 10V
                    #modulation_write_1.raw_value = 720
                    inputType_modulation_1 = '2-10v'
                    print("MODULATION 2V - 10V")
                elif input_type_1 == '0mA-20mA':              #si es 0mA-20mA
                    inputType_modulation_1 = '0-20mA'
                    #modulation_write_1.raw_value = 0
                    print("MODULATION 0mA-20mA")
                elif input_type_1 == '4mA-20mA':              #si es 4mA-20mA
                    inputType_modulation_1 = '4-20mA'
                    #modulation_write_1.raw_value = 720
                    print("MODULATION 4mA-20mA")

                print("es cafe modulation")
            elif modo_dut_1 == 'MODBUS':                #Si CAFE 1 es MODBUS
                #Switch Relay Modulation/Modbus
                pcfRPI.write("p4", "LOW")

                modoG_1 = 3
                nodo_1 = int(parametros[20])
                baud = int(parametros[17].split('|')[0])
                puerto_1 = '/dev/ttyUSB0'

                client_1 = ModbusSerialClient(
                method = 'rtu'
                ,port=puerto_1
                ,baudrate=baud
                ,parity = 'N'
                ,timeout = tOutModbus 
                )
                client_1.connect()
                print("es cafe modbus",client_1)
        elif name_dut_1 == 'COIL':                      #Si es COIL
            op_voltage_1 = parametros[28].split('|')[0]

            #Activar voltaje DUT #1
            if op_voltage_1 == '24vdc':
                gpio.output(16, gpio.LOW)#Swich to DC DUT 1
            else:
                gpio.output(16, gpio.HIGH)#Swich to AC DUT 1
                
        elif name_dut_1 == 'LIMIT SWITCH':              #Si es LIMIT SWITCH
            op_voltage_1 = parametros[32].split('|')[0]
            print("el dut1 es limit switch")

        #Que es el DUT 2
        if name_dut_2 == 'CAFE':                        #Si es CAFE
            op_voltage_2 = parametros[22].split('|')[0]
            
            #Decide power type to DUT 2
            if op_voltage_2 == '24vdc':
                gpio.output(21, gpio.LOW)#Swich to DC DUT 2
            else:
                gpio.output(21, gpio.HIGH)#Swich to AC DUT 2
            
            if modo_dut_2 == 'DIGITAL':                 #Si CAFE 2 es DIGITAL
                modoG_2 = 1
                print("es cafe digital")
            elif modo_dut_2 == 'MODULATION':            #Si CAFE 2 es MODULATION
                modoG_2 = 2
                input_type_2 = parametros[23].split('|')[0]
                
                try:
                    """"""
                    i2c_read_2 = busio.I2C(board.SCL, board.SDA)
                    adc_read_2 = ADS.ADS1115(i2c_read_2)
                    modulation_read_2 = AnalogIn(adc_read_2, ADS.P1)
                    #medio salida analoga 1
                    i2c_write_2 = busio.I2C(board.SCL, board.SDA)
                    modulation_write_2 = adafruit_mcp4725.MCP4725(i2c_write_2, address=97)
                    #Switch Relay Modulation/Modbus
                    pcfRPI.write("p5", "HIGH")
                    """"""
                except:
                    pass

                if input_type_2 == '0v-10v':              #si es 0V - 10V
                    inputType_modulation_2 = '0-10v'
                    #modulation_write_2.raw_value = 0
                    print("MODULATION 0V - 10V")
                elif input_type_2 == '2v-10v':              #si es 2V - 10V
                    inputType_modulation_2 = '2-10v'
                    #modulation_write_2.raw_value = 720
                    print("MODULATION 2V - 10V")
                elif input_type_2 == '0mA-20mA':              #si es 0mA-20mA
                    inputType_modulation_2 = '0-20mA'
                    #modulation_write_2.raw_value = 0
                    print("MODULATION 0mA-20mA")
                elif input_type_2 == '4mA-20mA':              #si es 4mA-20mA
                    inputType_modulation_2 = '4-20mA'
                    #modulation_write_2.raw_value = 720
                    print("MODULATION 4mA-20mA")

                print("es cafe modulation")
            elif modo_dut_2 == 'MODBUS':                #Si CAFE 2 es MODBUS
                #Switch Relay Modulation/Modbus
                pcfRPI.write("p5", "LOW")
                modoG_2 = 3
                nodo_2 = int(parametros[27])
                baud = int(parametros[24].split('|')[0])
                puerto_2 = '/dev/ttyUSB1'
                client_2 = ModbusSerialClient(
                method = 'rtu'
                ,port=puerto_2
                ,baudrate=baud
                ,parity = 'N'
                ,timeout = tOutModbus
                )
                client_2.connect()
                print("es cafe modbus",client_2)
        elif name_dut_2 == 'COIL':                      #Si es COIL
            op_voltage_2 = parametros[30].split('|')[0]

            #Activar DUT #2
            if op_voltage_2 == '24vdc':
                gpio.output(21, gpio.LOW)#Swich to DC DUT 2
            else:
                gpio.output(21, gpio.HIGH)#Swich to AC DUT 2
                
        elif name_dut_2 == 'LIMIT SWITCH':              #Si es LIMIT SWITCH
            op_voltage_2 = parametros[32].split('|')[0]
            print("el dut2 es limit switch")

    #print(cant_duts, puerto_dut_alone, dut_alone)
    #print("modo 1 = " + modo_dut_1, "modo 2 = "+modo_dut_2)

#Funciones SHOW para CAFE alone
def show_start_cafe_alone():
    global thread_modbus_a, client, modoG, nodo, running_threads

    pcfRPI.write("p7", "LOW") #Encender led RUN

    if thread_modbus_a is None or not thread_modbus_a.is_alive():
        thread_modbus_a = threading.Thread(target=show_write_start)
        thread_modbus_a.start()
        running_threads.append(thread_modbus_a) 
    print("STAR_cafe_alone")

def show_stop_cafe_alone():
    global thread_modbus_a, client, modoG, nodo, running_threads,flag_a

    if thread_modbus_a is not None and thread_modbus_a.is_alive():
        flag_a.set()
        thread_modbus_a.join()
        flag_a.clear()
            # print("open_modbus_cafe_alone")
    print("STOP_cafe_alone")

def show_open_cafe_alone(posPorcent):
    global client, modoG, nodo, inputType_modulation_a, modulation_write_a, setPoint_modulation_a
    port = globals()['port_gpio_alone']
    
    if modoG == 1:
        if port == 1:
            gpio.output(20, gpio.HIGH)#DIGITAL OPEN DUT#1
        else:
            gpio.output(12, gpio.HIGH)#DIGITAL OPEN DUT#2
            
        setPoint_modulation_a = 100

    elif modoG == 2:
        if inputType_modulation_a == '0-10v':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_0_10,alto_Mod_0_10))             #Convertir la posicion recibida en datos para el DAC
            modulation_write_a.raw_value = pos
            setPoint_modulation_a = int(posPorcent)
            print("open_0-10v")
        if inputType_modulation_a == '2-10v':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_2_10,alto_Mod_2_10))           #Convertir la posicion recibida en datos para el DAC
            modulation_write_a.raw_value = pos
            setPoint_modulation_a = int(posPorcent)
            print("open_2-10v")
        if inputType_modulation_a == '0-20mA':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_0_20,alto_Mod_0_20))           #Convertir la posicion recibida en datos para el DAC
            modulation_write_a.raw_value = pos
            setPoint_modulation_a = int(posPorcent)
            print("open_0-20mA")
        if inputType_modulation_a == '4-20mA':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_4_20,alto_Mod_4_20))           #Convertir la posicion recibida en datos para el DAC
            modulation_write_a.raw_value = pos
            setPoint_modulation_a = int(posPorcent)
            print("open_4-20mA")
    elif modoG == 3:
        pos = int(map(int(posPorcent),0,100,0,100))           #Convertir la posicion recibida en datos para el DAC
        setPoint_modulation_a = pos
        result2 = client.write_register(2, pos, nodo)
        print("open_modbus_cafe_alone")

def show_close_cafe_alone():
    global client, modoG, nodo, inputType_modulation_a, modulation_write_a,setPoint_modulation_a
    
    port = globals()['port_gpio_alone']
    
    if modoG == 1:
        if port == 1:
            gpio.output(20, gpio.LOW)#DIGITAL CLOSE DUT#1
        else:
            gpio.output(12, gpio.LOW)#DIGITAL CLOSE DUT#2
            
        setPoint_modulation_a = 0

    elif modoG == 2:
        if inputType_modulation_a == '0-10v':
            modulation_write_a.raw_value = bajo_Mod_0_10
            setPoint_modulation_a = 0
            print("close_0-10v")
        if inputType_modulation_a == '2-10v':
            modulation_write_a.raw_value = bajo_Mod_2_10
            setPoint_modulation_a = 0
            print("close_2-10v")
        if inputType_modulation_a == '0-20mA':
            modulation_write_a.raw_value = bajo_Mod_0_20
            setPoint_modulation_a = 0
            print("close_0-20mA")
        if inputType_modulation_a == '4-20mA':
            modulation_write_a.raw_value = bajo_Mod_4_20
            setPoint_modulation_a = 0
            print("close_4-20mA")
    elif modoG == 3:
        print(client,nodo)
        result2 = client.write_register(2, 0, nodo)
        setPoint_modulation_a = 0
        print("close_modbus_cafe_alone")

def show_read_cafe_alone():
    global client, nodo, modoG, modulation_read_a, inputType_modulation_a, setPoint_modulation_a, position_a

    #-----------------------------------------Al encender CAFE------------------------------------
    port = globals()['port_gpio_alone']
    
    position = 0
    setPoint = 0
    if modoG == 1:
        setPoint = setPoint_modulation_a
        if port == 1:
            #Readig relays feedback DUT#1
            try: 
                relay_O = int(not gpio.input(24))*100
                relay_C = int(not gpio.input(25))*100
                if (relay_O == 0 and relay_C == 0 and setPoint == 100):
                    position = "OP"
                elif (relay_O == 0 and relay_C == 0 and setPoint == 0):
                    position = "CL"
                elif (relay_O != relay_C):
                    position = setPoint
            except:
                pass
        else:
            #Readig relays feedback DUT#2
            try: 
                relay_O = int(not gpio.input(18))*100
                relay_C = int(not gpio.input(23))*100
                if (relay_O == 0 and relay_C == 0 and setPoint == 100):
                    position = "OP"
                elif (relay_O == 0 and relay_C == 0 and setPoint == 0):
                    position = "CL"
                elif (relay_O != relay_C):
                    position = setPoint
            except:
                pass
        
    elif modoG == 2:
        if inputType_modulation_a == '0-10v':   
            position = modulation_read_a.voltage*3.342*2
            valor = random.randint(0,10)
            position = int(map(position, 0,10,0,100))
            setPoint = setPoint_modulation_a
        elif inputType_modulation_a == '2-10v':   
            position = modulation_read_a.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 2,10,0,100))
            setPoint = setPoint_modulation_a
        elif inputType_modulation_a == '0-20mA':   
            position = modulation_read_a.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 0,20,0,100))
            setPoint = setPoint_modulation_a
        elif inputType_modulation_a == '4-20mA':   
            position = modulation_read_a.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 4,20,0,100))
            setPoint = setPoint_modulation_a

    elif modoG == 3:
        #result = client.read_holding_registers(0,3,nodo)
        #position = result.registers[1]
        #setPoint = result.registers[2]
        position = setPoint_modulation_a
        setPoint = setPoint_modulation_a
        
    position_a = position
        
    return position, setPoint

def show_write_start():
    global client, nodo, modoG, flag_a, inputType_modulation_a, modulation_read_a, modulation_write_a, setPoint_modulation_a, position_a, port_gpio_alone

    defSettings = read_default_settings()            #Cargar el width time desde la configuración por defecto
    if (port_gpio_alone == 1):
        widthTimePulse_show = int(defSettings[2][0])
        signalType = defSettings[1]
    elif (port_gpio_alone == 2):
        widthTimePulse_show = int(defSettings[6][0])
        signalType = defSettings[5]
    
    if modoG == 1:
        if port_gpio_alone == 1:
            while not flag_a.is_set():
                gpio.output(20, gpio.HIGH)#DIGITAL OPEN DUT#1
                setPoint_modulation_a = 100
                time.sleep(widthTimePulse_show)

                gpio.output(20, gpio.LOW)#DIGITAL CLOSE DUT#1
                setPoint_modulation_a = 0
                time.sleep(widthTimePulse_show)
        else:
            while not flag_a.is_set():
                gpio.output(12, gpio.HIGH)#DIGITAL OPEN DUT#2
                setPoint_modulation_a = 100
                time.sleep(widthTimePulse_show)
                
                gpio.output(12, gpio.LOW)#DIGITAL LOW DUT#2
                setPoint_modulation_a = 0
                time.sleep(widthTimePulse_show)

    elif modoG == 2:
        if signalType == 'pulseSignal':             #Signal Type PULSE SIGNAL settings default----------------------------------------
            if inputType_modulation_a == '0-10v':
                while not flag_a.is_set():
                    modulation_write_a.raw_value = alto_Mod_0_10
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_0_10
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_a == '2-10v':
                while not flag_a.is_set():
                    modulation_write_a.raw_value = alto_Mod_2_10
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_2_10
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_a == '0-20mA':
                while not flag_a.is_set():
                    modulation_write_a.raw_value = alto_Mod_0_20
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_0_20
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_a == '4-20mA':
                while not flag_a.is_set():
                    modulation_write_a.raw_value = alto_Mod_4_20
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_4_20
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)

        elif signalType == 'sawSignal':             #Signal Type SAW SIGNAL settings default--------------------------------------------
            if inputType_modulation_a == '0-10v':
                i = 0
                porcent_step = 1
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

            elif inputType_modulation_a == '2-10v':
                i = 0
                porcent_step = 1
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

            elif inputType_modulation_a == '0-20mA':
                i = 0
                porcent_step = 1
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    setPoint_modulation_a = int(item)
                    print(fpos)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

            elif inputType_modulation_a == '4-20mA':
                i = 0
                porcent_step = 1
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

        elif signalType == 'scaleSignal':             #Signal Type SCALE SIGNAL settings default--------------------------------------------
            if inputType_modulation_a == '0-10v':
                i = 0
                porcent_step = scale_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_a == '2-10v':
                i = 0
                porcent_step = scale_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_a == '0-20mA':
                i = 0
                porcent_step = scale_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_a == '4-20mA':
                i = 0
                porcent_step = scale_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)
                
    elif modoG == 3:
        if signalType == 'pulseSignal':
            while not flag_a.is_set():
                result2 = client.write_register(2, 100, nodo)
                setPoint_modulation_a = 100
                time.sleep(widthTimePulse_show)

                result2 = client.write_register(2, 0, nodo)
                setPoint_modulation_a = 0
                time.sleep(widthTimePulse_show)
        
        elif signalType == 'sawSignal':
            i = 0
            porcent_step = 1
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            #wtp_show = wtp_show/1000
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_a.is_set():
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_a = int(item)
                client.write_register(2, fpos, nodo)
                position_a = fpos
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(0.1)
       
        elif signalType == 'scaleSignal':
            i = 0
            porcent_step = scale_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            #wtp_show = wtp_show/1000
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_a.is_set():
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_a = int(item)
                result2 = client.write_register(2, fpos, nodo)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(wtp_show)

def turnOn_cafe_alone():
    global client, nodo, modoG, inputType_modulation_a, modulation_write_a, setPoint_modulation_a, tiempoApagadoCafe_a, tiempoEncendidoCafe_a
    #gpio.output(#, gpio.HIGH)  #GPIO Activar GPIO para encender puerto ALONE
    port = globals()['port_gpio_alone']
    opVoltage = globals()['op_voltage_a']

    if port == 1:
        #Encender DUT #1
        pcfRPI_on_off.write("p4", "HIGH")
    elif port == 2:
        #Encender DUT #2
        pcfRPI_on_off.write("p5", "HIGH")

    time.sleep(tiempoEncendidoCafe_a)

        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG == 1:      #Digital
        if port == 1:
            gpio.output(20, gpio.LOW)#DIGITAL OPEN DUT#1
        else:
            gpio.output(12, gpio.LOW)#DIGITAL OPEN DUT#2
            
        setPoint_modulation_a = 100
        print("posicion inicial digital cafe a")
    
    elif modoG == 2:    #Modulation
        if inputType_modulation_a == '0-10v':
            modulation_write_a.raw_value = bajo_Mod_0_10
            setPoint_modulation_a = 0
            print("close_0-10v")
        if inputType_modulation_a == '2-10v':
            modulation_write_a.raw_value = bajo_Mod_2_10
            setPoint_modulation_a = 0
            print("close_2-10v")
        if inputType_modulation_a == '0-20mA':
            modulation_write_a.raw_value = bajo_Mod_0_20
            setPoint_modulation_a = 0
            print("close_0-20mA")
        if inputType_modulation_a == '4-20mA':
            modulation_write_a.raw_value = bajo_Mod_4_20
            setPoint_modulation_a = 0
            print("close_4-20mA")
    
    elif modoG == 3:    #ModBus
        result2 = client.write_register(2, 0, nodo)

def turnOff_cafe_alone():
    global client, nodo, modoG, inputType_modulation_a, modulation_write_a, setPoint_modulation_a, tiempoApagadoCafe_a, position_a
    #gpio.output(#, gpio.LOW)  #GPIO Desactivar GPIO para apagar puerto ALONE
    p = globals()['port_gpio_alone']

        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG == 1:      #Digital
        if p == 1:
            gpio.output(20, gpio.LOW)#DIGITAL OPEN DUT#1
        else:
            gpio.output(12, gpio.LOW)#DIGITAL OPEN DUT#2
            
        setPoint_modulation_a = 100
        print("posicion inicial digital cafe a")
    
    elif modoG == 2:    #Modulation
        if inputType_modulation_a == '0-10v':
            modulation_write_a.raw_value = bajo_Mod_0_10
            setPoint_modulation_a = 0
            print("close_0-10v")
        if inputType_modulation_a == '2-10v':
            modulation_write_a.raw_value = bajo_Mod_2_10
            setPoint_modulation_a = 0
            print("close_2-10v")
        if inputType_modulation_a == '0-20mA':
            modulation_write_a.raw_value = bajo_Mod_0_20
            setPoint_modulation_a = 0
            print("close_0-20mA")
        if inputType_modulation_a == '4-20mA':
            modulation_write_a.raw_value = bajo_Mod_4_20
            setPoint_modulation_a = 0
            print("close_4-20mA")
    
    elif modoG == 3:    #ModBus
        result2 = client.write_register(2, 0, nodo)
        
    '''   
    if position_a > 1:
        time.sleep(tiempoApagadoCafe_a)
    else:
        pass
    '''

    if p == 1:
        #Apagar DUT #1
        pcfRPI_on_off.write("p4", "LOW")
    elif p == 2:
        #Apagar DUT #2
        pcfRPI_on_off.write("p5", "LOW")

    show_stop_cafe_alone()
    if (client != None):
        client.close()

#Funciones SHOW para CAFE 1
def show_start_cafe_1():
    global thread_modbus_1, client_1, modoG_1, nodo_1, running_threads

    if thread_modbus_1 is None or not thread_modbus_1.is_alive():
        thread_modbus_1 = threading.Thread(target=show_write_start_1)
        thread_modbus_1.start()
        running_threads.append(thread_modbus_1)
        print("STAR_cafe_1")

def show_stop_cafe_1():
    global thread_modbus_1, client_1, modoG_1, nodo_1, running_threads,flag_1

    if thread_modbus_1 is not None and thread_modbus_1.is_alive():
        flag_1.set()
        thread_modbus_1.join()
        flag_1.clear()
        print("stop_modbus_cafe_1")    
 
def show_open_cafe_1(posPorcent):
    global client_1, modoG_1, nodo_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1
    if modoG_1 == 1:
        gpio.output(20, gpio.HIGH)#DIGITAL OPEN DUT#1
        setPoint_modulation_1 = 100
        print("open_digital_cafe_1")
    
    elif modoG_1 == 2:
        if inputType_modulation_1 == '0-10v':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_0_10,alto_Mod_0_10))#Convertir la posicion recibida en datos para el DAC
            modulation_write_1.raw_value = pos
            setPoint_modulation_1 = int(posPorcent)
            print("open_0-10v")
        if inputType_modulation_1 == '2-10v':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_2_10,alto_Mod_2_10))           #Convertir la posicion recibida en datos para el DAC
            modulation_write_1.raw_value = pos
            setPoint_modulation_1 = int(posPorcent)
            print("open_2-10v")
        if inputType_modulation_1 == '0-20mA':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_0_20,alto_Mod_0_20 ))           #Convertir la posicion recibida en datos para el DAC
            modulation_write_1.raw_value = pos
            setPoint_modulation_1 = int(posPorcent)
            print("open_0-20mA")
        if inputType_modulation_1 == '4-20mA':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_4_20,alto_Mod_4_20))           #Convertir la posicion recibida en datos para el DAC
            modulation_write_1.raw_value = pos
            setPoint_modulation_1 = int(posPorcent)
            print("open_4-20mA")
    
    elif modoG_1 == 3:
        pos = int(map(int(posPorcent),0,100,0,100))           #Convertir la posicion recibida en datos para el DAC
        result2 = client_1.write_register(2, pos, nodo_1)
        setPoint_modulation_1 = pos

def show_close_cafe_1():
    print("close_cafe_1")
    global client_1, modoG_1, nodo_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1
    if modoG_1 == 1:
        gpio.output(20, gpio.LOW)#DIGITAL CLOSE DUT#1
        setPoint_modulation_1 = 0
        print("close_digital_cafe_1")
    elif modoG_1 == 2:
        if inputType_modulation_1 == '0-10v':
            modulation_write_1.raw_value = bajo_Mod_0_10
            setPoint_modulation_1 = 0
            print("close_0-10v")
        if inputType_modulation_1 == '2-10v':
            modulation_write_1.raw_value = bajo_Mod_2_10
            setPoint_modulation_1 = 0
            print("close_2-10v")
        if inputType_modulation_1 == '0-20mA':
            modulation_write_1.raw_value = bajo_Mod_0_20 
            setPoint_modulation_1 = 0
            print("close_0-20mA")
        if inputType_modulation_1 == '4-20mA':
            modulation_write_1.raw_value = bajo_Mod_4_20 
            setPoint_modulation_1 = 0
            print("close_4-20mA")
    elif modoG_1 == 3:
        result2 = client_1.write_register(2, 0, nodo_1)
        setPoint_modulation_1 = 0

def show_read_cafe_1():
    global client_1, nodo_1, modoG_1, modulation_read_1, inputType_modulation_1, setPoint_modulation_1, position_1

     #-----------------------------------------Al encender CAFE------------------------------------
    position = 0
    setPoint = 0
    if modoG_1 == 1:
        setPoint = setPoint_modulation_1
        #Readig relays feedback DUT#1
        try: 
            relay_O = int(not gpio.input(24))*100
            relay_C = int(not gpio.input(25))*100
            if (relay_O == 0 and relay_C == 0 and setPoint == 100):
                position = "OP"
            elif (relay_O == 0 and relay_C == 0 and setPoint == 0):
                position = "CL"
            elif (relay_O != relay_C):
                position = setPoint
        except:
            pass
    elif modoG_1 == 2:
        if inputType_modulation_1 == '0-10v':   
            position = modulation_read_1.voltage*3.342*2
            valor = random.randint(0,10)
            position = int(map(position, 0,10,0,100))
            setPoint = setPoint_modulation_1
        elif inputType_modulation_1 == '2-10v':   
            position = modulation_read_1.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 2,10,0,100))
            setPoint = setPoint_modulation_1
        elif inputType_modulation_1 == '0-20mA':   
            position = modulation_read_1.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 0,20,0,100))
            setPoint = setPoint_modulation_1
        elif inputType_modulation_1 == '4-20mA':   
            position = modulation_read_1.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 4,20,0,100))
            setPoint = setPoint_modulation_1
    elif modoG_1 == 3:
        # result = client_1.read_holding_registers(0,3,nodo_1)
        # position = result.registers[1]
        # setPoint = result.registers[2]
        position = setPoint_modulation_1
        setPoint = setPoint_modulation_1
        
    position_1 = position
    return position, setPoint

def show_write_start_1():
    global client_1, nodo_1, modoG_1, flag_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1

    defSettings = read_default_settings()            #Cargar el width time desde la configuración por defecto
    widthTimePulse_show = int(defSettings[2][0])
    signalType = defSettings[1]

    if modoG_1 == 1:
        while not flag_1.is_set():
            gpio.output(20, gpio.HIGH)#DIGITAL OPEN DUT#1
            setPoint_modulation_1 = 100
            time.sleep(widthTimePulse_show)

            gpio.output(20, gpio.LOW)#DIGITAL CLOSE DUT#1
            setPoint_modulation_1 = 0
            time.sleep(widthTimePulse_show)
    
    elif modoG_1 == 2:
        if signalType == 'pulseSignal':             #Signal Type PULSE SIGNAL settings default----------------------------------------
            if inputType_modulation_1 == '0-10v':
                while not flag_1.is_set():
                    modulation_write_1.raw_value = alto_Mod_0_10 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_0_10
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_1 == '2-10v':
                while not flag_1.is_set():
                    modulation_write_1.raw_value = alto_Mod_2_10 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_2_10 
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_1 == '0-20mA':
                while not flag_1.is_set():
                    modulation_write_1.raw_value = alto_Mod_0_20 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_0_20 
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_1 == '4-20mA':
                while not flag_1.is_set():
                    modulation_write_1.raw_value = alto_Mod_4_20 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_4_20 
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)

        elif signalType == 'sawSignal':             #Signal Type SAW SIGNAL settings default--------------------------------------------
            if inputType_modulation_1 == '0-10v':
                i = 0
                porcent_step = 1                    #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_1 == '2-10v':
                i = 0
                porcent_step = 1                    #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10 )
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_1 == '0-20mA':
                i = 0
                porcent_step = 1                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_1 == '4-20mA':
                i = 0
                porcent_step = 1                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

        elif signalType == 'scaleSignal':           #Signal Type SCALE SIGNAL settings default--------------------------------------------
            if inputType_modulation_1 == '0-10v':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_1 == '2-10v':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_1 == '0-20mA':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_1 == '4-20mA':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    modulation_write_1.raw_value = int(fpos)
                    setPoint_modulation_1 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)
    
    elif modoG_1 == 3:
        if signalType == 'pulseSignal':
            while not flag_1.is_set():
                result2 = client_1.write_register(2, 100, nodo_1)
                setPoint_modulation_1 = 100
                time.sleep(widthTimePulse_show)

                result2 = client_1.write_register(2, 0, nodo_1)
                setPoint_modulation_1 = 0
                time.sleep(widthTimePulse_show)
        
        elif signalType == 'sawSignal':
            i = 0
            porcent_step = 1
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            #wtp_show = wtp_show/1000
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_1.is_set():
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_1 = int(item)
                client_1.write_register(2, fpos, nodo_1)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(width_time_saw)
       
        elif signalType == 'scaleSignal':
            i = 0
            porcent_step = scale_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            #wtp_show = wtp_show/1000
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_1.is_set():
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_1 = int(item)
                result2 = client_1.write_register(2,fpos, nodo_1)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(wtp_show)

def turnOn_cafe_1():
    global client_1, nodo_1, modoG_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1, tiempoApagadoCafe_1, tiempoEncendidoCafe_a
    #gpio.output(#, gpio.HIGH)  #GPIO Activar GPIO para encender puerto ALONE
    opVoltage = globals()['op_voltage_1']

    #Encender DUT #1
    pcfRPI_on_off.write("p4", "HIGH")

    time.sleep(tiempoEncendidoCafe_a)
        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG_1 == 1:      #Digital
        gpio.output(20, gpio.LOW)#DIGITAL CLOSE DUT#1
        setPoint_modulation_1 = 0
        print("posicion inicial digital cafe a")
    
    elif modoG_1 == 2:    #Modulation
        if inputType_modulation_1 == '0-10v':
            modulation_write_1.raw_value = bajo_Mod_0_10
            setPoint_modulation_1 = 0
            print("close_0-10v")
        if inputType_modulation_1 == '2-10v':
            modulation_write_1.raw_value = bajo_Mod_2_10
            setPoint_modulation_1 = 0
            print("close_2-10v")
        if inputType_modulation_1 == '0-20mA':
            modulation_write_1.raw_value = bajo_Mod_0_20
            setPoint_modulation_1 = 0
            print("close_0-20mA")
        if inputType_modulation_1 == '4-20mA':
            modulation_write_1.raw_value = bajo_Mod_4_20
            setPoint_modulation_1 = 0
            print("close_4-20mA")
    
    elif modoG_1 == 3:    #ModBus
        result2 = client_1.write_register(2, 0, nodo_1)
        setPoint_modulation_1 = 0

def turnOff_cafe_1():
    global client_1, nodo_1, modoG_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1, tiempoApagadoCafe_1, position_1
    #gpio.output(#, gpio.LOW)  #GPIO Desactivar GPIO para apagar puerto ALONE

        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG_1 == 1:      #Digital
        gpio.output(20, gpio.LOW)#DIGITAL CLOSE DUT#1
        setPoint_modulation_1 = 0
        print("posicion inicial digital cafe a")
    
    elif modoG_1 == 2:    #Modulation
        if inputType_modulation_1 == '0-10v':
            modulation_write_1.raw_value = bajo_Mod_0_10
            setPoint_modulation_1 = 0
            print("close_0-10v")
        if inputType_modulation_1 == '2-10v':
            modulation_write_1.raw_value = bajo_Mod_2_10
            setPoint_modulation_1 = 0
            print("close_2-10v")
        if inputType_modulation_1 == '0-20mA':
            modulation_write_1.raw_value = bajo_Mod_0_20
            setPoint_modulation_1 = 0
            print("close_0-20mA")
        if inputType_modulation_1 == '4-20mA':
            modulation_write_1.raw_value = bajo_Mod_4_20
            setPoint_modulation_1 = 0
            print("close_4-20mA")
    
    elif modoG_1 == 3:    #ModBus
        result2 = client_1.write_register(2, 0, nodo)
        setPoint_modulation_1 = 0

    '''
    if position_1 > 1:
        time.sleep(tiempoApagadoCafe_1)
    else:
        pass
    '''

    print("Apagar cafe 1")
    show_stop_cafe_1()
    if (client_1 != None):
        client_1.close()
        
    #Apagar DUT #1
    pcfRPI_on_off.write("p4", "LOW")

#Funciones SHOW para CAFE 2
def show_start_cafe_2():
    global thread_modbus_2, client_2, modoG_2, nodo_2, running_threads

    if thread_modbus_2 is None or not thread_modbus_2.is_alive():
        thread_modbus_2 = threading.Thread(target=show_write_start_2)
        thread_modbus_2.start()
        running_threads.append(thread_modbus_2)     
    print("STAR_cafe_2")

def show_stop_cafe_2():
    global thread_modbus_2, client_2, modoG_2, nodo_2, running_threads, flag_2

    if thread_modbus_2 is not None and thread_modbus_2.is_alive():
        flag_2.set()
        thread_modbus_2.join()
        flag_2.clear()
        print("STOP_cafe_2")   

def show_open_cafe_2(posPorcent):
    global client_2, modoG_2, nodo_2, inputType_modulation_2, modulation_write_2, setPoint_modulation_2
    print("open_cafe_2")
    if modoG_2 == 1:
        gpio.output(12, gpio.HIGH)#DIGITAL OPEN DUT#2
        setPoint_modulation_2 = 100
        print("open_digital_cafe_2")
    elif modoG_2 == 2:
        if inputType_modulation_2 == '0-10v':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_0_10,alto_Mod_0_10))             #Convertir la posicion recibida en datos para el DAC
            modulation_write_2.raw_value = pos
            setPoint_modulation_2 = 100
            print("open_0-10v")
        if inputType_modulation_2 == '2-10v':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_2_10,alto_Mod_2_10))             #Convertir la posicion recibida en datos para el DAC
            modulation_write_2.raw_value = pos
            setPoint_modulation_2 = 100
            print("open_2-10v")
        if inputType_modulation_2 == '0-20mA':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_0_20,alto_Mod_0_20))             #Convertir la posicion recibida en datos para el DAC
            modulation_write_2.raw_value = pos
            setPoint_modulation_2 = 100            
            print("open_0-20mA")
        if inputType_modulation_2 == '4-20mA':
            pos = int(map(int(posPorcent),0,100,bajo_Mod_4_20,alto_Mod_4_20))             #Convertir la posicion recibida en datos para el DAC
            modulation_write_2.raw_value = pos
            setPoint_modulation_2 = 100            
            print("open_4-20mA")
    elif modoG_2 == 3:
        pos = int(map(int(posPorcent),0,100,0,100))           #Convertir la posicion recibida en datos para rs485
        result2 = client_2.write_register(2, pos, nodo_2)
        setPoint_modulation_2 = pos

def show_close_cafe_2():
    print("close_cafe_2")
    global client_2, modoG_2, nodo_2, inputType_modulation_2, modulation_write_2, setPoint_modulation_2
    if modoG_2 == 1:
        gpio.output(12, gpio.LOW)#DIGITAL CLOSE DUT#2
        setPoint_modulation_2 = 0  
        print("close_digital_cafe_2")
    elif modoG_2 == 2:
        if inputType_modulation_2 == '0-10v':
            modulation_write_2.raw_value = bajo_Mod_0_10
            setPoint_modulation_2 = 0            
            print("close_0-10v")
        if inputType_modulation_2 == '2-10v':
            modulation_write_2.raw_value = bajo_Mod_2_10
            setPoint_modulation_2 = 0            
            print("close_2-10v")
        if inputType_modulation_2 == '0-20mA':
            modulation_write_2.raw_value = bajo_Mod_0_20 
            setPoint_modulation_2 = 0            
            print("close_0-20mA")
        if inputType_modulation_2 == '4-20mA':
            modulation_write_2.raw_value = bajo_Mod_4_20 
            setPoint_modulation_2 = 0            
            print("close_4-20mA")
        print("close_modulation_cafe_2")
    elif modoG_2 == 3:
        result2 = client_2.write_register(2, 0, nodo_2)
        setPoint_modulation_2 = 0

def show_read_cafe_2():
    global client_2, nodo_2, modoG_2, modulation_read_2, inputType_modulation_2, setPoint_modulation_2, position_2

    #-----------------------------------------Al encender CAFE------------------------------------
    position = 0
    setPoint = 0
    if modoG_2 == 1:
        setPoint = setPoint_modulation_2
        #Readig relays feedback DUT#2
        try: 
            relay_O = int(not gpio.input(18))*100
            relay_C = int(not gpio.input(23))*100
            if (relay_O == 0 and relay_C == 0 and setPoint == 100):
                position = "OP"
            elif (relay_O == 0 and relay_C == 0 and setPoint == 0):
                position = "CL"
            elif (relay_O != relay_C):
                position = setPoint
        except:
            pass

    elif modoG_2 == 2:
        if inputType_modulation_2 == '0-10v':   
            position = modulation_read_2.voltage*3.342*2
            valor = random.randint(0,10)
            position = int(map(position, 0,10,0,100))
            setPoint = setPoint_modulation_2
        elif inputType_modulation_2 == '2-10v':   
            position = modulation_read_2.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 2,10,0,100))
            setPoint = setPoint_modulation_2
        elif inputType_modulation_2 == '0-20mA':   
            position = modulation_read_2.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 0,20,0,100))
            setPoint = setPoint_modulation_2
        elif inputType_modulation_2 == '4-20mA':   
            position = modulation_read_2.voltage*3.342*2
            valor = random.randint(2,10)
            position = int(map(position, 4,20,0,100))
            setPoint = setPoint_modulation_2

    elif modoG_2 == 3:
        # result = client_2.read_holding_registers(0,3,nodo_2)
        # position = result.registers[1]
        # setPoint = result.registers[2]
        position = setPoint_modulation_2
        setPoint = setPoint_modulation_2
    
    position_2 = position

    return position, setPoint

def show_write_start_2():
    global client_2, nodo_2, modoG_2, flag_2, inputType_modulation_2, modulation_read_2, modulation_write_2, setPoint_modulation_2, bajo_Mod_0_10

    defSettings = read_default_settings()            #Cargar el width time desde la configuración por defecto
    widthTimePulse_show = int(defSettings[6][0])
    signalType = defSettings[5]

    if modoG_2 == 1:
        while not flag_2.is_set():
            gpio.output(12, gpio.HIGH)#DIGITAL OPEN DUT#2
            setPoint_modulation_2 = 100
            time.sleep(widthTimePulse_show)
            
            gpio.output(12, gpio.LOW)#DIGITAL LOW DUT#2
            setPoint_modulation_2 = 0
            time.sleep(widthTimePulse_show)
    
    elif modoG_2 == 2:
        if signalType == 'pulseSignal':             #Signal Type PULSE SIGNAL settings default----------------------------------------
            if inputType_modulation_2 == '0-10v':
                while not flag_2.is_set():
                    modulation_write_2.raw_value = alto_Mod_0_10
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_0_10
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_2 == '2-10v':
                while not flag_2.is_set():
                    modulation_write_2.raw_value = alto_Mod_2_10
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_2_10
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_2 == '0-20mA':
                while not flag_2.is_set():
                    modulation_write_2.raw_value = alto_Mod_0_20 
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_0_20 
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_2 == '4-20mA':
                while not flag_2.is_set():
                    modulation_write_2.raw_value = alto_Mod_4_20 
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_4_20 
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)

        elif signalType == 'sawSignal':             #Signal Type SAW SIGNAL settings default--------------------------------------------
            if inputType_modulation_2 == '0-10v':
                i = 0
                porcent_step = 1                    #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

            elif inputType_modulation_2 == '2-10v':
                i = 0
                porcent_step = 1                    #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

            elif inputType_modulation_2 == '0-20mA':
                i = 0
                porcent_step = 1                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

            elif inputType_modulation_2 == '4-20mA':
                i = 0
                porcent_step = 1                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(0.3)

        elif signalType == 'scaleSignal':           #Signal Type SCALE SIGNAL settings default--------------------------------------------
            if inputType_modulation_2 == '0-10v':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_2 == '2-10v':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_2 == '0-20mA':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)

            elif inputType_modulation_2 == '4-20mA':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                #wtp_show = wtp_show/1000
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(wtp_show)   
    
    elif modoG_2 == 3:
        if signalType == 'pulseSignal':
            while not flag_2.is_set():
                result2 = client_2.write_register(2, 100, nodo_2)
                setPoint_modulation_2 = 100
                time.sleep(widthTimePulse_show)

                result2 = client_2.write_register(2, 0, nodo_2)
                setPoint_modulation_2 = 0
                time.sleep(widthTimePulse_show)
        
        elif signalType == 'sawSignal':
            i = 0
            porcent_step = 1
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            #wtp_show = wtp_show/1000
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_2.is_set():
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_2 = int(item)
                client_2.write_register(2, fpos, nodo_2)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(width_time_saw)
       
        elif signalType == 'scaleSignal':
            i = 0
            porcent_step = scale_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            #wtp_show = wtp_show/1000
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_2.is_set():
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_2 = int(item)
                result2 = client_2.write_register(2, fpos, nodo_2)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(wtp_show)

def turnOn_cafe_2():
    global client_2, nodo_2, modoG_2, inputType_modulation_2, modulation_write_2, setPoint_modulation_2, tiempoEncendidoCafe_a

    #gpio.output(#, gpio.HIGH)  #GPIO Activar GPIO para encender puerto ALONE
    opVoltage = globals()['op_voltage_2']
    
    #Encender DUT #2
    pcfRPI_on_off.write("p5", "HIGH")
    
    time.sleep(tiempoEncendidoCafe_a)

        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG_2 == 1:      #Digital
        print("posicion inicial digital cafe a")
    
    elif modoG_2 == 2:    #Modulation
        if inputType_modulation_2 == '0-10v':
            modulation_write_2.raw_value = bajo_Mod_0_10
            setPoint_modulation_2 = 0
            print("close_0-10v")
        if inputType_modulation_2 == '2-10v':
            modulation_write_2.raw_value = bajo_Mod_2_10
            setPoint_modulation_2 = 0
            print("close_2-10v")
        if inputType_modulation_2 == '0-20mA':
            modulation_write_2.raw_value = bajo_Mod_0_20
            setPoint_modulation_2 = 0
            print("close_0-20mA")
        if inputType_modulation_2 == '4-20mA':
            modulation_write_2.raw_value = bajo_Mod_4_20
            setPoint_modulation_2 = 0
            print("close_4-20mA")
    
    elif modoG_2 == 3:    #ModBus
        result2 = client_2.write_register(2, 0, nodo_2)
        setPoint_modulation_2 = 0

def turnOff_cafe_2():
    global client_2, nodo_2, modoG_2, inputType_modulation_2, modulation_write_2, setPoint_modulation_2, tiempoApagadoCafe_2, position_2
    #gpio.output(#, gpio.LOW)  #GPIO Desactivar GPIO para apagar puerto ALONE

        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG_2 == 1:      #Digital
        print("posicion inicial digital cafe a")
    
    elif modoG_2 == 2:    #Modulation
        if inputType_modulation_2 == '0-10v':
            modulation_write_2.raw_value = bajo_Mod_0_10
            setPoint_modulation_2 = 0
            print("close_0-10v")
        if inputType_modulation_2 == '2-10v':
            modulation_write_2.raw_value = bajo_Mod_2_10 
            setPoint_modulation_2 = 0
            print("close_2-10v")
        if inputType_modulation_2 == '0-20mA':
            modulation_write_2.raw_value = bajo_Mod_0_20 
            setPoint_modulation_2 = 0
            print("close_0-20mA")
        if inputType_modulation_2 == '4-20mA':
            modulation_write_2.raw_value = bajo_Mod_4_20 
            setPoint_modulation_2 = 0
            print("close_4-20mA")
    
    elif modoG_2 == 3:    #ModBus
        result2 = client_2.write_register(2, 0, nodo_2)
        setPoint_modulation_2 = 0


    '''
    if position_2 > 1:
        time.sleep(tiempoApagadoCafe_2)
    else:
        pass
    '''

    print("Apagar cafe 2")
    show_stop_cafe_2()
    if (client_2 != None):
        client_2.close()
        
    #Apagar DUT #2
    pcfRPI_on_off.write("p5", "LOW")

#Funciones SHOW para COIL alone
def show_start_coil_alone():
    global thread_modbus_a, running_threads

    if thread_modbus_a is None or not thread_modbus_a.is_alive():
        thread_modbus_a = threading.Thread(target=show_write_start_coil_a)
        thread_modbus_a.start()
        running_threads.append(thread_modbus_a) 

def show_stop_coil_alone():
    global thread_modbus_a, flag_a, port_gpio_alone

    #Cerrar solenoide en AUTO
    if port_gpio_alone == 1:
        #Apagar DUT #1
        pcfRPI_on_off.write("p4", "LOW")
    elif port_gpio_alone == 2:
        #Apagar DUT #2
        pcfRPI_on_off.write("p5", "LOW")


    if thread_modbus_a is not None and thread_modbus_a.is_alive():
        flag_a.set()
        thread_modbus_a.join()
        flag_a.clear()
    print("Stop coil alone")

def show_open_coil_alone():
    port = globals()['port_gpio_alone']
    
    if port == 1:
        #Encender DUT #1
        pcfRPI_on_off.write("p4", "HIGH")
    elif port == 2:
        #Encender DUT #2
        pcfRPI_on_off.write("p5", "HIGH")

def show_close_coil_alone():
    port = globals()['port_gpio_alone']
    
    if port == 1:
        #Apagar DUT #1
        pcfRPI_on_off.write("p4", "LOW")
    elif port == 2:
        #Apagar DUT #2
        pcfRPI_on_off.write("p5", "LOW")

def show_write_start_coil_a():
    global flag_a, posCoil_a, port_gpio_alone

    defSettings = read_default_settings()            #Cargar el width time desde la configuración por defecto
    print(defSettings)
    if (port_gpio_alone == 1):
        widthTimePulse_show = int(defSettings[3][0])
    elif (port_gpio_alone == 2):
        widthTimePulse_show = int(defSettings[7][0])

    while not flag_a.is_set():
        #Abrir solenoide en AUTO
        if port_gpio_alone == 1:
            #Encender DUT #1
            pcfRPI_on_off.write("p4", "HIGH")
        elif port_gpio_alone == 2:
            #Encender DUT #2
            pcfRPI_on_off.write("p5", "HIGH")

        posCoil_a = 'open'
        time.sleep(widthTimePulse_show)

        #Cerrar solenoide en AUTO
        if port_gpio_alone == 1:
            #Apagar DUT #1
            pcfRPI_on_off.write("p4", "LOW")
        elif port_gpio_alone == 2:
            #Apagar DUT #2
            pcfRPI_on_off.write("p5", "LOW")

        posCoil_a = 'close'
        time.sleep(widthTimePulse_show)

def show_read_coil_alone():
    global posCoil_a

    return posCoil_a

#Funciones SHOW para COIL 1
def show_start_coil_1():
    global thread_modbus_1, running_threads

    if thread_modbus_1 is None or not thread_modbus_1.is_alive():
        thread_modbus_1 = threading.Thread(target=show_write_start_coil_1)
        thread_modbus_1.start()
        running_threads.append(thread_modbus_1) 

def show_stop_coil_1():
    global thread_modbus_1, flag_1

    pcfRPI_on_off.write("p4", "LOW")

    if thread_modbus_1 is not None and thread_modbus_1.is_alive():
        flag_1.set()
        thread_modbus_1.join()
        flag_1.clear()
    print("Stop coil 1")

def show_open_coil_1():
    pcfRPI_on_off.write("p4", "HIGH")

def show_close_coil_1():
    pcfRPI_on_off.write("p4", "LOW")

def show_write_start_coil_1():
    global flag_1, posCoil_1

    defSettings = read_default_settings()            #Cargar el width time desde la configuración por defecto
    widthTimePulse_show = int(defSettings[3][0])

    while not flag_1.is_set():
        pcfRPI_on_off.write("p4", "HIGH")
        posCoil_1 = 'open'
        time.sleep(widthTimePulse_show)

        pcfRPI_on_off.write("p4", "LOW")
        posCoil_1 = 'close'
        time.sleep(widthTimePulse_show)

def show_read_coil_1():
    global posCoil_1

    return posCoil_1

#Funciones SHOW para COIL 2
def show_start_coil_2():
    global thread_modbus_2, running_threads

    if thread_modbus_2 is None or not thread_modbus_2.is_alive():
        thread_modbus_2 = threading.Thread(target=show_write_start_coil_2)
        thread_modbus_2.start()
        running_threads.append(thread_modbus_2) 
    print("Start coil 2")

def show_stop_coil_2():
    global thread_modbus_2, flag_2
    
    pcfRPI_on_off.write("p5", "LOW")

    if thread_modbus_2 is not None and thread_modbus_2.is_alive():
        flag_2.set()
        thread_modbus_2.join()
        flag_2.clear()
    print("Stop coil 2")

def show_open_coil_2():
    pcfRPI_on_off.write("p5", "HIGH")

def show_close_coil_2():
    pcfRPI_on_off.write("p5", "LOW")

def show_write_start_coil_2():
    global flag_2, posCoil_2

    defSettings = read_default_settings()            #Cargar el width time desde la configuración por defecto
    widthTimePulse_show = int(defSettings[7][0])

    while not flag_2.is_set():
        pcfRPI_on_off.write("p5", "HIGH")
        posCoil_2 = 'open'
        time.sleep(widthTimePulse_show)

        pcfRPI_on_off.write("p5", "LOW")
        posCoil_2 = 'close'
        time.sleep(widthTimePulse_show)

def show_read_coil_2():
    global posCoil_2

    return posCoil_2

#Funciones SHOW para LIMIT SWITCH Alone
def show_read_ls_alone():
    global port_gpio_alone

    try:
        if (port_gpio_alone == 1):
            relay_O = int(not gpio.input(24))
            relay_C = int(not gpio.input(25))
        elif (port_gpio_alone == 2):
            relay_O = int(not gpio.input(18))
            relay_C = int(not gpio.input(23))          
    except:
        pass

    state = ""

    print(relay_O, relay_C)

    if relay_O == 0 and relay_C == 0:
        state = "tran"
    elif relay_O == 1 and relay_C == 0:
        state = "open"
    elif relay_O == 0 and relay_C == 1:
        state = "close"

    return state

def turnOn_ls_alone():
    print("Encender limit switch alone")

def turnOff_ls_alone():
    print("Apagar limit switch alone")

#Funciones SHOW para LIMIT SWITCH 1
def show_read_ls_1():
    try:
        relay_O = int(not gpio.input(24))
        relay_C = int(not gpio.input(25))    
    except:
        pass

    state = ""

    if relay_O == 0 and relay_C == 0:
        state = "tran"
    elif relay_O == 1 and relay_C == 0:
        state = "open"
    elif relay_O == 0 and relay_C == 1:
        state = "close"

    return state

def turnOn_ls_1():
    print("Encender limit switch 1")

def turnOff_ls_1():
    print("Apagar limit switch 1")

#Funciones SHOW para LIMIT SWITCH 2
def show_read_ls_2():
    try:
        relay_O = int(not gpio.input(18))
        relay_C = int(not gpio.input(23))
    except:
        pass

    state = ""

    if relay_O == 0 and relay_C == 0:
        state = "tran"
    elif relay_O == 1 and relay_C == 0:
        state = "open"
    elif relay_O == 0 and relay_C == 1:
        state = "close"

    return state

def turnOn_ls_2():
    print("Encender limit switch 2")

def turnOff_ls_2():
    print("Apagar limit switch 2")

def params_only_show(_data_dut_1, _data_dut_2, _cant_duts, modo):
    _name_alone_dut = 'NONE'
    _name_dut_1 = _data_dut_1[2]
    _name_dut_2 = _data_dut_2[2]
    _id_dut = 0
    if _data_dut_1[0] == 1:
        _id_dut = 'DUT #1'
        #_name_dut_1 = 0
        _name_alone_dut = _data_dut_1[2]
    elif _data_dut_2[0] == 1:
        _id_dut = 'DUT #2'
        #_name_dut_2 = 0
        _name_alone_dut = _data_dut_2[2]

    respuesta = _id_dut+','+_name_alone_dut+','+_name_dut_1+','+_name_dut_2

    return respuesta

def map(valor, desde_min, desde_max, a_min, a_max):
    # Asegurarse de que el valor esté dentro del rango original
    valor = max(desde_min, min(valor, desde_max))
    
    # Calcular el mapeo
    return (valor - desde_min) * (a_max - a_min) / (desde_max - desde_min) + a_min

def turn_off_all():
    #try:
    turnOff_cafe_1()
    #except:
    #   pass
        
    #try:
    turnOff_cafe_2()
    #except:
    #   pass
        
    try:
        turnOff_cafe_alone()
    except:
        pass
        
    print("apagar todo")

def stop():
    global client,client_1, client_2, cant_duts, port_gpio_alone, name_dut_1, name_dut_2, dut_alone, modo_dut_1, modo_dut_2, modo_dut_alone

    #si hay 1 DUT
    if cant_duts == 1:
        if dut_alone == 'CAFE':
            show_stop_cafe_alone()
            if (client != None):
                client.close()
            turnOff_cafe_alone()
        elif dut_alone == 'COIL':
            show_stop_coil_alone()
            show_close_coil_alone()
        elif dut_alone == 'LIMIT SWITCH':
            turnOn_ls_alone()

    elif cant_duts == 2:
        #-------------STOP DUT #1-------------#
        if name_dut_1 == 'CAFE':
            show_stop_cafe_1()
            if (client_1 != None):
                client_1.close()
            turnOff_cafe_1()
        elif name_dut_1 == 'COIL':
            show_stop_coil_1()
            show_close_coil_1()
        elif name_dut_1 == 'LIMIT SWITCH':
            turnOff_ls_1()

        #-------------STOP DUT #2-------------#
        if name_dut_2 == 'CAFE':
            show_stop_cafe_2()
            if (client_2 != None):
                client_2.close()
            turnOff_cafe_2()
        elif name_dut_2 == 'COIL':
            show_stop_coil_2()
            show_close_coil_2()
        elif name_dut_2 == 'LIMIT SWITCH':
            turnOff_ls_2()
        
    #Terminar todos los clientes ModBus



    #Apagar los dos puertos
    #gpio.output(#, gpio.LOW)  #GPIO Desactivar GPIO para apagar puerto ALONE
    print("PARAR TODOS LOS HILOS")

def config_def_settings():
    global port_gpio_alone

    defData = read_default_settings()

    #Se anade los valores por defecto dependiendo del dut alone
    if port_gpio_alone == 1:
        defData.extend([defData[1], defData[2], defData[3]])
    elif port_gpio_alone == 2:
        defData.extend([defData[5], defData[6], defData[7]])
    else:
        defData.extend([0, 0, 0])

    return defData

def read_default_settings():
    otra = []
    registro = defSet.objects.get(id=1)

    for field in registro._meta.fields:
        otra.append(getattr(registro, field.name))

    otra.pop(0)
    aDefSet = otra
    return aDefSet
