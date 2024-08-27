#prueba git 3 raspberry pi
from datetime import datetime
from pymodbus.client import ModbusSerialClient
#import minimalmodbus
import threading
import time
import random
import json
import numpy as np
from cycle_test.models import tempDataCt_a as tDataCt_a
from cycle_test.models import cycleTestData as ctd
import pytz

""""""
try:
    import pcf8574_io
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
    pass
""""""

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
    
tDataCt_a.objects.all().delete

widthTimePulse_show = 6

#modo global

# Especificar la zona horaria deseada (ejemplo: 'America/Mexico_City')
zona_horaria = pytz.timezone('America/New_York')

modoG = 0
modoG_1 = 0
modoG_2 = 0
listaP = []

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
saw_porcent = 1
width_time_saw = 0.1
tOutModbus = 0.5

#--------------------------------- Cycle Test Data-----------------------------------------#
testerName_g = ''
actuatorRef_g = ''
load_g = False
loadDetails_g = ''
#--------------------------------------------CAFE ALONE--------------------------------------------#
modo_dut_alone = ''
dut_alone = ''

puerto_dut_alone = None
posAnteriorA_a = 0
posAnteriorB_a = 0

counter_open_cafe_a = 0
counter_close_cafe_a = 0

controlSignal_a = 0
feedbackSignal_a = 0
relayO_a = 0
relayC_a = 0

pausa_hilo = False
tiempoApagadoCafe_a = 6
tiempoEncendidoCafe_a = 3
op_voltage_a = None
#Encender puerto alone
port_gpio_alone = None
#parametros modulation ALONE
modulation_write_a = None
modulation_read_a = None
inputType_modulation_a = 0
setPoint_modulation_a = 0
widthTimePulse_a = None
signalType_a = None
position_a = 0
#parametros modbus ALONE
client = None
nodo = 1
baud = 19200
flag_a = threading.Event()
# Bandera para controlar la pausa del cronómetro
pausa_flag_a = threading.Event()
flag_c_a = threading.Event()
thread_modbus_a = None
cronometro_a = None
thread_crono_a = None

posMod_a = 0
setPointMod_a = 0
flag_read_a = threading.Event()
thread_readMod_a = None

temp_a = [None]*1000
current_a = [None]*1000
setPoint_a = [None]*1000
feedback_a = [None]*1000
relayFeO_a = [None]*1000
relayFeC_a = [None]*1000
timeStamp_a = [None]*1000
indexDB_a = 0

thread_saveDB_a = None
flag_thread_saveDB_a = threading.Event()
#----------------CRONOMETRO------------#
inicio = 0
tiempo_pausado = 0
en_progreso = False
tiempo_total_a = 0
hilo = None
_detener_hilo = threading.Event()
minutos_cafe_a = 0
segundos_cafe_a = 0
horas_cafe_a = 0

dateStart_a = None
dateEnd_a = None

#----------------------------------------------CAFE 1----------------------------------------------#
name_dut_1 = ''
modo_dut_1 = ''

posAnteriorA_1 = 0
posAnteriorB_1 = 0

counter_open_cafe_1 = 0
counter_close_cafe_1 = 0

minutos_cafe_1 = 0
segundos_cafe_1 = 0

pausa_hilo_1 = False
tiempoApagadoCafe_1 = 6
tiempoEncendidoCafe_1 = 3
op_voltage_1 = None
#Encender puerto 1
port_gpio_1 = None
#parametros modulation 1
modulation_write_1 = None
modulation_read_1 = None
inputType_modulation_1 = 0
setPoint_modulation_1 = 0
#parametros modbus 1
client_1 = None
nodo_1 = 1
baud_1 = 19200
flag_1 = threading.Event()
flag_c_1 = threading.Event()

posMod_1 = 0
setPointMod_1 = 0
flag_read_1 = threading.Event()
thread_readMod_1 = None
posAnt_modBus_1 = 0

thread_modbus_1 = None
thread_crono_1 = None
#----------------------------------------------CAFE 2----------------------------------------------#
name_dut_2 = ''
modo_dut_2 = ''

posAnteriorA_2 = 0
posAnteriorB_2 = 0

counter_open_cafe_2 = 0
counter_close_cafe_2 = 0

minutos_cafe_2 = 0
segundos_cafe_2 = 0

pausa_hilo_2 = False
tiempoApagadoCafe_2 = 6
tiempoEncendidoCafe_2 = 3
op_voltage_2 = None
#Encender puerto 2
port_gpio_2 = None
#parametros modulation 2
modulation_write_2 = None
modulation_read_2 = None
inputType_modulation_2 = 0
setPoint_modulation_2 = 0
#parametros modbus 2
client_2 = None
nodo_2 = 1
baud_2 = 19200
flag_2 = threading.Event()
flag_c_2 = threading.Event()

posMod_2 = 0
setPointMod_2 = 0
flag_read_2 = threading.Event()
thread_readMod_2 = None
posAnt_modBus_2 = 0
permiso_read_2 = False

thread_modbus_2 = None
thread_crono_2 = None
#----------------------------------------------COIL ALONE----------------------------------------------#
posCoil_a = None
#----------------------------------------------COIL 1----------------------------------------------#
posCoil_1 = None
#----------------------------------------------COIL 2----------------------------------------------#
posCoil_2 = None

stop_condition = threading.Condition()
running_threads = []

