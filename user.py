from caproto.server import pvproperty, PVGroup
from caproto import ChannelType

class UserPVs(PVGroup):
    name = pvproperty(
            read_only = True,
            dtype = ChannelType.STRING)
    say_hello = pvproperty(
            dtype = ChannelType.INT)
    use_machine = pvproperty(
            dtype = ChannelType.INT)

    def __init__(self, prefix, id, user, ioc):
        super().__init__(f'{prefix}user:{id}:')
        self.id = id
        self.uses = None
        self.ioc = ioc
        self.user = user

    @name.startup
    async def name(self, instance, value):
        await self.name.write(self.user.name)

    @say_hello.putter
    async def say_hello(self, instance, value):
        print(f"hi, I'm {self.user.name}")

    @use_machine.putter
    async def use_machine(self, instance, value):
        self.ioc.messages.put(
                {'cmd': 'use_machine', 
                    'user': self.user.id,
                    'machine': value})


class User:
    def __init__(self, prefix, id, name, ioc):
        self.id = id
        self.name = name
        self.pvs = UserPVs(prefix, id, self, ioc=ioc)

