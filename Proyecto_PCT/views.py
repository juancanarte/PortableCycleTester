#test 7
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template import Template, Context
from django.urls import reverse
from Proyecto_PCT.Funciones.show import funciones_show
from Proyecto_PCT.Funciones.dut import funciones_dut
from Proyecto_PCT.Funciones.cycle_test import funciones_cycleTest
import random
import math
import json
import subprocess

from cycle_test.models import defSettings as defSet
#from pymodbus.client import ModbusSerialClient
"""
client = ModbusSerialClient(
        method = 'rtu'
        ,port='COM3'
        ,baudrate=19200
        ,parity = 'N'
        ,timeout=1
  )
client.connect()"""

current_value = 0
enable = False
list_parameters = []
cambio = 0

def inicio(request):
    return render(request, "Proyecto_PCT/templates/inicio.html")

def def_settings(request):
    defSettings = {}
    otra = []
    registro = defSet.objects.get(id=1)

    for field in registro._meta.fields:
        otra.append(getattr(registro, field.name))

    otra.pop(0)
    aDefSet = otra

    if request.method == 'POST':
        opcion_presionada = request.POST.get('defSettings')
        parametros = opcion_presionada.split(',')

        for i in range(0,len(parametros)):
            value = parametros[i].split('|')[0]
            clave = parametros[i].split('|')[1] 
            defSettings[clave] = value
    
        nuevo_registro, creado = defSet.objects.update_or_create(defSettings,id=1)

        url_vista3 = reverse('Def_settings')
        return redirect(url_vista3)

    return render(request, "Proyecto_PCT/templates/settings.html", 
                                                                {'pct_mode':aDefSet[0], 'cafe_1_signal_type':aDefSet[1],
                                                                 'cafe_1_width_time':aDefSet[2], 'coil_1_width_time':aDefSet[3],
                                                                 'ls_1_op_voltage':aDefSet[4], 'cafe_2_signal_type':aDefSet[5],
                                                                 'cafe_2_width_time':aDefSet[6], 'coil_2_width_time':aDefSet[7],
                                                                 'ls_2_op_voltage':aDefSet[8]})

def menu(request):
    return render(request, "Proyecto_PCT/templates/menu.html")

def type_of_test(request):
    registro = defSet.objects.get(id=1)
    pct_mode = (registro.pctMode)

    if request.method == 'POST':
        opcion_presionada = request.POST.get('opcion_tot')
        if opcion_presionada == 'Cycle_test':
            opcion_presionada = 'Cycle test'
        return redirect('Dut', mode=opcion_presionada)
    return render(request, "Proyecto_PCT/templates/type_of_test/type_of_test.html",{'pct_mode':pct_mode})

def black(request):
    if request.method == 'POST':
        opcion_presionada = request.POST.get('opcion_turnOff')
        if opcion_presionada == 'shut_down':
            subprocess.run(["sudo", "shutdown", "-h", "now"])
            print("apagar pct")
        elif opcion_presionada == 'reboot':
            subprocess.run(["sudo", "reboot"])
            print("reiniciar pct")

    return render(request, "Proyecto_PCT/templates/black.html")

def dut(request, mode):
    if request.method == 'POST':
        opcion_presionada = request.POST.get('opcion')

        _data_dut_1, _data_dut_2 = funciones_dut.dut_parametros(opcion_presionada, mode)
        _cant_duts = 2-(opcion_presionada.count('NONE') + opcion_presionada.count('_________'))
        # _data_dut_1 = [sDUT_1, _template_dut_1, name_dut_1]
        # _data_dut_2 = [sDUT_2 ,_template_dut_2, name_dut_2]

        request.session['data_dut_1'] = _data_dut_1
        request.session['data_dut_2'] = _data_dut_2
        request.session['cant_duts'] = _cant_duts

        """if mode == 'Show':
            respuesta = funciones_show.params_only_show(_data_dut_1, _data_dut_2, _cant_duts, mode)
            request.session['set_parameters'] = respuesta
            request.session['mode'] = mode
            url_vista3 = reverse('Show')
        else:"""
        url_vista3 = reverse('Set_parameter', kwargs={'mode': mode})
        return redirect(url_vista3)
    return render(request, "Proyecto_PCT/templates/dut/dut.html",{'mode': mode})