def extraer_parametros(parametrosR, modo):
    global listaP

    parametros = parametrosR.split(',')
    listaP = []
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
    global client,modoG,nodo,baud,client_1,modoG_1,nodo_1,client_2,modoG_2,nodo_2,modulation_read_a,modulation_write_a,inputType_modulation_a,\
    modulation_read_1,modulation_write_1,inputType_modulation_1,modulation_read_2,modulation_write_2,inputType_modulation_2,port_gpio_alone,\
    op_voltage_a,op_voltage_1,op_voltage_2,puerto_dut_alone, dut_alone

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
                    puerto = '/dev/ttyUSB1'
                    #Switch Relay Modulation/Modbus DUT #1
                    pcfRPI.write("p4", "LOW")
                    
                else:
                    puerto = '/dev/ttyUSB0'
                    #Switch Relay Modulation/Modbus DUT #2
                    pcfRPI.write("p5", "LOW")
                
                nodo = int(parametros[10])
                baud = int(parametros[7].split('|')[0])
                modoG = 3
                client = ModbusSerialClient(
                method = 'rtu'
                ,port=puerto
                ,baudrate=baud
                ,parity = 'N'
                ,timeout=tOutModbus
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
                    pcfRPI.write("p4", "HIGH")
                    """"""
                except:
                    pass

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
                #Switch Relay Modulation/Modbus
                pcfRPI.write("p4", "LOW")

                modoG_1 = 3
                nodo_1 = int(parametros[20])
                baud_1 = int(parametros[17].split('|')[0])
                puerto_1 = '/dev/ttyUSB0'

                client_1 = ModbusSerialClient(
                method = 'rtu'
                ,port = puerto_1
                ,baudrate = baud_1
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
                #Switch Relay Modulation/Modbus
                pcfRPI.write("p5", "LOW")
                modoG_2 = 3
                nodo_2 = int(parametros[27])
                baud_2 = int(parametros[24].split('|')[0])
                puerto_2 = '/dev/ttyUSB1'
                client_2 = ModbusSerialClient(
                method = 'rtu'
                ,port=puerto_2
                ,baudrate=baud_2
                ,parity = 'N'
                ,timeout=tOutModbus
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

#Funciones CYCLE TEST para CAFE alone
def cycleTest_start_cafe_alone():
    global thread_modbus_a, thread_crono_a, client, modoG, nodo, running_threads, counter_open_cafe_a,\
           counter_close_cafe_a, minutos_cafe_a, segundos_cafe_a, thread_readMod_a

    counter_open_cafe_a = 0
    counter_close_cafe_a = 0

    if thread_modbus_a is None or not thread_modbus_a.is_alive():
        thread_modbus_a = threading.Thread(target=cycleTest_write_start)
        thread_modbus_a.start()
        running_threads.append(thread_modbus_a) 
    
    reiniciar()
    iniciar()
    start_saveInDB_a()
    
    if modoG == 3:
        if thread_readMod_a is None or not thread_readMod_a.is_alive():
            thread_readMod_a = threading.Thread(target=theread_read_cafe_alone)
            thread_readMod_a.start()
            running_threads.append(thread_readMod_a)
    else:
        pass

def cycleTest_stop_cafe_alone():
    global thread_modbus_a, client, modoG, nodo, running_threads,flag_a,flag_c_a,thread_crono_a, minutos_cafe_a, segundos_cafe_a, thread_readMod_a,\
           flag_read_a

    if thread_modbus_a is not None and thread_modbus_a.is_alive():
        flag_a.set()
        thread_modbus_a.join()
        flag_a.clear()

    detener()
    reiniciar()
    stop_saveInDB_a()
    joinTemporalDB_a()

    if modoG == 3:
        if thread_readMod_a is not None and thread_readMod_a.is_alive():
            flag_read_a.set()
            thread_readMod_a.join()
            flag_read_a.clear()
    else:
        pass

def cycleTest_write_start():
    global client, nodo, modoG, flag_a, inputType_modulation_a, modulation_read_a, modulation_write_a, setPoint_modulation_a, port_gpio_alone,\
    listaP, pausa_hilo, signalType_a, widthTimePulse_a

    setPoint_modulation_a = 0
    widthTimePulse_show = int(listaP[5][0])
    widthTimePulse_a = int(listaP[5][0])
    signalType = listaP[4]
    signalType_a = listaP[4]
    
    if modoG == 1:
        print("open_digital_cafe_alone")

    elif modoG == 2:
        if signalType == 'pulseSignal':             #Signal Type PULSE SIGNAL settings default----------------------------------------
            if inputType_modulation_a == '0-10v':
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    modulation_write_a.raw_value = alto_Mod_0_10
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_0_10
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_a == '2-10v':
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    modulation_write_a.raw_value = alto_Mod_2_10
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_2_10
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_a == '0-20mA':
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    modulation_write_a.raw_value = alto_Mod_0_20
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_0_20
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_a == '4-20mA':
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    modulation_write_a.raw_value = alto_Mod_4_20
                    setPoint_modulation_a = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_a.raw_value = bajo_Mod_4_20
                    setPoint_modulation_a = 0
                    time.sleep(widthTimePulse_show)

        elif signalType == 'sawSignal':             #Signal Type SAW SIGNAL settings default--------------------------------------------
            if inputType_modulation_a == '0-10v':
                i = 0
                porcent_step = saw_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_a == '2-10v':
                i = 0
                porcent_step = saw_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_a == '0-20mA':
                i = 0
                porcent_step = saw_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_a == '4-20mA':
                i = 0
                porcent_step = saw_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    setPoint_modulation_a = int(item)
                    modulation_write_a.raw_value = int(fpos)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

        elif signalType == 'scaleSignal':             #Signal Type SCALE SIGNAL settings default--------------------------------------------
            if inputType_modulation_a == '0-10v':
                i = 0
                porcent_step = scale_porcent
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_a.is_set():
                    while pausa_hilo == True:
                        time.sleep(0.1)
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
                while pausa_hilo == True:
                    time.sleep(0.1)
                result2 = client.write_register(2, 100, nodo)
                #client.write_register(2, 100, functioncode=6)
                setPoint_modulation_a = 100
                time.sleep(widthTimePulse_show)

                result2 = client.write_register(2, 0, nodo)
                #client.write_register(2, 0, functioncode=6)
                setPoint_modulation_a = 0
                time.sleep(widthTimePulse_show)
        
        elif signalType == 'sawSignal':
            i = 0
            porcent_step = saw_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_a.is_set():
                while pausa_hilo == True:
                    time.sleep(0.1)
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_a = int(item)
                client.write_register(2, fpos, nodo)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(width_time_saw)
       
        elif signalType == 'scaleSignal':
            i = 0
            porcent_step = scale_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_a.is_set():
                while pausa_hilo == True:
                    time.sleep(0.1)
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_a = int(item)
                result2 = client.write_register(2, fpos, nodo)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(wtp_show)

def cycleTest_read_cafe_alone():
    global client, nodo, modoG, modulation_read_a, inputType_modulation_a, setPoint_modulation_a, listaP, counter_open_cafe_a,\
    counter_close_cafe_a, minutos_cafe_a, segundos_cafe_a, puerto_dut_alone, posMod_a, relayO_a, relayC_a, controlSignal_a,\
    feedbackSignal_a, position_a, horas_cafe_a

    signalType_a = listaP[4]
    #-----------------------------------------Al encender CAFE------------------------------------
    port = globals()['port_gpio_alone']
    
    position = 0
    setPoint = 0
    if modoG == 1:
        setPoint = setPoint_modulation_a
        if port == 1:
            #Readig relays feedback DUT#1
            try: 
                relay_Od = int(not gpio.input(24))*100
                relay_Cd = int(not gpio.input(25))*100
                if (relay_Od == 0 and relay_Cd == 0 and setPoint == 100):
                    position = "OP"
                elif (relay_Od == 0 and relay_Cd == 0 and setPoint == 0):
                    position = "CL"
                elif (relay_Od != relay_Cd):
                    position = setPoint
            except:
                pass
        else:
            #Readig relays feedback DUT#2
            try: 
                relay_Od = int(not gpio.input(18))*100
                relay_Cd = int(not gpio.input(23))*100
                if (relay_Od == 0 and relay_Cd == 0 and setPoint == 100):
                    position = "OP"
                elif (relay_Od == 0 and relay_Cd == 0 and setPoint == 0):
                    position = "CL"
                elif (relay_Od != relay_Cd):
                    position = setPoint
            except:
                pass
    
    elif modoG == 2:
        if inputType_modulation_a == '0-10v':   
            position = modulation_read_a.voltage*3.342*2
            position = int(map(position, 0,10,0,100))
            setPoint = setPoint_modulation_a
        elif inputType_modulation_a == '2-10v':   
            position = modulation_read_a.voltage*3.342*2
            position = int(map(position, 2,10,0,100))
            setPoint = setPoint_modulation_a
        elif inputType_modulation_a == '0-20mA':   
            position = modulation_read_a.voltage*3.342*2
            position = int(map(position, 0,20,0,100))
            setPoint = setPoint_modulation_a
        elif inputType_modulation_a == '4-20mA':   
            position = modulation_read_a.voltage*3.342*2
            position = int(map(position, 4,20,0,100))
            setPoint = setPoint_modulation_a

    elif modoG == 3:
        position = posMod_a
        setPoint = setPoint_modulation_a

    try:
        if (puerto_dut_alone == 1):
            relay_O = int(not gpio.input(25))*50
            relay_C = int(not gpio.input(24))*50
        elif (puerto_dut_alone == 2):
            relay_O = int(not gpio.input(23))*50
            relay_C = int(not gpio.input(18))*50            
    except:
        relay_O = random.randint(0,100)
        relay_C = random.randint(0,100)

    relayO_a = relay_O
    relayC_a = relay_C
    controlSignal_a = setPoint
    feedbackSignal_a = position

    position_a = position
    
    mostrar_tiempo()

    relay_analysis(relay_O, relay_C)

    return setPoint, position, signalType_a, relay_O, relay_C, counter_open_cafe_a, counter_close_cafe_a, horas_cafe_a, minutos_cafe_a, segundos_cafe_a

def theread_read_cafe_alone():
    global client, nodo, flag_read_a, posMod_a, setPoint_modulation_a
    falla = 0
    while not flag_read_a.is_set():
        if falla < 3:
            try:
                result = client.read_holding_registers(0,3,nodo)
                posMod_a = result.registers[1]
            except:
                falla = falla + 1
            
        else:
            falla = 0
            posMod_a = setPoint_modulation_a
        time.sleep(0.01)

def cycleTest_pause_cafe_alone():
    global pausa_hilo

    pausa_hilo = True
    #pausar_cronometro()
    pausar()

def cycleTest_resume_cafe_alone():
    global pausa_hilo

    pausa_hilo = False
    #reanudar_cronometro()
    reanudar()

def relay_analysis(signal_relayA, signal_relayB):
    global posAnteriorA_a, posAnteriorB_a, counter_open_cafe_a, counter_close_cafe_a

    if signal_relayA == 50 and posAnteriorA_a == 0:
        counter_open_cafe_a = counter_open_cafe_a + 1

    if signal_relayB == 50 and posAnteriorB_a == 0:
        counter_close_cafe_a = counter_close_cafe_a + 1

    posAnteriorA_a = signal_relayA
    posAnteriorB_a = signal_relayB

def cronometro():
    global minutos_cafe_a, segundos_cafe_a, tempo_aux
    tiempo_acumulado = 0

    while not flag_c_a.is_set():
        tiempo_inicio = time.time() - tiempo_acumulado
        while not flag_c_a.is_set() and not pausa_flag_a.is_set():
            tiempo_transcurrido = time.time() - tiempo_inicio + tiempo_acumulado
            minutos_cafe_a, segundos_cafe_a = divmod(int(tiempo_transcurrido), 60)
            #print(f"Tiempo transcurrido: {minutos_cafe_a:02}:{segundos_cafe_a:02}", end='\r')
            time.sleep(1)
        tiempo_acumulado = time.time() - tiempo_inicio
        while pausa_flag_a.is_set():
            time.sleep(0.1)

def _actualizar_tiempo():
    global inicio, tiempo_pausado, en_progreso, tiempo_total_a, hilo, _detener_hilo

    while not _detener_hilo.is_set():
        if en_progreso:
            tiempo_total_a = time.time() - inicio
        time.sleep(0.1)

def iniciar():
    global inicio, tiempo_pausado, en_progreso, tiempo_total_a, hilo, _detener_hilo, dateStart_a, zona_horaria

    if not en_progreso:
        dateStart_a = datetime.now(zona_horaria) #Capturar fecha inicial completa

        inicio = time.time() - tiempo_total_a
        en_progreso = True
        if hilo is None:
            _detener_hilo.clear()
            hilo = threading.Thread(target=_actualizar_tiempo)
            hilo.start()
        print("Cronómetro iniciado")

def pausar():
    global inicio, tiempo_pausado, en_progreso, tiempo_total_a, hilo, _detener_hilo
    if en_progreso:
        en_progreso = False
        print("Cronómetro pausado")

def reanudar():
    global inicio, tiempo_pausado, en_progreso, tiempo_total_a, hilo, _detener_hilo
    if not en_progreso:
        inicio = time.time() - tiempo_total_a
        en_progreso = True
        print("Cronómetro reanudado")

def reiniciar():
    global inicio, tiempo_pausado, en_progreso, tiempo_total_a, hilo, _detener_hilo
    en_progreso = False
    tiempo_total_a = 0
    inicio = 0
    print("Cronómetro reiniciado")

def tiempo_transcurrido():
    global tiempo_total_a
    return tiempo_total_a

def mostrar_tiempo():
    global minutos_cafe_a, segundos_cafe_a, horas_cafe_a

    tiempo = tiempo_transcurrido()
    minutos_cafe_a, segundos_cafe_a = divmod(tiempo, 60)
    horas, minutos_cafe_a = divmod(minutos_cafe_a, 60)
    minutos_cafe_a = int(minutos_cafe_a)
    segundos_cafe_a = int(segundos_cafe_a)
    horas_cafe_a = int(horas)

def detener():
    global inicio, tiempo_pausado, en_progreso, tiempo_total_a, hilo, _detener_hilo, dateEnd_a, zona_horaria

    if hilo is not None:
        dateEnd_a = datetime.now(zona_horaria)

        _detener_hilo.set()
        hilo.join()
        hilo = None
        print("Hilo del cronómetro detenido")

# Función para iniciar el cronómetro en un hilo separado
def iniciar_cronometro():
    flag_c_a.clear()
    pausa_flag_a.clear()
    hilo_cronometro = threading.Thread(target=cronometro)
    hilo_cronometro.start()

# Función para detener el cronómetro
def detener_cronometro():
    flag_c_a.set()

# Función para pausar el cronómetro
def pausar_cronometro():
    pausa_flag_a.set()

# Función para reanudar el cronómetro
def reanudar_cronometro():
    pausa_flag_a.clear()

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

    if position_a > 1:
        time.sleep(tiempoApagadoCafe_a)
    else:
        pass

    if p == 1:
        #Apagar DUT #1
        pcfRPI_on_off.write("p4", "LOW")
    elif p == 2:
        #Apagar DUT #2
        pcfRPI_on_off.write("p5", "LOW")

    cycleTest_stop_cafe_alone()
    if (client != None):
        client.close()

def saveInDB_cafe_alone():
    global relayO_a, relayC_a, controlSignal_a, feedbackSignal_a
    print("guardar en db")

#Funciones CYCLE TEST para CAFE #1
def cycleTest_start_cafe_1():
    global thread_modbus_1, thread_crono_1, client_1, modoG_1, nodo_1, running_threads, counter_open_cafe_1,\
           counter_close_cafe_1, minutos_cafe_1, segundos_cafe_1, thread_readMod_1

    counter_open_cafe_1 = 0
    counter_close_cafe_1 = 0

    if thread_modbus_1 is None or not thread_modbus_1.is_alive():
        thread_modbus_1 = threading.Thread(target=cycleTest_write_start_1)
        thread_modbus_1.start()
        running_threads.append(thread_modbus_1) 
    
    if thread_crono_1 is None or not thread_crono_1.is_alive():
        thread_crono_1 = threading.Thread(target=cronometro_1)
        thread_crono_1.start()
        running_threads.append(thread_crono_1)

    if modoG_1 == 3:
        if thread_readMod_1 is None or not thread_readMod_1.is_alive():
            thread_readMod_1 = threading.Thread(target=theread_read_cafe_1)
            thread_readMod_1.start()
            running_threads.append(thread_readMod_1)
    else:
        pass
      
def cycleTest_stop_cafe_1():
    global thread_modbus_1, client_1, modoG_1, nodo_1, running_threads, flag_1, flag_c_1, thread_crono_1, minutos_cafe_1, segundos_cafe_1,\
           thread_readMod_1, flag_read_1

    if thread_modbus_1 is not None and thread_modbus_1.is_alive():
        flag_1.set()
        thread_modbus_1.join()
        flag_1.clear()

    if thread_crono_1 is not None and thread_crono_1.is_alive():
        flag_c_1.set()
        thread_crono_1.join()
        flag_c_1.clear()
        minutos_cafe_1 = 0
        segundos_cafe_1 = 0
    
    if modoG_1 == 3:
        if thread_readMod_1 is not None and thread_readMod_1.is_alive():
            flag_read_1.set()
            thread_readMod_1.join()
            flag_read_1.clear()
    else:
        pass

def cycleTest_write_start_1():
    global client_1, nodo_1, modoG_1, flag_1, inputType_modulation_1, modulation_read_1, modulation_write_1, setPoint_modulation_1, port_gpio_1,\
    listaP, pausa_hilo_1, flag_2
        
    setPoint_modulation_1 = 0
    widthTimePulse_show = int(listaP[15][0])
    signalType = listaP[14]

    if modoG_1 == 1:
        print("open_digital_cafe_alone")
    
    elif modoG_1 == 2:
        if signalType == 'pulseSignal':             #Signal Type PULSE SIGNAL settings default----------------------------------------
            if inputType_modulation_1 == '0-10v':
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
                    modulation_write_1.raw_value = alto_Mod_0_10 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_0_10
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_1 == '2-10v':
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
                    modulation_write_1.raw_value = alto_Mod_2_10 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_2_10 
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_1 == '0-20mA':
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
                    modulation_write_1.raw_value = alto_Mod_0_20 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_0_20 
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_1 == '4-20mA':
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
                    modulation_write_1.raw_value = alto_Mod_4_20 
                    setPoint_modulation_1 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_1.raw_value = bajo_Mod_4_20 
                    setPoint_modulation_1 = 0
                    time.sleep(widthTimePulse_show)

        elif signalType == 'sawSignal':             #Signal Type SAW SIGNAL settings default--------------------------------------------
            if inputType_modulation_1 == '0-10v':
                i = 0
                porcent_step = saw_porcent   #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
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
                porcent_step = saw_porcent    #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)                    
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
                porcent_step = saw_porcent       #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
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
                porcent_step = saw_porcent      #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_1.is_set():
                    while pausa_hilo_1 == True:
                        time.sleep(0.1)                    
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
                while pausa_hilo_1 == True:
                    time.sleep(0.1)
                result1 = client_1.write_register(2, 100, nodo_1)
                setPoint_modulation_1 = 100
                time.sleep(widthTimePulse_show)

                result1 = client_1.write_register(2, 0, nodo_1)
                setPoint_modulation_1 = 0
                time.sleep(widthTimePulse_show)
        
        elif signalType == 'sawSignal':
            i = 0
            porcent_step = saw_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_1.is_set():
                while pausa_hilo_1 == True:
                    time.sleep(0.1)
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
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_1.is_set():
                while pausa_hilo_1 == True:
                    time.sleep(0.1)
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_1 = int(item)
                result2 = client_1.write_register(2,fpos, nodo_1)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(wtp_show)

def cycleTest_read_cafe_1():
    global client_1, nodo_1, modoG_1, modulation_read_1, inputType_modulation_1, setPoint_modulation_1, listaP, counter_open_cafe_1,\
    counter_close_cafe_1, minutos_cafe_1, segundos_cafe_1, posMod_1

    signalType_1 = listaP[14]
    #-----------------------------------------Al encender CAFE------------------------------------
    position = 0
    setPoint = 0
    if modoG_1 == 1:
        print("leyendo digital")
    elif modoG_1 == 2:
        if inputType_modulation_1 == '0-10v':   
            position = modulation_read_1.voltage*3.342*2
            position = int(map(position, 0,10,0,100))
            setPoint = setPoint_modulation_1
        elif inputType_modulation_1 == '2-10v':   
            position = modulation_read_1.voltage*3.342*2
            position = int(map(position, 2,10,0,100))
            setPoint = setPoint_modulation_1
        elif inputType_modulation_1 == '0-20mA':   
            position = modulation_read_1.voltage*3.342*2
            position = int(map(position, 0,20,0,100))
            setPoint = setPoint_modulation_1
        elif inputType_modulation_1 == '4-20mA':   
            position = modulation_read_1.voltage*3.342*2
            position = int(map(position, 4,20,0,100))
            setPoint = setPoint_modulation_1

    elif modoG_1 == 3:
        #result = client_1.read_holding_registers(0,3,nodo_1)
        # try:
        #     position = result.registers[1]
        # except:
        #     position = setPoint_modulation_1

        #position = result.registers[1]
        position = posMod_1
        setPoint = setPoint_modulation_1

    try:
        relay_O = int(not gpio.input(18))*50
        relay_C = int(not gpio.input(23))*50
    except:
        relay_O = random.randint(0,100)
        relay_C = random.randint(0,100)

    relay_analysis_1(relay_O, relay_C)

    return setPoint, position, signalType_1, relay_O, relay_C, counter_open_cafe_1, counter_close_cafe_1, minutos_cafe_1, segundos_cafe_1

def theread_read_cafe_1():
    global client_1, nodo_1, flag_read_1, posMod_1, setPointMod_1, setPoint_modulation_1, posAnt_modBus_1
    falla = 0
    while not flag_read_1.is_set():
        if falla < 3:
            try:
                result = client_1.read_holding_registers(0,3,nodo_1)
                posMod_1 = result.registers[1]
                posAnt_modBus_1 = posMod_1
            except:
                falla = falla + 1
        else:
            falla = 0
            posMod_1 = posAnt_modBus_1
        time.sleep(0.01)

def cycleTest_pause_cafe_1():
    global pausa_hilo_1
    pausa_hilo_1 = True

def cycleTest_resume_cafe_1():
    global pausa_hilo_1
    pausa_hilo_1 = False

def relay_analysis_1(signal_relayA, signal_relayB):
    global posAnteriorA_1, posAnteriorB_1, counter_open_cafe_1, counter_close_cafe_1

    if signal_relayA == 50 and posAnteriorA_1 == 0:
        counter_open_cafe_1 = counter_open_cafe_1 + 1

    if signal_relayB == 50 and posAnteriorB_1 == 0:
        counter_close_cafe_1 = counter_close_cafe_1 + 1

    posAnteriorA_1 = signal_relayA
    posAnteriorB_1 = signal_relayB

def cronometro_1():
    global minutos_cafe_1, segundos_cafe_1
    tiempo_inicio = time.time()
    while not flag_c_1.is_set():
        tiempo_transcurrido = time.time() - tiempo_inicio
        minutos_cafe_1, segundos_cafe_1 = divmod(int(tiempo_transcurrido), 60)
        #print(f"Tiempo transcurrido: {minutos_cafe_a:02}:{segundos_cafe_a:02}", end='\r')
        time.sleep(1)

def turnOn_cafe_1():
    global client_1, nodo_1, modoG_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1, tiempoApagadoCafe_1, tiempoEncendidoCafe_a
    #gpio.output(#, gpio.HIGH)  #GPIO Activar GPIO para encender puerto ALONE
    opVoltage = globals()['op_voltage_1']

    if opVoltage == '24vdc':
        print("Rele 24vdc cafe 1")
    else:
        print("120/240 vdc cafe 1")

    time.sleep(tiempoEncendidoCafe_a)
        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG_1 == 1:      #Digital
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
    global client_1, nodo_1, modoG_1, inputType_modulation_1, modulation_write_1, setPoint_modulation_1, tiempoApagadoCafe_1
    #gpio.output(#, gpio.LOW)  #GPIO Desactivar GPIO para apagar puerto ALONE

        #Posicion inicial en Cero cuando se alimente CAFE
    if modoG_1 == 1:      #Digital
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

    time.sleep(tiempoApagadoCafe_1)

    print("Apagar cafe 1")
    cycleTest_stop_cafe_1()
    if (client_1 != None):
        client_1.close()
#Funciones CYCLE TEST para CAFE #2
def cycleTest_start_cafe_2():
    global thread_modbus_2, thread_crono_2, client_2, modoG_2, nodo_2, running_threads, counter_open_cafe_2,\
           counter_close_cafe_2, minutos_cafe_2, segundos_cafe_2, thread_readMod_2

    counter_open_cafe_2 = 0
    counter_close_cafe_2 = 0

    if thread_modbus_2 is None or not thread_modbus_2.is_alive():
        thread_modbus_2 = threading.Thread(target=cycleTest_write_start_2)
        thread_modbus_2.start()
        running_threads.append(thread_modbus_2) 
    
    if thread_crono_2 is None or not thread_crono_2.is_alive():
        thread_crono_2 = threading.Thread(target=cronometro_2)
        thread_crono_2.start()
        running_threads.append(thread_crono_2)
    
    #Iniciar hilo de lectura modbus para cafe 2
    if modoG_2 == 3:
        if thread_readMod_2 is None or not thread_readMod_2.is_alive():
            thread_readMod_2 = threading.Thread(target=theread_read_cafe_2)
            thread_readMod_2.start()
            running_threads.append(thread_readMod_2) 
    else:
        pass

def cycleTest_stop_cafe_2():
    global thread_modbus_2, client_2, modoG_2, nodo_2, running_threads, flag_2, flag_c_2, thread_crono_2, minutos_cafe_2, segundos_cafe_2,\
           thread_readMod_2, flag_read_2

    if thread_modbus_2 is not None and thread_modbus_2.is_alive():
        flag_2.set()
        thread_modbus_2.join()
        flag_2.clear()

    if thread_crono_2 is not None and thread_crono_2.is_alive():
        flag_c_2.set()
        thread_crono_2.join()
        flag_c_2.clear()
        minutos_cafe_2 = 0
        segundos_cafe_2 = 0

    #Detener hilo de lectura modbus para cafe 2
    if modoG_2 == 3:
        if thread_readMod_2 is not None and thread_readMod_2.is_alive():
            flag_read_2.set()
            thread_readMod_2.join()
            flag_read_2.clear()
    else:
        pass

def cycleTest_write_start_2():
    global client_2, nodo_2, modoG_2, flag_2, inputType_modulation_2, modulation_read_2, modulation_write_2, setPoint_modulation_2, port_gpio_2,\
    listaP, pausa_hilo_2, permiso_read_2

    setPoint_modulation_2 = 0
    widthTimePulse_show = int(listaP[22][0])
    signalType = listaP[21]

    if modoG_2 == 1:
        print("open_digital_cafe_1")
    
    elif modoG_2 == 2:
        if signalType == 'pulseSignal':             #Signal Type PULSE SIGNAL settings default----------------------------------------
            if inputType_modulation_2 == '0-10v':
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    modulation_write_2.raw_value = alto_Mod_0_10 
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_0_10
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_2 == '2-10v':
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    modulation_write_2.raw_value = alto_Mod_2_10 
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_2_10 
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_2 == '0-20mA':
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    modulation_write_2.raw_value = alto_Mod_0_20 
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_0_20 
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)
            elif inputType_modulation_2 == '4-20mA':
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    modulation_write_2.raw_value = alto_Mod_4_20 
                    setPoint_modulation_2 = 100
                    time.sleep(widthTimePulse_show)

                    modulation_write_2.raw_value = bajo_Mod_4_20 
                    setPoint_modulation_2 = 0
                    time.sleep(widthTimePulse_show)

        elif signalType == 'sawSignal':             #Signal Type SAW SIGNAL settings default--------------------------------------------
            if inputType_modulation_2 == '0-10v':
                i = 0
                porcent_step = saw_porcent   #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_10,alto_Mod_0_10)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_2 == '2-10v':
                i = 0
                porcent_step = saw_porcent    #Porcentaje de sierra
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)                    
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_2_10,alto_Mod_2_10 )
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_2 == '0-20mA':
                i = 0
                porcent_step = saw_porcent       #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_0_20,alto_Mod_0_20)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

            elif inputType_modulation_2 == '4-20mA':
                i = 0
                porcent_step = saw_porcent      #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
                    item = final_array[i]
                    fpos = map(item,0,100,bajo_Mod_4_20,alto_Mod_4_20)
                    modulation_write_2.raw_value = int(fpos)
                    setPoint_modulation_2 = int(item)
                    i = i + 1
                    if i == len(final_array):
                        i = 0
                    time.sleep(width_time_saw)

        elif signalType == 'scaleSignal':           #Signal Type SCALE SIGNAL settings default--------------------------------------------
            if inputType_modulation_2 == '0-10v':
                i = 0
                porcent_step = scale_porcent                   #Porcentaje de escalon
                wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)
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
                wtp_show = widthTimePulse_show
                array_1 = np.arange(0,101,porcent_step)
                array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
                final_array = np.concatenate((array_1, array_2))
                while not flag_2.is_set():
                    while pausa_hilo_2 == True:
                        time.sleep(0.1)                    
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
                while pausa_hilo_2 == True:
                    time.sleep(0.1)
                result2 = client_2.write_register(2, 100, nodo_2)
                setPoint_modulation_2 = 100
                time.sleep(widthTimePulse_show)

                result2 = client_2.write_register(2, 0, nodo_2)
                setPoint_modulation_2 = 0
                time.sleep(widthTimePulse_show)

        
        elif signalType == 'sawSignal':
            i = 0
            porcent_step = saw_porcent
            wtp_show = (widthTimePulse_show*1000)/(100/porcent_step)
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_2.is_set():
                while pausa_hilo_2 == True:
                    time.sleep(0.1)
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
            wtp_show = widthTimePulse_show
            array_1 = np.arange(0,101,porcent_step)
            array_2 = np.arange(100, -1, -1*porcent_step)[1:-1]
            final_array = np.concatenate((array_1, array_2))
            while not flag_2.is_set():
                while pausa_hilo_2 == True:
                    time.sleep(0.1)
                item = final_array[i]
                fpos = int(item)
                setPoint_modulation_2 = int(item)
                result2 = client_2.write_register(2,fpos, nodo_2)
                i = i + 1
                if i == len(final_array):
                    i = 0
                time.sleep(wtp_show)

