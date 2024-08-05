import json
from random import randint
from time import sleep
import asyncio
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from Proyecto_PCT.Funciones.show import funciones_show
from cycle_test.Funciones import funciones_cycleTest

#-----------CAFE Alone-----------#
ct_position_cafe_a = 0
ct_setPoint_cafe_a = 0
ct_relays_cafe_a = 0

sh_position_cafe_a = 0
sh_setPoint_cafe_a = 0
#-----------CAFE 1-----------#
ct_position_cafe_1 = 0
ct_setPoint_cafe_1 = 0
ct_relays_cafe_1 = 0

sh_position_cafe_1 = 0
sh_setPoint_cafe_1 = 0
#-----------CAFE 2-----------#
ct_position_cafe_2 = 0
ct_setPoint_cafe_2 = 0
ct_relays_cafe_2 = 0

sh_position_cafe_2 = 0
sh_setPoint_cafe_2 = 0

class sh_read_cafe_a(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True

        self.paused = False
        asyncio.ensure_future(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True


    async def send_sensor_data(self):
        while self.running:
            if not self.paused:
                _pos, _setPos = funciones_show.show_read_cafe_alone()
                await self.send(json.dumps({'pos': _pos,'setPos':_setPos}))
            await asyncio.sleep(0.08)

class sh_read_cafe_1(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True

        self.paused = False
        asyncio.ensure_future(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True


    async def send_sensor_data(self):
        while self.running:
            if not self.paused:
                _pos, _setPos = funciones_show.show_read_cafe_1()
                await self.send(json.dumps({'pos': _pos,'setPos':_setPos}))
            await asyncio.sleep(0.08)

class sh_read_cafe_2(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True

        self.paused = False
        asyncio.ensure_future(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True


    async def send_sensor_data(self):
        while self.running:
            if not self.paused:
                _pos, _setPos = funciones_show.show_read_cafe_2()
                await self.send(json.dumps({'pos': _pos,'setPos':_setPos}))
            await asyncio.sleep(0.08)

class sh_read_lm_a(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True

        self.paused = False
        asyncio.ensure_future(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True


    async def send_sensor_data(self):
        while self.running:
            if not self.paused:
                _state = funciones_show.show_read_ls_alone()
                await self.send(json.dumps({'state':_state}))
            await asyncio.sleep(0.08)

class sh_read_lm_1(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True

        self.paused = False
        asyncio.ensure_future(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True


    async def send_sensor_data(self):
        while self.running:
            if not self.paused:
                _state = funciones_show.show_read_ls_1()
                await self.send(json.dumps({'state':_state}))
            await asyncio.sleep(0.08)

class sh_read_lm_2(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True

        self.paused = False
        asyncio.ensure_future(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True


    async def send_sensor_data(self):
        while self.running:
            if not self.paused:
                _state = funciones_show.show_read_ls_2()
                await self.send(json.dumps({'state':_state}))
            await asyncio.sleep(0.08)

class ct_read_cafe_a(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = False
        self.paused = False  # Agrega esta variable
        
        #await self.send_sensor_data()

    async def disconnect(self, close_code):
        self.paused = True
        self.running = False
        await asyncio.sleep(1)
        print("Desconectado")
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True
            asyncio.ensure_future(self.send_sensor_data())

    async def send_sensor_data(self):
        global ct_position_cafe_a, ct_setPoint_cafe_a, ct_relays_cafe_a
        while self.running:
            if not self.paused:
                _pos, _setPos, _signalType, _relay_O, _relay_C, _relayCountA, _relayCountB, _hor, _min, _sec  = funciones_cycleTest.cycleTest_read_cafe_alone()
                _ct_relays_cafe_a = randint(1,100)

                if (_signalType == 'sawSignal'):
                    if (_pos != ct_position_cafe_a):
                        await self.send(json.dumps({'pos':ct_position_cafe_a, 'setPos':ct_setPoint_cafe_a, 'relay_O':_relay_O, 'relay_C':_relay_C,
                                                    'relayCountA':_relayCountA, 'relayCountB':_relayCountB, 'hor':_hor, "min":_min, "sec":_sec}))
                        ct_position_cafe_a = _pos
                        ct_setPoint_cafe_a = _setPos
                        ct_relays_cafe_a = _ct_relays_cafe_a
                
                else:
                    await self.send(json.dumps({'pos':_pos, 'setPos':_setPos, 'relay_O':_relay_O, 'relay_C':_relay_C, 'relayCountA':_relayCountA,
                                                'relayCountB':_relayCountB, 'hor':_hor, "min":_min, "sec":_sec}))
            await asyncio.sleep(0.08)

class ct_read_cafe_1(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = False
        self.paused = False  # Agrega esta variable

    async def disconnect(self, close_code):
        self.paused = True
        self.running = False
        await asyncio.sleep(1)
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True
            asyncio.ensure_future(self.send_sensor_data())

    async def send_sensor_data(self):
        global ct_position_cafe_1, ct_setPoint_cafe_1, ct_relays_cafe_1
        while self.running:
            if not self.paused:
                _pos, _setPos, _signalType, _relay_O, _relay_C, _relayCountA, _relayCountB, _min, _sec  = funciones_cycleTest.cycleTest_read_cafe_1()
                _ct_relays_cafe_1 = randint(1,100)
                if (_signalType == 'sawSignal'):
                    if (_pos != ct_position_cafe_1):
                        await self.send(json.dumps({'pos':ct_position_cafe_1, 'setPos':ct_setPoint_cafe_1, 'relay_O':_relay_O, 'relay_C':_relay_C,
                                                    'relayCountA':_relayCountA, 'relayCountB':_relayCountB, "min":_min, "sec":_sec}))
                        ct_position_cafe_1 = _pos
                        ct_setPoint_cafe_1 = _setPos
                        ct_relays_cafe_1 = _ct_relays_cafe_1
                
                else:
                    await self.send(json.dumps({'pos':_pos, 'setPos':_setPos, 'relay_O':_relay_O, 'relay_C':_relay_C, 'relayCountA':_relayCountA,
                                                'relayCountB':_relayCountB, "min":_min, "sec":_sec}))
            await asyncio.sleep(0.08)

class ct_read_cafe_2(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = False
        self.paused = False  # Agrega esta variable

    async def disconnect(self, close_code):
        self.paused = True
        self.running = False
        await asyncio.sleep(1)
        raise StopConsumer()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'pause':
            self.paused = True
        elif message == 'resume':
            self.paused = False
        elif message == 'stop':
            self.paused = True
            self.running = False
        elif message == 'start':
            self.paused = False
            self.running = True
            asyncio.ensure_future(self.send_sensor_data())

    async def send_sensor_data(self):
        global ct_position_cafe_2, ct_setPoint_cafe_2, ct_relays_cafe_2
        while self.running:
            if not self.paused:
                _pos, _setPos, _signalType, _relay_O, _relay_C, _relayCountA, _relayCountB, _min, _sec  = funciones_cycleTest.cycleTest_read_cafe_2()
                _ct_relays_cafe_2 = randint(1,100)
                if (_signalType == 'sawSignal'):
                    if (_pos != ct_position_cafe_2):
                        await self.send(json.dumps({'pos':ct_position_cafe_2, 'setPos':ct_setPoint_cafe_2, 'relay_O':_relay_O, 'relay_C':_relay_C,
                                                    'relayCountA':_relayCountA, 'relayCountB':_relayCountB, "min":_min, "sec":_sec}))
                        ct_position_cafe_2 = _pos
                        ct_setPoint_cafe_2 = _setPos
                        ct_relays_cafe_2 = _ct_relays_cafe_2
                
                else:
                    await self.send(json.dumps({'pos':_pos, 'setPos':_setPos, 'relay_O':_relay_O, 'relay_C':_relay_C, 'relayCountA':_relayCountA,
                                                'relayCountB':_relayCountB, "min":_min, "sec":_sec}))
            await asyncio.sleep(0.08)
