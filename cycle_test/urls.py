from django.contrib import admin
from django.urls import path
from cycle_test import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cycle_test/', views.cycle_test, name='Cycle_test'),
    #Funciones Cycle Test CAFE Alone
    #path('show_start_cafe_alone/', views.show_start_cafe_alone, name='sw_new'),
    path('cycleTest_start_cafe_alone/', views.cycleTest_start_cafe_alone, name='CycleTest_start_cafe_alone'),
    path('cycleTest_stop_cafe_alone/', views.cycleTest_stop_cafe_alone, name='CycleTest_stop_cafe_alone'),
    path('cycleTest_pause_cafe_alone/', views.cycleTest_pause_cafe_alone, name='CycleTest_pause_cafe_alone'),
    path('cycleTest_resume_cafe_alone/', views.cycleTest_resume_cafe_alone, name='CycleTest_resume_cafe_alone'),
    path('cycleTest_read_cafe_alone/', views.cycleTest_read_cafe_alone, name='CycleTest_read_cafe_alone'),
    path('cycleTest_turnOn_cafe_alone/', views.turnOn_cafe_alone, name='TurnOn_cafe_alone'),
    path('cycleTest_turnOff_cafe_alone/', views.turnOff_cafe_alone, name='TurnOff_cafe_alone'),
    path('cycleTest_sendData_alone/', views.sendData_cafe_alone, name='SendData_cafe_alone'),
    path('cycleTest_saveData_alone/', views.saveData_cafe_alone, name='SaveData_cafe_alone'),
    path('cycleTest_customTime_alone/', views.customTime_cafe_alone, name='CustomTime_cafe_alone'),
    #Funciones Cycle Test CAFE #1
    path('cycleTest_start_cafe_1/', views.cycleTest_start_cafe_1, name='CycleTest_start_cafe_1'),
    path('cycleTest_stop_cafe_1/', views.cycleTest_stop_cafe_1, name='CycleTest_stop_cafe_1'),
    path('cycleTest_pause_cafe_1/', views.cycleTest_pause_cafe_1, name='CycleTest_pause_cafe_1'),
    path('cycleTest_resume_cafe_1/', views.cycleTest_resume_cafe_1, name='CycleTest_resume_cafe_1'),
    path('cycleTest_read_cafe_1/', views.cycleTest_read_cafe_1, name='CycleTest_read_cafe_1'),
    path('cycleTest_turnOn_cafe_1/', views.turnOn_cafe_1, name='TurnOn_cafe_1'),
    path('cycleTest_turnOff_cafe_1/', views.turnOff_cafe_1, name='TurnOff_cafe_1'),
    path('cycleTest_sendData_1/', views.sendData_cafe_1, name='SendData_cafe_1'),
    path('cycleTest_saveData_1/', views.saveData_cafe_1, name='SaveData_cafe_1'),
    path('cycleTest_customTime_1/', views.customTime_cafe_1, name='CustomTime_cafe_1'),
    #Funciones Cycle Test CAFE #2
    path('cycleTest_start_cafe_2/', views.cycleTest_start_cafe_2, name='CycleTest_start_cafe_2'),
    path('cycleTest_stop_cafe_2/', views.cycleTest_stop_cafe_2, name='CycleTest_stop_cafe_2'),
    path('cycleTest_pause_cafe_2/', views.cycleTest_pause_cafe_2, name='CycleTest_pause_cafe_2'),
    path('cycleTest_resume_cafe_2/', views.cycleTest_resume_cafe_2, name='CycleTest_resume_cafe_2'),
    path('cycleTest_read_cafe_2/', views.cycleTest_read_cafe_2, name='CycleTest_read_cafe_2'),
    path('cycleTest_turnOn_cafe_2/', views.turnOn_cafe_2, name='TurnOn_cafe_2'),
    path('cycleTest_turnOff_cafe_2/', views.turnOff_cafe_2, name='TurnOff_cafe_2'),
    #FIN funciones Cycle Test
    path('stop/', views.stop, name='Stop'),
]