def cycleTest_read_cafe_2():
    global client_2, nodo_2, modoG_2, modulation_read_2, inputType_modulation_2, setPoint_modulation_2, listaP, counter_open_cafe_2,\
    counter_close_cafe_2, minutos_cafe_2, segundos_cafe_2, posMod_2

    signalType_2 = listaP[14]
    #-----------------------------------------Al encender CAFE------------------------------------
    position = 0
    setPoint = 0
    if modoG_2 == 1:
        print("leyendo digital")
    
    elif modoG_2 == 2:
        if inputType_modulation_2 == '0-10v':   
            position = modulation_read_2.voltage*3.342*2
            position = int(map(position, 0,10,0,100))
            setPoint = setPoint_modulation_2
        elif inputType_modulation_2 == '2-10v':   
            position = modulation_read_2.voltage*3.342*2
            position = int(map(position, 2,10,0,100))
            setPoint = setPoint_modulation_2
        elif inputType_modulation_2 == '0-20mA':   
            position = modulation_read_2.voltage*3.342*2
            position = int(map(position, 0,20,0,100))
            setPoint = setPoint_modulation_2
        elif inputType_modulation_2 == '4-20mA':   
            position = modulation_read_2.voltage*3.342*2
            position = int(map(position, 4,20,0,100))
            setPoint = setPoint_modulation_2

    elif modoG_2 == 3:
        #result = client_2.read_holding_registers(0,3,nodo_2)
        # try:
        #     position = result.registers[1]
        # except:
        #     position = setPoint_modulation_2

        #position = result.registers[1]
        position = posMod_2
        setPoint = setPoint_modulation_2

    try:
        relay_O = int(not gpio.input(24))*50
        relay_C = int(not gpio.input(25))*50
    except:
        relay_O = random.randint(0,100)
        relay_C = random.randint(0,100)

    relay_analysis_2(relay_O, relay_C)

    return setPoint, position, signalType_2, relay_O, relay_C, counter_open_cafe_2, counter_close_cafe_2, minutos_cafe_2, segundos_cafe_2

