class KlassNoExplicitLoop:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.started = False
        self.stopped = False

        self.async_started = False
        self.async_stopped = False

    def start(self):
        self.started = True

    async def astart(self, loop):
        self.async_started = True

    def stop(self):
        self.stopped = True

    async def astop(self):
        self.async_stopped = True
