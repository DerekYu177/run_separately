import unittest
# from asyncnostic import asyncnostic

import asyncio
from run_separately import run_separately_as

from .fixtures import KlassNoExplicitLoop

# @asyncnostic
# class TestRunInSeparateProcess(unittest.TestCase):
#     async def test_with_no_explicit_loop(self, loop):
#         klass = KlassNoExplicitLoop
#         klass = run_in_separate_process(klass)
#         inst_klass = klass("apples", b="bananas")
#
#         await inst_klass.start()
#         await asyncio.sleep(0)
#         await inst_klass.stop()
#
#         assert inst_klass.started
#         assert inst_klass.stopped
#         assert not inst_klass.async_started
#         assert not inst_klass.async_stopped
#
#         assert inst_klass.a == "apples"
#         assert inst_klass.b == "bananas"