def theread_read_cafe_2():
    global client_2, nodo_2, flag_read_2, posMod_2, setPoint_modulation_2, permiso_read_2, posAnt_modBus_2
    falla = 0
    while not flag_read_2.is_set():
        if falla < 3:
            try:
                result = client_2.read_holding_registers(0,3,nodo_2)
                posMod_2 = result.registers[1]
                posAnt_modBus_2 = posMod_2
            except:
                falla = falla + 1
        else:
            falla = 0
            posMod_2 = posAnt_modBus_2
        time.sleep(0.01)    

def cycleTest_pause_cafe_2():
    global pausa_hilo_2
    pausa_hilo_2 = True

def cycleTest_resume_cafe_2():
    global pausa_hilo_2
    pausa_hilo_2 = False

def relay_analysis_2(signal_relayA, signal_relayB):
    global posAnteriorA_2, posAnteriorB_2, counter_open_cafe_2, counter_close_cafe_2

    if signal_relayA == 50 and posAnteriorA_2 == 0:
        counter_open_cafe_2 = counter_open_cafe_2 + 1

    if signal_relayB == 50 and posAnteriorB_2 == 0:
        counter_close_cafe_2 = counter_close_cafe_2 + 1

    posAnteriorA_2 = signal_relayA
    posAnteriorB_2 = signal_relayB