def set_parameter(request, mode):
    global list_parameters, cambio

    _data_dut_1 = request.session.get('data_dut_1')
    _data_dut_2 = request.session.get('data_dut_2')
    _cant_duts = request.session.get('cant_duts')

    _temp_dut_1 = _data_dut_1[1]
    _temp_dut_2 = _data_dut_2[1]
    _name_alone_dut = 'NONE'
    _name_dut_1 = _data_dut_1[2]
    _name_dut_2 = _data_dut_2[2]

    _id_dut = 0
    _temp_alone_dut = "Proyecto_PCT/templates/set_parameters/set_parameters_box/dut_empty.html"

    if _data_dut_1[0] == 1:
        _id_dut = 1
        _temp_alone_dut = _data_dut_1[1]
        _name_alone_dut = _data_dut_1[2]
    elif _data_dut_2[0] == 1:
        _id_dut = 2
        _temp_alone_dut = _data_dut_2[1]
        _name_alone_dut = _data_dut_2[2]

    if request.method == 'POST':
        opcion_presionada = request.POST.get('SetParameters')
        request.session['set_parameters'] = opcion_presionada

        if mode == 'Show':
            nextVista = 'Show'
        elif mode == 'Cycle test':
            nextVista = 'Cycle_test'

        request.session['mode'] = mode
        url = reverse(nextVista)
        return redirect(url)

    return render(request, "Proyecto_PCT/templates/set_parameters/set_parameters.html",
                        {'mode': mode, 'dut1': _name_dut_1, 'dut2': _name_dut_2, 'cant_duts': _cant_duts,
                        'temp_dut_1': _temp_dut_1, 'temp_dut_2': _temp_dut_2, 'id_dut': _id_dut,
                        'temp_alone_dut':_temp_alone_dut, 'name_alone_dut': _name_alone_dut})

@csrf_exempt
def show(request):
    _cant_duts = request.session.get('cant_duts')
    _mode = request.session.get('mode')
    _paramsR = request.session.get('set_parameters')
    _params = funciones_show.extraer_parametros(_paramsR, _mode)

    funciones_show.show_params(_paramsR,_mode)

    #Definir al tiempo del pulso por defecto en cafe a
    _dataDef = funciones_show.config_def_settings()

    
    list_context = {'mode':_mode, 'cant_duts':_cant_duts, 'id_dut':_params[0], 'name_alone_dut':_params[1],
                    'temp_alone_dut':_params[2], 'dut1':_params[3], 'dut2':_params[4], 'temp_dut_1':_params[5],
                    'temp_dut_2':_params[6], 'modo_cafe_a':_params[7], 'opVoltage_cafe_a':_params[8], 
                    'inputSignal_cafe_a':_params[9], 'signalType_cafe_a':_params[11], 'widthTime_cafe_a':_params[12],
                    'opVoltage_coil_a':_params[14], 'widthTime_coil_a':_params[15], 'params_ls_a':_params[16],
                    'modo_cafe_1':_params[17], 'opVoltage_cafe_1':_params[18], 'inputSignal_cafe_1':_params[19],
                    'signalType_cafe_1':_params[21], 'widthTime_cafe_1':_params[22], 'modo_cafe_2':_params[24],
                    'opVoltage_cafe_2':_params[25], 'inputSignal_cafe_2':_params[26], 'signalType_cafe_2':_params[28],
                    'widthTime_cafe_2':_params[29], 'opVoltage_coil_1':_params[31], 'widthTime_cafe_1':_params[32],
                    'opVoltage_coil_2':_params[33], 'widthTime_cafe_2':_params[34], 'params_ls_1':_params[35],
                    'params_ls_2':_params[36], 'def_input_signal_1':_dataDef[1], 'def_widthTime_cafe_1':_dataDef[2],
                    'def_widthTime_coil_1':_dataDef[3], 'def_opVoltage_ls_1':_dataDef[4], 'def_input_signal_2':_dataDef[5],
                    'def_widthTime_cafe_2':_dataDef[6],  'def_widthTime_coil_2':_dataDef[7], 'def_opVoltage_ls_2':_dataDef[8],
                    'def_input_signal_a':_dataDef[9], 'def_widthTime_cafe_a':_dataDef[10], 'def_widthTime_coil_a':_dataDef[11]}
    


    #Extructura respuesta [id_dut, label_dut, temp_dut_alone, label_dut_1, label_dut_2, temp_dut_1, temp_dut_2, modo_dut_1, modo_dut_2, modo_dut_a]
    return render(request, "Proyecto_PCT/templates/show/show.html",list_context)

def turn_off_all(request):
    funciones_show.turn_off_all()
    data = ''
    return JsonResponse({'data': data})

def updateSoftware(request):
    if request.method == 'POST':
        try:
            result = subprocess.run(['/home/pct/Desktop/PCT/update_code.sh'], capture_output=True, text=True)
            if result.returncode == 0:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': result.stderr})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    print("Actualizando software")
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

