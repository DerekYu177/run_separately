import multiprocessing
import asyncio
import inspect


DEFAULT_METHODS = ["start", "stop"]

class KlassProcessWrapper:
    pass

def run_in_separate_process(klass, callable_methods=DEFAULT_METHODS):
    class KlassWrapper:
        def __repr__(self):
            return f"Wrapped_{self._inst_klass.__class__.__name__}"

        def __init__(self, *args, **kwargs):
            self._inst_klass = klass(*args, **kwargs)
            self._process_stop_event = multiprocessing.Event()
            self._return_inst_klass = multiprocessing.Queue()

            self._internal_ctrl_args = {
                "inst_klass": self._inst_klass,
                "process_stop_event": self._process_stop_event,
                "return_inst_klass": self._return_inst_klass,
            }

            self._process = multiprocessing.Process(
                name=f"Wrapped_{self._inst_klass.__class__.__name__}",
                target=self._run,
                args=(self._async_run,),
                kwargs={**self._internal_ctrl_args},
                daemon=True,
            )

        @staticmethod
        async def _async_run(loop, inst_klass, process_stop_event):
            inst_klass.start()
            # await inst_klass.start(loop)

            while not process_stop_event.is_set():
                await asyncio.sleep(0)

            inst_klass.stop()
            # await inst_klass.stop()

        def _run(self, coro, **internal_ctrl_args):
            loop = asyncio.new_event_loop()

            future = coro(loop, **internal_ctrl_args)
            loop.run_until_complete(future)

            loop.stop()
            loop.close()

        async def start(self):
            self._process.start()

        async def stop(self):
            self._process_stop_event.set()

        def __getattribute__(self, key):
            #     # try:
            #     # value = super().__getattribute__(key)
            #     # except AttributeError:
            #     value = self._inst_klass.__getattribute__(key)
            #
            #     return value
            import pdb

            pdb.set_trace()

    wrapper = KlassWrapper
    wrapper.__name__ = klass.__name__
    return wrapper