def cronometro_2():
    global minutos_cafe_2, segundos_cafe_2
    tiempo_inicio = time.time()
    while not flag_c_2.is_set():
        tiempo_transcurrido = time.time() - tiempo_inicio
        minutos_cafe_2, segundos_cafe_2 = divmod(int(tiempo_transcurrido), 60)
        time.sleep(1)

def turnOn_cafe_2():
    global client_2, nodo_2, modoG_2, inputType_modulation_2, modulation_write_2, setPoint_modulation_2, tiempoEncendidoCafe_a

    #gpio.output(#, gpio.HIGH)  #GPIO Activar GPIO para encender puerto ALONE
    opVoltage = globals()['op_voltage_2']

    if opVoltage == '24vdc':
        print("Rele 24vdc cafe 2")
    else:
        print("120/240 vdc cafe 2")
    
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
    global client_2, nodo_2, modoG_2, inputType_modulation_2, modulation_write_2, setPoint_modulation_2, tiempoApagadoCafe_2
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
        print("apagar cafe 2 modbus")

    time.sleep(tiempoApagadoCafe_2)

    cycleTest_stop_cafe_2()
    if (client_2 != None):
        client_2.close()
#-----------FIN Funciones CYCLE TEST---------#
def map(valor, desde_min, desde_max, a_min, a_max):
    # Asegurarse de que el valor esté dentro del rango original
    valor = max(desde_min, min(valor, desde_max))
    
    # Calcular el mapeo
    return (valor - desde_min) * (a_max - a_min) / (desde_max - desde_min) + a_min

