import unittest
import numpy as np

from main import gen_angles

state_default = list(map(lambda a: np.sqrt(a), [.03, .07, .15, .05, .1, .3, .2, .1]))

class test(unittest.TestCase):
    def test1(self):
        assert(np.allclose(gen_angles(state_default), [1.98, 1.91, 1.43, 1.98, 1.05, 2.09, 1.23], rtol=.01))
    def test2(self):
        return
