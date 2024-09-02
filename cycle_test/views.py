from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template import Template, Context
from django.urls import reverse
from Proyecto_PCT.Funciones.show import funciones_show
from cycle_test.Funciones import funciones_cycleTest
from cycle_test.models import tempDataCt_a
from cycle_test.models import users
from cycle_test.models import cycleTestData
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import random
import math
import json
import subprocess

def show_start_cafe_alone(request):
    funciones_show.show_start_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

def cycle_test(request):
    _cant_duts = request.session.get('cant_duts')
    _mode = request.session.get('mode')
    _paramsR = request.session.get('set_parameters')
    _cycleTestData = request.session.get('cycleTestData')

    _users = users.objects.all()

    _params = funciones_cycleTest.extraer_parametros(_paramsR, _mode)
    list_context = {'mode':_mode, 'cant_duts':_cant_duts, 'id_dut':_params[0], 'name_alone_dut':_params[1],
                    'temp_alone_dut':_params[2], 'dut1':_params[3], 'dut2':_params[4], 'temp_dut_1':_params[5],
                    'temp_dut_2':_params[6], 'modo_cafe_a':_params[7], 'opVoltage_cafe_a':_params[8], 
                    'inputSignal_cafe_a':_params[9], 'baud_cafe_a':_params[10],'signalType_cafe_a':_params[11], 
                    'widthTime_cafe_a':_params[12], 'node_cafe_a':_params[13],
                    'opVoltage_coil_a':_params[14], 'widthTime_coil_a':_params[15], 'params_ls_a':_params[16],
                    'modo_cafe_1':_params[17], 'opVoltage_cafe_1':_params[18], 'inputSignal_cafe_1':_params[19],
                    'baud_cafe_1':_params[20],
                    'signalType_cafe_1':_params[21], 'widthTime_cafe_1':_params[22],'node_cafe_1':_params[23],
                    'modo_cafe_2':_params[24],
                    'opVoltage_cafe_2':_params[25], 'inputSignal_cafe_2':_params[26], 'baud_cafe_2':_params[27],
                    'signalType_cafe_2':_params[28],
                    'widthTime_cafe_2':_params[29], 'node_cafe_2':_params[30],
                    'opVoltage_coil_1':_params[31], 'widthTime_coil_1':_params[32],
                    'opVoltage_coil_2':_params[33], 'widthTime_coil_2':_params[34], 'params_ls_1':_params[35],
                    'params_ls_2':_params[36], 'users':_users, 'testerName':_cycleTestData[0], 'actuatorRef':_cycleTestData[1],
                    'load':_cycleTestData[2], 'loadDetails':_cycleTestData[3]}
    funciones_cycleTest.show_params(_paramsR,_mode)
    
    if request.method == 'POST':
        print("Hacer algo")

    #Extructura respuesta [id_dut, label_dut, temp_dut_alone, label_dut_1, label_dut_2, temp_dut_1, temp_dut_2, modo_dut_1, modo_dut_2, modo_dut_a]
    return render(request, "Proyecto_PCT/templates/cycle_test/cycle_test.html",list_context)

#Funcioes CYCLE TEST para CAFE alone
def cycleTest_start_cafe_alone(request):
    funciones_cycleTest.cycleTest_start_cafe_alone()
    tempDataCt_a.objects.all().delete()

    data = ''
    return JsonResponse({'data': data})

def cycleTest_stop_cafe_alone(request):
    funciones_cycleTest.cycleTest_stop_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_pause_cafe_alone(request):
    funciones_cycleTest.cycleTest_pause_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_resume_cafe_alone(request):
    funciones_cycleTest.cycleTest_resume_cafe_alone()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_read_cafe_alone(request):
    res1, res2 = funciones_cycleTest.cycleTest_read_cafe_alone()
    data1 = res1
    data2 = res2
    return JsonResponse({'data1':data1, 'data2':data2})

def turnOn_cafe_alone(request):
    data = ''
    funciones_cycleTest.turnOn_cafe_alone()
    return JsonResponse({'data': data})