def turn_off_all():
    print("apagar todo")

def stop():
    global client,client_1, client_2, cant_duts, port_gpio_alone, name_dut_1, name_dut_2, dut_alone, modo_dut_1, modo_dut_2, modo_dut_alone

    #si hay 1 DUT
    if cant_duts == 1:
        if dut_alone == 'CAFE':
            cycleTest_stop_cafe_alone()
            if (client != None):
                client.close()
            turnOff_cafe_alone()
            stop_saveInDB_a()
        """
        elif dut_alone == 'COIL':
            show_stop_coil_alone()
            show_close_coil_alone()
        elif dut_alone == 'LIMIT SWITCH':
            turnOn_ls_alone()
        """

    elif cant_duts == 2:
        #-------------STOP DUT #1-------------#
        if name_dut_1 == 'CAFE':
            cycleTest_stop_cafe_1()
            if (client_1 != None):
                client_1.close()
            turnOff_cafe_1()
        """    
        elif name_dut_1 == 'COIL':
            show_stop_coil_1()
            show_close_coil_1()
        elif name_dut_1 == 'LIMIT SWITCH':
            turnOff_ls_1()
        """

        #-------------STOP DUT #2-------------#
        if name_dut_2 == 'CAFE':
            cycleTest_stop_cafe_2()
            if (client_2 != None):
                client_2.close()
            turnOff_cafe_2()
        """
        elif name_dut_2 == 'COIL':
            show_stop_coil_2()
            show_close_coil_2()
        elif name_dut_2 == 'LIMIT SWITCH':
            turnOff_ls_2()
        """
    #Terminar todos los clientes ModBus



    #Apagar los dos puertos
    #gpio.output(#, gpio.LOW)  #GPIO Desactivar GPIO para apagar puerto ALONE
    print("PARAR TODOS LOS HILOS")

