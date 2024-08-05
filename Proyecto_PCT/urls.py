"""
URL configuration for Proyecto_PCT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples: 
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from Proyecto_PCT import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('main/', views.menu, name='Menu'),
    path('type_of_test/', views.type_of_test, name='Type_of_test'),
    path('==<str:mode>/', views.dut, name='Dut'),
    path('<str:mode>/set_parameters/', views.set_parameter, name='Set_parameter'),
    #path('cycle_test/', views.cycle_test, name='Cycle_test'),
    path('test_test/', views.prueba_RPI, name='Test_test'),
    path('show/', views.show, name='Show'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('prueba/', views.prueba, name = "prueba"),
    path('control/', views.control_led, name='control_led'),
    path('get_sensor_data/', views.get_sensor_data, name='get_sensor_data'),
    path('def_settings/', views.def_settings, name='Def_settings'),
    path('black/', views.black, name='Black'),
    path('turn_off_all/', views.turn_off_all, name='Turn_off_all'),
    #----------------------------------------URL's SHOW----------------------------------------#
    #Funciones SHOW para CAFE alone
    path('show_start_cafe_alone/', views.show_start_cafe_alone, name='Show_start_cafe_alone'),
    path('show_stop_cafe_alone/', views.show_stop_cafe_alone, name='Show_stop_cafe_alone'),
    path('show_open_cafe_alone/', views.show_open_cafe_alone, name='Show_open_cafe_alone'),
    path('show_close_cafe_alone/', views.show_close_cafe_alone, name='Show_close_cafe_alone'),
    path('show_read_cafe_alone/', views.show_read_cafe_alone, name='Show_read_cafe_alone'),
    path('turnOn_cafe_alone/', views.turnOn_cafe_alone, name='TurnOn_cafe_alone'),
    path('turnOff_cafe_alone/', views.turnOff_cafe_alone, name='TurnOff_cafe_alone'),
    #Funciones SHOW para CAFE 1
    path('show_start_cafe_1/', views.show_start_cafe_1, name='Show_start_cafe_1'),
    path('show_stop_cafe_1/', views.show_stop_cafe_1, name='Show_stop_cafe_1'),
    path('show_open_cafe_1/', views.show_open_cafe_1, name='Show_open_cafe_1'),
    path('show_close_cafe_1/', views.show_close_cafe_1, name='Show_close_cafe_1'),
    path('show_read_cafe_1/', views.show_read_cafe_1, name='Show_read_cafe_1'),
    path('turnOn_cafe_1/', views.turnOn_cafe_1, name='TurnOn_cafe_1'),
    path('turnOff_cafe_1/', views.turnOff_cafe_1, name='TurnOff_cafe_1'),
    #Funciones SHOW para CAFE 2
    path('show_start_cafe_2/', views.show_start_cafe_2, name='Show_start_cafe_2'),
    path('show_stop_cafe_2/', views.show_stop_cafe_2, name='Show_stop_cafe_2'),
    path('show_open_cafe_2/', views.show_open_cafe_2, name='Show_open_cafe_2'),
    path('show_close_cafe_2/', views.show_close_cafe_2, name='Show_close_cafe_2'),
    path('show_read_cafe_2/', views.show_read_cafe_2, name='Show_read_cafe_2'),
    path('turnOn_cafe_2/', views.turnOn_cafe_2, name='TurnOn_cafe_2'),
    path('turnOff_cafe_2/', views.turnOff_cafe_2, name='TurnOff_cafe_2'),
    #Funciones SHOW para COIL alone
    path('show_start_coil_alone/', views.show_start_coil_alone, name='Show_start_coil_alone'),
    path('show_stop_coil_alone/', views.show_stop_coil_alone, name='Show_stop_coil_alone'),
    path('show_open_coil_alone/', views.show_open_coil_alone, name='Show_open_coil_alone'),
    path('show_close_coil_alone/', views.show_close_coil_alone, name='Show_close_coil_alone'),
    path('show_read_coil_alone/', views.show_read_coil_alone, name='Show_read_coil_alone'),
    #Funciones SHOW para COIL 1
    path('show_start_coil_1/', views.show_start_coil_1, name='Show_start_coil_1'),
    path('show_stop_coil_1/', views.show_stop_coil_1, name='Show_stop_coil_1'),
    path('show_open_coil_1/', views.show_open_coil_1, name='Show_open_coil_1'),
    path('show_close_coil_1/', views.show_close_coil_1, name='Show_close_coil_1'),
    path('show_read_coil_1/', views.show_read_coil_1, name='Show_read_coil_1'),
    #Funciones SHOW para COIL 2
    path('show_start_coil_2/', views.show_start_coil_2, name='Show_start_coil_2'),
    path('show_stop_coil_2/', views.show_stop_coil_2, name='Show_stop_coil_2'),
    path('show_open_coil_2/', views.show_open_coil_2, name='Show_open_coil_2'),
    path('show_close_coil_2/', views.show_close_coil_2, name='Show_close_coil_2'),
    path('show_read_coil_2/', views.show_read_coil_2, name='Show_read_coil_2'),
    #Funciones SHOW para LIMIT SWITCH Alone
    path('show_read_ls_alone/', views.show_read_ls_alone, name='Show_read_ls_alone'),
    path('turnOn_ls_alone/', views.turnOn_ls_alone, name='TurnOn_ls_alone'),
    path('turnOff_ls_alone/', views.turnOff_ls_alone, name='TurnOff_ls_alone'),
    #Funciones SHOW para LIMIT SWITCH 1
    path('turnOn_ls_1/', views.turnOn_ls_1, name='TurnOn_ls_1'),
    path('turnOff_ls_1/', views.turnOff_ls_1, name='TurnOff_ls_1'),
    #Funciones SHOW para LIMIT SWITCH 2
    path('turnOn_ls_2/', views.turnOn_ls_2, name='TurnOn_ls_2'),
    path('turnOff_ls_2/', views.turnOff_ls_2, name='TurnOff_ls_2'),
    #----------------------------------------URL's CYCLE TEST----------------------------------------#
    #Funciones CYCLE TEST para CAFE alone
    path('ct/', include('cycle_test.urls')),
    #path('gpio1/', views.gpio1, name='Gpio1'),
    #path('gpio2/', views.gpio2, name='Gpio2'),
    #path('gpio3/', views.gpio3, name='Gpio3'),
    #path('gpio4/', views.gpio4, name='Gpio4'),
    path('stop/', views.stop, name='Stop'),
    path('send_to_sensor/', views.send_to_sensor, name='send_to_sensor'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