def turnOff_cafe_alone(request):
    data = ''
    funciones_cycleTest.turnOff_cafe_alone()
    return JsonResponse({'data': data})

def sendData_cafe_alone(request):
    data = funciones_cycleTest.sendData_cafe_alone()

    print(data)
    return JsonResponse({'dateStart_a': data['dateStart_a'], 'dateEnd_a': data['dateEnd_a'], 'counter_open_cafe_a':data['counter_open_cafe_a'],
                         'counter_close_cafe_a':data['counter_close_cafe_a']})

@csrf_exempt
def saveData_cafe_alone(request):
    if request.method == 'POST':
        # Realiza tus validaciones y guarda los datos
        # Si todo está bien
        observations = request.POST.get('observations')
        funciones_cycleTest.joinTemporalDB_a(observations)

        return JsonResponse({'success': True})
        
        # Si hubo un error
        # return JsonResponse({'success': False, 'error': 'Mensaje de error'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
def customTime_cafe_alone(request):
    data = ''
    if request.method == 'POST':
        input_data = request.POST.get('customTime', '')
        funciones_cycleTest.setCustomTime_a(input_data)
    return JsonResponse({'data': data})

def remoteStop_cafe_alone():
    should_execute = True  # Esta condición puede ser más compleja

    # Responder con un JSON que el cliente puede interpretar
    return JsonResponse({'should_execute': should_execute})

def activar_funcion_desde_vista(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mi_grupo",
        {
            'type': 'send_message_to_client',
            'message': 'ejecutar_funcion'
        }
    )
    return HttpResponse("Mensaje enviado a WebSocket")

#Funcioes CYCLE TEST para CAFE 1
def cycleTest_start_cafe_1(request):
    funciones_cycleTest.cycleTest_start_cafe_1()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_stop_cafe_1(request):
    funciones_cycleTest.cycleTest_stop_cafe_1()
    data = ''
    return JsonResponse({'data': data})
  
def cycleTest_pause_cafe_1(request):
    funciones_cycleTest.cycleTest_pause_cafe_1()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_resume_cafe_1(request):
    funciones_cycleTest.cycleTest_resume_cafe_1()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_read_cafe_1(request):
    res1, res2 = funciones_cycleTest.cycleTest_read_cafe_1()
    data1 = res1
    data2 = res2
    return JsonResponse({'data1':data1, 'data2':data2})

def turnOn_cafe_1(request):
    data = ''
    funciones_cycleTest.turnOn_cafe_1()
    return JsonResponse({'data': data})

def turnOff_cafe_1(request):
    data = ''
    funciones_cycleTest.turnOff_cafe_1()
    return JsonResponse({'data': data})

#Funcioes CYCLE TEST para CAFE 2
def cycleTest_start_cafe_2(request):
    funciones_cycleTest.cycleTest_start_cafe_2()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_stop_cafe_2(request):
    funciones_cycleTest.cycleTest_stop_cafe_2()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_pause_cafe_2(request):
    funciones_cycleTest.cycleTest_pause_cafe_2()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_resume_cafe_2(request):
    funciones_cycleTest.cycleTest_resume_cafe_2()
    data = ''
    return JsonResponse({'data': data})

def cycleTest_read_cafe_2(request):
    res1, res2 = funciones_cycleTest.cycleTest_read_cafe_2()
    data1 = res1
    data2 = res2
    return JsonResponse({'data1':data1, 'data2':data2})

def turnOn_cafe_2(request):
    data = ''
    funciones_cycleTest.turnOn_cafe_2()
    return JsonResponse({'data': data})

def turnOff_cafe_2(request):
    data = ''
    funciones_cycleTest.turnOff_cafe_2()
    return JsonResponse({'data': data})
#-----------------FIN funciones cycle test-----------------#

def stop(request):
    funciones_cycleTest.stop()
    data = ''
    return JsonResponse({'data': data})   
