from caproto.server import pvproperty, PVGroup
from caproto import ChannelType

import curio

class MachinePVs(PVGroup):
    name = pvproperty(
            read_only = True,
            dtype = ChannelType.STRING)
    startup = pvproperty(
            dtype = ChannelType.INT)
    used_by = pvproperty(
            dtype = ChannelType.INT)

    def __init__(self, prefix, id, machine):
        super().__init__(f'{prefix}machine:{id}:')
        self.id = id
        self.machine = machine

    @name.startup
    async def name(self, instance, value):
        await self.name.write(self.machine.name)

    @startup.putter
    async def startup(self, instance, value):
        print(f'{self.name.value} is starting up')

    @used_by.startup
    async def used_by(self, instance, value):
        return self.machine.used_by

    #async def update(self, instance):
    #    await self.used_by.write(value = self.machine.used_by)

class Machine:
    def __init__(self, prefix, id, name):
        self.id = id
        self.name = name
        self.pvs = MachinePVs(prefix, id, self)
        self.used_by = -1

    async def set_user(self, user):
        self.used_by = user
        #curio.run(pvs.update)
        await self.pvs.used_by.write(value = self.used_by)