#Funcioes SHOW para CAFE alone
def show_start_cafe_alone(request):
    funciones_show.show_start_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

def show_stop_cafe_alone(request):
    funciones_show.show_stop_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

@csrf_exempt
def show_open_cafe_alone(request):
    data = ''
    if request.method == 'POST':
        input_data = request.POST.get('porcPos', '')
        print(input_data)
        funciones_show.show_open_cafe_alone(input_data)
    return JsonResponse({'data': data})

def show_close_cafe_alone(request):
    funciones_show.show_close_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

def show_read_cafe_alone(request):
    res1, res2 = funciones_show.show_read_cafe_alone()
    data1 = res1
    data2 = res2
    return JsonResponse({'data1':data1, 'data2':data2})

def turnOn_cafe_alone(request):
    data = ''
    funciones_show.turnOn_cafe_alone()
    return JsonResponse({'data': data})

def turnOff_cafe_alone(request):
    data = ''
    funciones_show.turnOff_cafe_alone()
    return JsonResponse({'data': data})

#Funcioes SHOW para CAFE 1
def show_start_cafe_1(request):
    funciones_show.show_start_cafe_1()
    data = ''
    return JsonResponse({'data': data})

def show_stop_cafe_1(request):
    funciones_show.show_stop_cafe_1()
    data = ''
    return JsonResponse({'data': data})

@csrf_exempt
def show_open_cafe_1(request):
    data = ''
    if request.method == 'POST':
        input_data = request.POST.get('porcPos', '')
        funciones_show.show_open_cafe_1(input_data)
    return JsonResponse({'data': data})

def show_close_cafe_1(request):
    funciones_show.show_close_cafe_1()
    data = ''
    return JsonResponse({'data': data})

def show_read_cafe_1(request):
    res1, res2 = funciones_show.show_read_cafe_1()
    data1 = res1
    data2 = res2
    return JsonResponse({'data1':data1, 'data2':data2})

def turnOn_cafe_1(request):
    data = ''
    funciones_show.turnOn_cafe_1()
    return JsonResponse({'data': data})

def turnOff_cafe_1(request):
    data = ''
    funciones_show.turnOff_cafe_1()
    return JsonResponse({'data': data})

#Funcioes SHOW para CAFE 2
def show_start_cafe_2(request):
    funciones_show.show_start_cafe_2()
    data = ''
    return JsonResponse({'data': data})

def show_stop_cafe_2(request):
    funciones_show.show_stop_cafe_2()
    data = ''
    return JsonResponse({'data': data})

@csrf_exempt
def show_open_cafe_2(request):
    data = ''
    if request.method == 'POST':
        input_data = request.POST.get('porcPos', '')
        funciones_show.show_open_cafe_2(input_data)
    return JsonResponse({'data': data})

def show_close_cafe_2(request):
    funciones_show.show_close_cafe_2()
    data = ''
    return JsonResponse({'data': data})

def show_read_cafe_2(request):
    res1, res2 = funciones_show.show_read_cafe_2()
    data1 = res1
    data2 = res2
    return JsonResponse({'data1':data1, 'data2':data2})

def turnOn_cafe_2(request):
    data = ''
    funciones_show.turnOn_cafe_2()
    return JsonResponse({'data': data})

def turnOff_cafe_2(request):
    data = ''
    funciones_show.turnOff_cafe_2()
    return JsonResponse({'data': data})

#Funciones SHOW para COIL alone
def show_start_coil_alone(request):
    funciones_show.show_start_coil_alone()
    data = ''
    return JsonResponse({'data': data})

def show_stop_coil_alone(request):
    funciones_show.show_stop_coil_alone()
    data = ''
    return JsonResponse({'data': data})

def show_open_coil_alone(request):
    funciones_show.show_open_coil_alone()
    data = ''
    return JsonResponse({'data': data})

def show_close_coil_alone(request):
    funciones_show.show_close_coil_alone()
    data = ''
    return JsonResponse({'data': data})

def show_read_coil_alone(request):
    res1 = funciones_show.show_read_coil_alone()
    data1 = res1
    return JsonResponse({'data1':data1})

#Funciones SHOW para COIL 1
def show_start_coil_1(request):
    funciones_show.show_start_coil_1()
    data = ''
    return JsonResponse({'data': data})

def show_stop_coil_1(request):
    funciones_show.show_stop_coil_1()
    data = ''
    return JsonResponse({'data': data})

def show_open_coil_1(request):
    funciones_show.show_open_coil_1()
    data = ''
    return JsonResponse({'data': data})

def show_close_coil_1(request):
    funciones_show.show_close_coil_1()
    data = ''
    return JsonResponse({'data': data})

