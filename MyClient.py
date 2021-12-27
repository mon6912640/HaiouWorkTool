import asyncio
import websockets


async def auth_system(websocket):
    while True:
        cred_text = input('please enter your username and password:')
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        if 'congratulation' in response_str:
            return False


async def send_msg(websocket):
    while True:
        _text = input('please enter your context: ')
        if _text == 'exit':
            print(f'you have enter "exit", goodbye')
            await websocket.close(reason='user exit')
            return False
        await websocket.send(_text)
        recv_text = await websocket.recv()
        print(f'{recv_text}')


async def main_logic():
    async with websockets.connect('ws://192.168.22.23:5678') as websocket:
        await auth_system(websocket)
        await send_msg(websocket)


asyncio.get_event_loop().run_until_complete(main_logic)
