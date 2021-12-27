import asyncio
import websockets


async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(':')
        if cred_dict[0] == 'admin' and cred_dict[1] == '123456':
            response_str = 'congratulation, you have connect with server\r\nnow, you can do something else'
            await websocket.send(response_str)
            return True
        else:
            response_str = 'sorry, the username or password is wrong, please submit again'
            await websocket.send(response_str)


async def recv_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        response_text = f'your submit context: {recv_text}'
        await websocket.send(response_text)


async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)


start_server = websockets.serve(main_logic, '192.168.22.23', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
