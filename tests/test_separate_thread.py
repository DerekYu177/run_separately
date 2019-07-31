import unittest
# from asyncnostic import asyncnostic

from .fixtures import KlassNoExplicitLoop
from run_separately.separate_thread import KlassThreadWrapper

class TestKlassThreadWrapper(unittest.TestCase):
    def setUp(self):
        user_defined_klass = KlassNoExplicitLoop
        user_defined_klass = KlassThreadWrapper(user_defined_klass)
        self.user_defined_klass = user_defined_klass(1, 2)

    def test_attributes_exists_on_user_defined_class(self):
        assert self.user_defined_klass.a == 1
        assert self.user_defined_klass.b == 2