def show_read_coil_1(request):
    res1 = funciones_show.show_read_coil_1()
    data1 = res1
    return JsonResponse({'data1':data1})

#Funciones SHOW para COIL 2
def show_start_coil_2(request):
    funciones_show.show_start_coil_2()
    data = ''
    return JsonResponse({'data': data})

def show_stop_coil_2(request):
    funciones_show.show_stop_coil_2()
    data = ''
    return JsonResponse({'data': data})

def show_open_coil_2(request):
    funciones_show.show_open_coil_2()
    data = ''
    return JsonResponse({'data': data})

def show_close_coil_2(request):
    funciones_show.show_close_coil_2()
    data = ''
    return JsonResponse({'data': data})

def show_read_coil_2(request):
    res1 = funciones_show.show_read_coil_2()
    data1 = res1
    return JsonResponse({'data1':data1})

#Funciones SHOW para LIMIT SWITCH Alone
def show_read_ls_alone(request):
    status_G, status_Y, status_R = funciones_show.show_read_ls_alone()
    return JsonResponse({'status_G':status_G, 'status_Y':status_Y, 'status_R':status_R})

def turnOn_ls_alone(request):
    funciones_show.show_read_ls_alone()
    data1 = ''
    return JsonResponse({'data1':data1})

def turnOff_ls_alone(request):
    funciones_show.turnOff_ls_alone()
    data1 = ''
    return JsonResponse({'data1':data1})

#Funciones SHOW para LIMIT SWITCH #1
def turnOn_ls_1(request):
    funciones_show.turnOn_ls_1()
    data1 = ''
    return JsonResponse({'data1':data1})

def turnOff_ls_1(request):
    funciones_show.turnOff_ls_1()
    data1 = ''
    return JsonResponse({'data1':data1})

#Funciones SHOW para LIMIT SWITCH #2
def turnOn_ls_2(request):
    funciones_show.turnOn_ls_2()
    data1 = ''
    return JsonResponse({'data1':data1})

def turnOff_ls_2(request):
    funciones_show.turnOff_ls_2()
    data1 = ''
    return JsonResponse({'data1':data1})



#--------------------- FIN VISTAS------------------#
def stop(request):
    funciones_show.stop()
    data = ''
    return JsonResponse({'data': data})   

def modbus1_params(request):
    return HttpResponse()

def prueba_RPI(request):
    global current_value
    current_value = 0
    print("hola")
    return render(request, "Proyecto_PCT/templates/cycle_test/cycle_test copy.html")

def home(request):
    return render(request, "Proyecto_PCT/templates/prueba.html")

def saludo(request):

    doc_externo = open("E:/simuPCT/PCT_Software/Proyecto_PCT/Proyecto_PCT/plantillas/primera.html")

    plt = Template(doc_externo.read())

    doc_externo.close()

    ctx = Context()

    documento = plt.render(ctx)

    return HttpResponse(documento)

def prueba(request):

    return render(request, "Proyecto_PCT/templates/primera.html")

def control_led(request):
    if request.method == 'POST':
        if 'encender' in request.POST:
            print("encender led")  # Encender el LED
        elif 'apagar' in request.POST:
            print("apagar led")  # Apagar el LED

    led_state = random.randint(1,100)
    context = {'led_state': led_state}
    return render(request, 'Proyecto_PCT/templates/botones.html', context)

def get_sensor_data(request):
    # Simulamos la obtención de datos del sensor
    data = random.randint(0, 100)
    return JsonResponse({'data': data})

"""def gpio1(request):

    # Simulamos la obtención de datos del sensor
    #result = client.read_holding_registers(0,10,1)
    #result2 = client.write_register(3, 10, unit=1)
    #print(result,result2)
    data = 'Se activo el gpio_1'
    return JsonResponse({'data': result.registers})

def gpio2(request):
    result2 = client.write_register(2, 100, 1)
    # Simulamos la obtención de datos del sensor
    data = 'cerrado'
    
    return JsonResponse({'data': data})

def gpio3(request):
    # Simulamos la obtención de datos del sensor
    result2 = client.write_register(2, 0, 1)
    # Simulamos la obtención de datos del sensor
    data = 'cerrado'
    return JsonResponse({'data': data})

def gpio4(request):
    # Simulamos la obtención de datos del sensor
    data = 'Se activo el gpio_4'
    return JsonResponse({'data': data})"""

def send_to_sensor(request):
    global current_value
    # Genera el nuevo valor correspondiente a una función seno
    current_value += 0.1
    values = math.sin(current_value)
    values2 = math.cos(current_value)
    return JsonResponse({'data': values,'data2': values2})