def start_saveInDB_a():
    global thread_saveDB_a, running_threads

    if thread_saveDB_a is None or not thread_saveDB_a.is_alive():
        thread_saveDB_a = threading.Thread(target=saveInDB_a)
        thread_saveDB_a.start()
        running_threads.append(thread_saveDB_a) 

def stop_saveInDB_a():
    global thread_saveDB_a, flag_thread_saveDB_a

    #Detenr hilo que guarda en base de datos
    if thread_saveDB_a is not None and thread_saveDB_a.is_alive():
        flag_thread_saveDB_a.set()
        thread_saveDB_a.join()
        flag_thread_saveDB_a.clear()

def saveInDB_a():
    global temp_a, current_a, setPoint_a, feedback_a, relayFeO_a, relayFeC_a, timeStamp_a, indexDB_a, flag_thread_saveDB_a
    
    tDataCt_a.objects.all().delete
    
    while not flag_thread_saveDB_a.is_set():
        #Estan los vectores llenos?
        if indexDB_a < 1000:
            #Asignar nuevos valores de lectura a los vectores
            setPoint_a[indexDB_a] = setPoint_modulation_a
            feedback_a[indexDB_a] = position_a
            relayFeO_a[indexDB_a] = relayO_a
            relayFeC_a[indexDB_a] = relayC_a
            temp_a[indexDB_a] = 0
            current_a[indexDB_a] = 0
            timeStamp_a[indexDB_a] = tiempo_total_a
            
            #incrementar el contador general
            indexDB_a = indexDB_a + 1
        #Ya se llenaron los vectores
        else:
            #Converitr listas a json
            jsonTempA = json.dumps(temp_a)
            jsonBytes_TempA = jsonTempA.encode('utf-8')
            
            jsonCurrentA = json.dumps(current_a)
            jsonBytes_CurrentA = jsonCurrentA.encode('utf-8')
            
            jsonSetPointA = json.dumps(setPoint_a)
            jsonBytes_SetPointA = jsonSetPointA.encode('utf-8')
            
            jsonFeedbackA = json.dumps(feedback_a)
            jsonBytes_FeedbackA = jsonFeedbackA.encode('utf-8')
            
            jsonRelaysFeOA = json.dumps(relayFeO_a)
            jsonBytes_RelaysFeOA = jsonRelaysFeOA.encode('utf-8')
            
            jsonRelaysFeCA = json.dumps(relayFeC_a)
            jsonBytes_RelaysFeCA = jsonRelaysFeCA.encode('utf-8')
            
            jsonTimeStampA = json.dumps(timeStamp_a)
            jsonBytes_TimeStampA = jsonTimeStampA.encode('utf-8')
            
            temp_data = tDataCt_a(      #Instancia de base de datos temporal
                    temp = jsonBytes_TempA,
                    current = jsonBytes_CurrentA,
                    setPoint = jsonBytes_SetPointA,
                    feedback = jsonBytes_FeedbackA,
                    relayO = jsonBytes_RelaysFeOA,
                    relayC = jsonBytes_RelaysFeCA,
                    timeStamp = jsonBytes_TimeStampA
                )
            temp_data.save() #Guardar json en base de datos
            indexDB_a = 0
            print("Van mil datos")

        time.sleep(0.06)

