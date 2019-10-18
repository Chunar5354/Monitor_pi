# 测试websocket数据总览

import asyncio
import websockets
import json

async def hello():
    uri = "ws://39.100.5.176:30104"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")
        j_name = {"customer_name":"",
                "serial_number":"406",
                "parameter":['voltage_AB', 'voltage_BC', 'voltage_CA',
                                'current_A', 'current_B', 'current_C',
                                'temp_fore_winding_A', 'temp_fore_winding_B', 'temp_fore_winding_C',
                                'temp_fore_bearing', 'temp_rear_bearing',
                                'temp_water', 'temp_controller_env',
                                'rev', 'temp_rotator'],
                "limit":"1", 
                "start":"",
                "end":""}

        name = json.dumps(j_name)

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())