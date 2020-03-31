# coding:utf-8
import hmac
import asyncio
import websockets
from google.protobuf import reflection
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
from removed import dhs_pb2


class DHSMgr:
    _msgType = {'notify': b'\x01', 'req': b'\x02', 'res': b'\x03'}
    def __init__(self):
        self._url = "wss://mj-srv-3.majsoul.com:4021"
        self._msgPool = {} # msgIndex:(resType, callback func)
        self._msgIndex = 0
        self._msgQueue = []
        self._addrBook = dhs_pb2
        self._wrapper = self._addrBook.Wrapper()
        self._serviceRoot = 'CustomizedContestManagerApi'
        self._ws = None
    @staticmethod
    def _hash(passwd : str) -> bytearray:
        return hmac.new(b'lailai', bytearray(passwd.encode('utf-8')), 'sha256').hexdigest()

    async def login(self,user, passwd):
        data = {
            'account': user,
            'password': self.__class__._hash(passwd),
            'gen_access_token': True,
            'type': 0
        }
        await self.send("loginContestManager", print, data)

    async def run(self):
        async def on_message(msg):
            if msg[0] == ord(self.__class__._msgType['notify']):
                wrapper = self._addrBook.Wrapper()
                wrapper.ParseFromString(msg[1:])
                notification = reflection.MakeClass(self._addrBook.DESCRIPTOR.message_types_by_name[wrapper.name[4:]])()
                notification.ParseFromString(wrapper.data)
                if wrapper.name[4:] in self._msgPool.keys():
                    for index in self._msgPool[wrapper.name[4:]]:
                        if index != -1:
                            cb = self._msgPool[wrapper.name[4:]][index]
                            if asyncio.iscoroutinefunction(cb):
                                await cb(protobuf_to_dict(notification))
                            else:
                                cb(protobuf_to_dict(notification))
            elif msg[0] == ord(self.__class__._msgType['res']):
                # get index
                index = msg[1] + msg[2] * 256
                if index in self._msgPool.keys():
                    # callback
                    self._wrapper.ParseFromString(msg[3:])
                    res = self._msgPool[index][0]()
                    res.ParseFromString(self._wrapper.data)
                    if self._msgPool[index][1] is not None:
                        if asyncio.iscoroutinefunction(self._msgPool[index][1]):
                            await self._msgPool[index][1](protobuf_to_dict(res))
                        else:
                            self._msgPool[index][1](protobuf_to_dict(res))
                    self._msgPool.pop(index)
        async with websockets.connect(self._url) as ws:
            self._ws = ws
            while True:
                await on_message(await ws.recv())

    async def send(self, path, callback, msg = None):
        try:
            while self._ws is None:
                await asyncio.sleep(1)
            self._msgIndex %= 60007
            method = self._addrBook.DESCRIPTOR.services_by_name[self._serviceRoot].methods_by_name[path]
        except KeyError:
            print('API not exist')
            return
        obj = reflection.MakeClass(method.input_type)()
        self._msgPool[self._msgIndex] = (reflection.MakeClass(method.output_type), callback)
        if msg is not None:
            dict_to_protobuf(obj, msg)
        self._wrapper.name = bytes('.' + method.full_name, 'utf-8')
        self._wrapper.data = obj.SerializeToString()
        req = self.__class__._msgType['req'] + bytes([self._msgIndex % 256, self._msgIndex // 256]) + self._wrapper.SerializeToString()
        self._msgIndex += 1
        await self._ws.send(req)

    def bind(self, path : str, callback) -> int:
        if path in self._msgPool.keys():
            index = self._msgPool[path][-1] + 1
            self._msgPool[path][-1] += 1
            self._msgPool[path][index] = callback
            return index
        else:
            self._msgPool[path] = {-1:1}
            self._msgPool[path][0] = callback
            return 0

    def unbind(self, path: str, index) -> bool:
        if index == -1:
            return False
        if path not in self._msgPool.keys():
            return False
        if index not in self._msgPool[path].keys():
            return True
        self._msgPool[path].pop(index)
        return True