def joinTemporalDB_a():
    registros = tDataCt_a.objects.all() #Conncecion al modelo de DB

    #Creacion de listas para concatenar registros temporales
    temp_conca = []
    current_conca = []
    setPoint_conca = []
    feedBack_conca = []
    relayO_conca = []
    relayC_conca = []
    timeStamp_conca = []

    for registro in registros:
        # Decodificar el BLOB de bytes a string
        tempConca_json = registro.temp.decode('utf-8')
        currentConca_json = registro.current.decode('utf-8')
        setPointConca_json = registro.setPoint.decode('utf-8')
        feedbackConca_json = registro.feedback.decode('utf-8')
        relayOConca_json = registro.relayO.decode('utf-8')
        relayCConca_json = registro.relayC.decode('utf-8')
        timeStampConca_json = registro.timeStamp.decode('utf-8')
        
        # Convertir el string JSON a una lista
        lista_temp = json.loads(tempConca_json)
        lista_current = json.loads(currentConca_json)
        lista_setPoint = json.loads(setPointConca_json)
        lista_feedBack = json.loads(feedbackConca_json)
        lista_relayO = json.loads(relayOConca_json)
        lista_relayC = json.loads(relayCConca_json)
        lista_timeStamp = json.loads(timeStampConca_json)

        # Concatenar las listas
        temp_conca.extend(lista_temp)
        current_conca.extend(lista_current)
        setPoint_conca.extend(lista_setPoint)
        feedBack_conca.extend(lista_feedBack)
        relayO_conca.extend(lista_relayO)
        relayC_conca.extend(lista_relayC)
        timeStamp_conca.extend(lista_timeStamp)

    print("Este es operation mode :", modo_dut_alone)

    newCycleTestRegister(dut_alone, actuatorRef_g, load_g, loadDetails_g, testerName_g,
                         'ninguna observacion', modo_dut_alone, baud, nodo, op_voltage_a, inputType_modulation_a,
                         signalType_a, widthTimePulse_a, 100, 0, '12', '08', '2024', '20240812',
                         dateStart_a, dateEnd_a, '1506', '1500',
                         temp_conca, current_conca, setPoint_conca,
                         feedBack_conca, relayO_conca, relayC_conca,
                         timeStamp_conca, ['100','99'], ['99','88']) 

def saveCtData(testerName_l, actuatorRef_l, load_l, loadDetails_l):
    global testerName_g, actuatorRef_g, load_g, loadDetails_g

    #Traer datos del cycle test desde el front
    testerName_g = testerName_l
    actuatorRef_g = actuatorRef_l
    load_g = load_l == 'on'
    loadDetails_g = loadDetails_l
    
def newCycleTestRegister(_dut, _actuatorRef, _load, _loadDetails, _testerName, _observations,
                         _operationMode, _bauds, _node, _operationVoltage, _inputType, _signalType,
                         _pulseTime, _highValue,
                         _lowValue, _day, _month, _year, _fullDate, _dateStart, _dateEnd,
                         _plannedTimeTest,
                         _finalTimeTest, _temp, _current, _setPoint, _feedBack, _relayO, _relayC,
                         _timeStamp, _relaysCounter, _feedBackCounter):
    
    #Convertir listas a json
    jsonLoadDetailsA = json.dumps(_loadDetails)
    jsonBytes_LoadDetailsA = jsonLoadDetailsA.encode('utf-8')

    jsonTempA = json.dumps(_temp)
    jsonBytes_TempA = jsonTempA.encode('utf-8')
    
    jsonCurrentA = json.dumps(_current)
    jsonBytes_CurrentA = jsonCurrentA.encode('utf-8')
    
    jsonSetPointA = json.dumps(_setPoint)
    jsonBytes_SetPointA = jsonSetPointA.encode('utf-8')
    
    jsonFeedbackA = json.dumps(_feedBack)
    jsonBytes_FeedbackA = jsonFeedbackA.encode('utf-8')
    
    jsonRelaysFeOA = json.dumps(_relayO)
    jsonBytes_RelaysFeOA = jsonRelaysFeOA.encode('utf-8')
    
    jsonRelaysFeCA = json.dumps(_relayC)
    jsonBytes_RelaysFeCA = jsonRelaysFeCA.encode('utf-8')
    
    jsonTimeStampA = json.dumps(_timeStamp)
    jsonBytes_TimeStampA = jsonTimeStampA.encode('utf-8')
    
    jsonRelaysCounterA = json.dumps(_relaysCounter)
    jsonBytes_RelaysCounterA = jsonRelaysCounterA.encode('utf-8')

    jsonFeedBackCounterA = json.dumps(_feedBackCounter)
    jsonBytes_FeedBackCounterA = jsonFeedBackCounterA.encode('utf-8')

    #Pasar de tabla temporal a tabla final
    temp_data = ctd(    #Instancia de base de datos final
        dut = _dut,
        actuatorRef = _actuatorRef,
        load = _load,
        loadDetails = jsonBytes_LoadDetailsA,
        testerName = _testerName,
        observations = _observations,
        operationMode = _operationMode,
        bauds = _bauds,
        node = _node,
        operationVoltage = _operationVoltage,
        inputType = _inputType,
        signalType = _signalType,
        pulseTime = _pulseTime,
        highValue = _highValue,
        lowValue = _lowValue,
        day = _day,
        month = _month,
        year = _year,
        fullDate = _fullDate,
        dateStart = _dateStart,
        dateEnd = _dateEnd,
        plannedTimeTest = _plannedTimeTest,
        finalTimeTest = _finalTimeTest,
        temp = jsonBytes_TempA,
        current = jsonBytes_CurrentA,
        setPoint = jsonBytes_SetPointA,
        feedBack = jsonBytes_FeedbackA,
        relayO = jsonBytes_RelaysFeOA,
        relayC = jsonBytes_RelaysFeCA,
        timeStamp = jsonBytes_TimeStampA,
        relaysCounter = jsonBytes_RelaysCounterA,
        feedBackCounter = jsonBytes_FeedBackCounterA
        )
    temp_data.save() #Guardar json en base de datos
